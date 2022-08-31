import os
from tensorflow import keras
import tensorflow as tf

import time

batch_size = 15
img_height = 160
img_width = 90

TRESHOLD_PRED = 0.2 #0.6

SRC_TEST_IMG = "backend_indoor_nav\\training\\cam_captures\\5.jpg"
SRC_DIR = "backend_indoor_nav\\training\\cam_captures"
IMAGES_ONE_CAT_DIR = "backend_indoor_nav\\training\\one_category"

def decode_img(img):
  img = tf.image.decode_jpeg(img, channels=3) #color images
  img = tf.image.convert_image_dtype(img, tf.float32) 
   #convert unit8 tensor to floats in the [0,1]range
  return img 
    
def get_labels_for_class(class_num):
    # extract category names from image folder
    return  os.listdir(IMAGES_ONE_CAT_DIR)[class_num] 

def get_index_of_element(element, list):
    for i in range(len(list)):
        if(list[i] == element):
            return i
    return None

def find_median(positions):
    pos_set = list(set(positions)) # remove duplicates
    amounts = [0] * len(pos_set)
    for pos in positions:
        index = get_index_of_element(pos, pos_set)
        amounts[index] += 1
    max = 0
    max_idx = 0
    for i in range(len(amounts)):
        if amounts[i] > max:
            max = amounts[i]
            max_idx = i

    return pos_set[max_idx]

def initial_localization(model):
    """ Calculates the initial localization, eg 5 localizations and calculation of the mdedian"""
    images = []
    image_arrays = []
    for i in range(len(os.listdir(SRC_DIR))): 
        img = keras.preprocessing.image.load_img(SRC_DIR + "\\" +  str(i) + ".jpg", target_size=(320,180,3))
        images.append(img)
        img_array = keras.preprocessing.image.img_to_array(img)[:,:,:]
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis
        image_arrays.append(img_array)

    predictions = []
    pred_classes = []
    pred_labels = []
    
    # predict all images
    for img_array in image_arrays:
        preds = model.predict(img_array)
        if(preds[0][preds.argmax(axis=-1)[0]] >= TRESHOLD_PRED):
            predictions.append( preds )
            pred_classes.append( preds.argmax(axis=-1))
            pred_labels.append(get_labels_for_class(preds.argmax(axis=-1)[0]))
    return find_median(pred_labels)

def normal_localization(model, img_path=SRC_TEST_IMG):
    img = keras.preprocessing.image.load_img(img_path , target_size=(320,180,3))
    img_array = keras.preprocessing.image.img_to_array(img)[:,:,:]
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis
    
    preds = model.predict(img_array)
    
    # check if prediction is good enough in general
    if(preds[0][preds.argmax(axis=-1)[0]] >= TRESHOLD_PRED):
        pred_label = get_labels_for_class(preds.argmax(axis=-1)[0])
        return (pred_label, preds[0][preds.argmax(axis=-1)[0]])
    return None, 0.0
