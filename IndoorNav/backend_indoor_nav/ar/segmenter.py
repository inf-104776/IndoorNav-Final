# System libs
import csv
import  scipy.io
from PIL import Image, ImageFilter
import torchvision.transforms
from cv2 import cv2
from torch import torch
import numpy
import PIL.Image

# Our libs
from mit_semseg.models import ModelBuilder, SegmentationModule
from mit_semseg.utils import colorEncode

from ar.constants import BASE_DIR_AR

import time 

COLOR_MAT = 'data\\color150.mat'
OBJECT150 = 'data\\object150_info.csv'
ENCODER = 'ckpt\\ade20k-resnet50dilated-ppm_deepsup\\encoder_epoch_20.pth'
DECODER = 'ckpt/ade20k-resnet50dilated-ppm_deepsup/decoder_epoch_20.pth'

colors = scipy.io.loadmat(BASE_DIR_AR + COLOR_MAT)['colors']
names = {}
with open( BASE_DIR_AR + OBJECT150) as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        names[int(row[0])] = row[5].split(";")[0]

def create_model():
    # Network Builders
    net_encoder = ModelBuilder.build_encoder(
        arch='resnet50dilated',
        fc_dim=2048,
        weights= BASE_DIR_AR + ENCODER)
    net_decoder = ModelBuilder.build_decoder(
        arch='ppm_deepsup',
        fc_dim=2048,
        num_class=150,
        weights= BASE_DIR_AR + DECODER,
        use_softmax=True)

    crit = torch.nn.NLLLoss(ignore_index=-1)
    segmentation_module = SegmentationModule(net_encoder, net_decoder, crit)
    segmentation_module.eval()
    return segmentation_module

def preprocess_image(img_path):
    pil_image = Image.open(img_path).convert('RGB')
    #Blur to reduce noise
    pil_image = pil_image.filter(ImageFilter.BLUR)

    # Load and normalize one image as a singleton tensor batch
    pil_to_tensor = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(
            mean=[0.485, 0.456, 0.406], # These are RGB mean+std values
            std=[0.229, 0.224, 0.225])  # across a large photo dataset.
    ])
    img_data = pil_to_tensor(pil_image)

    singleton_batch = {'img_data': img_data[None, :]} # img_data[None].cuda()
    output_size = img_data.shape[1:]

    return (singleton_batch, output_size)

def select_prediction(pred_img, index ):
    """selects the prediction with the given index as color code and returns an image"""
    pred = pred_img.copy()
    pred[pred != index] = -1
    return pred

def visualize_result(pred, img=None, return_image=False, index=None):
    # filter prediction class if requested
    if index is not None:
        pred = pred.copy()
        pred[pred != index] = -1
        print(f'{names[index+1]}:')

    # colorize prediction
    pred_color = colorEncode(pred, colors).astype(numpy.uint8)

    if return_image:
        im_vis = numpy.concatenate((img, pred_color), axis=1)
        return im_vis

def find_largest_contour_idx(contours):
    idx_max_contour = None
    max_area = 0
    for c_idx in range(len(contours)):
        area = cv2.contourArea(contours[c_idx])
        if area > max_area:
            max_area = area
            idx_max_contour = c_idx
    return idx_max_contour

def find_convex_hull(pred_img):
    ''' calculates the contur and convex hull'''
   
    pred_img = pred_img.astype(numpy.uint8)
    _, thresh = cv2.threshold(pred_img, 50, 255, cv2.THRESH_BINARY)
    im2 = thresh.copy()

    #contours to create the convex hull from
    contours, _ = cv2.findContours(im2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    largest_contour_idx = find_largest_contour_idx(contours)

    #empty black image to display lines
    drawing = numpy.zeros((thresh.shape[0], thresh.shape[1], 3), numpy.uint8)

    # draw contours and hull points
    if len(contours) != 0:
        hull = cv2.convexHull(contours[largest_contour_idx], False)
        
        color = (255, 255, 255) 
        cv2.drawContours(drawing, [hull], 0, color, 1, 8)

    return drawing

def convert_prediction_to_binary(pred):
    """converts prediction image to binary image"""
    for y, _y in enumerate(pred):
        for x, _x in enumerate(pred[y]):
            pred[y][x] =  0 if pred[y][x] == -1 else 255
    return pred

def create_segmentation_image(segmenter, img_path, object_idx=None):
    # Segmentation
    (singleton_batch, output_size) =  preprocess_image(img_path)
    scores = segmenter(singleton_batch, segSize=output_size)

    # Get the predicted scores for each pixel
    _, pred = torch.max(scores, dim=1)
    pred = pred.cpu()[0].numpy()
    if object_idx is None: 
        return pred
    
    pred_image = select_prediction(pred, object_idx)
    pred_image = convert_prediction_to_binary(pred_image)
    return pred_image

def draw_lines_from_hough(lines, hull_grey):
    """Only to debug - draws given lines from the hough lines transform"""
    lines_dst = cv2.cvtColor(hull_grey, cv2.COLOR_GRAY2BGR)

    # Draw the lines
    if lines is not None:
        for line in lines:
            l = line[0]
            cv2.line(lines_dst, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)


def get_floor_lines(segmenter, img_path):
    ''' Calculates the lines of the convex hull of the floor of the given image
    May take a while on a cpu '''
    floor_idx = 3
    floor = create_segmentation_image(segmenter, img_path, floor_idx)

    hull = find_convex_hull(floor)
    hull_grey = cv2.cvtColor(hull, cv2.COLOR_BGR2GRAY)

    # process image to find lines in the convex hull
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    hull_grey = cv2.dilate(hull_grey, kernel, iterations=2)

    #return lines in convex hull
    res = cv2.HoughLinesP(hull_grey, 1, numpy.pi / 180, 30, 0, 10, 30), hull_grey

    return res 