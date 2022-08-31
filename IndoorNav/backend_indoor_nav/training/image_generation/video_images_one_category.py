import cv2
import os
import math

NUM_IMAGES_PER_CAT = 200
# size of the image used for training the models
IMG_WIDTH_TRAIN = 180
IMG_HEIGHT_TRAIN = 320

src_folder_name = "C:\\Users\\MaraPape\\Desktop\\Master\\Thesis\\Videos\\"
dest_folder_name = 'backend_indoor_nav\\training\\one_category\\'

def create_folder(path):
    try:
        # creating a folder named data
        if not os.path.exists(path):
            os.makedirs(path)

    # if not created then raise error
    except OSError:
        print ('Error: Creating directory of' + path)

def create_frames(src_path, dest_path, filename):
    """creates frames from video at src_path and writes images to dest_path"""
    # Read the video from specified path
    src_dir_path = src_path.rsplit('\\',1)[0]
    skip_steps = calc_num_frames_to_skip(src_dir_path)

    skip_frames = 0
    idx = int(filename[0]) - 1
    skip_frames = skip_steps[idx]

    cam = cv2.VideoCapture(src_path)
    currentframe = 0

    num_frames_captured = 0

    while(True):
        # reading from frame
        ret,frame = cam.read()

        if ret:
            # if video is still left continue creating images
            if currentframe > (num_frames_captured * skip_frames):
                name = '.\\' + dest_path + "\\" + filename[0] + '_f' + str(currentframe) + '.jpg'
                frame = cv2.resize(frame, (IMG_WIDTH_TRAIN, IMG_HEIGHT_TRAIN))
                cv2.imwrite(name, frame)
                num_frames_captured += 1

            currentframe += 1
        else: 
            break
    print(num_frames_captured)

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()


def calc_num_frames_to_skip(path):   
    """calculates how many frames need to be skipped beforde a new
    image is created. Videos at the destination path contain one or 
    more videos per direction"""
    skip_frames = [0.0, 0.0, 0.0, 0.0]
    for root, _, files in os.walk(path):
        for file in files:
            video = cv2.VideoCapture(os.path.join(root, file))
            num_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
            idx = int(file[0]) - 1
            skip_frames[idx] += float(num_frames)

    for i in range(len(skip_frames)):
        skip_frames[i] = skip_frames[i] / NUM_IMAGES_PER_CAT
    
    return skip_frames

def create_images_from_video():
    """creates all images from one video """
    for root, dirs, files in os.walk(src_folder_name):
        for file in files:
            folder_name = root.replace(src_folder_name, "")
            folder_name = folder_name.replace("\\", "")
            folder_name = folder_name + file[0]

            dest_path = os.path.join(dest_folder_name, folder_name)
            src_path = os.path.join(root, file)
            create_folder(dest_path)
            create_frames(src_path, dest_path, file)

create_images_from_video()