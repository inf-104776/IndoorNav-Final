
# Importing all necessary libraries
import cv2
import os

src_folder_name = "C:\\Users\\MaraPape\\Desktop\\Master\\Thesis\\Videos\\"
dest_images_from_video = 'images\\'
training_images = 'training_images\\'


def create_folder(path):

    try:
        # creating a folder named data
        if not os.path.exists(path):
            os.makedirs(path)

    # if not created then raise error
    except OSError:
        print ('Error: Creating directory of' + path)

def create_frames_from_folder(src, dest, keep_folder_structure):
    for root, _, files in os.walk(src):
        for file in files:
            # extract filename
            dest_root = root.replace(src_folder_name, dest_images_from_video)
            filename = dest_root.replace(dest_images_from_video, "")
            filename = filename.replace("\\", "_")
            filename = filename + "_" + file.replace(".mp4", "")

            if(not keep_folder_structure):
                dest_root = training_images
            create_frames(os.path.join(root,file), os.path.join(dest_root, filename), )
            
def create_folder_structure():
    create_folder(training_images)
    for root, dirs, files in os.walk(src_folder_name):
        for dir in dirs:
            dest_root = root.replace(src_folder_name, dest_images_from_video)
            print(os.path.join(dest_root, dir))
            create_folder(os.path.join(dest_root, dir))

def convert_all_videos_to_images(keep_folder_structure):
    for root, dirs, files in os.walk(src_folder_name):
        for dir in dirs:
            dest_root = root.replace(src_folder_name, dest_images_from_video)
            print(os.path.join(dest_root, dir))
            create_frames_from_folder(os.path.join(root, dir), os.path.join(dest_root, dir), keep_folder_structure)   

def create_frames(src_path, dest_path):
    # Read the video from specified path
    cam = cv2.VideoCapture(src_path)
    currentframe = 0
    while(True):
        # reading from frame
        ret,frame = cam.read()

        if ret:
            # if video is still left continue creating images
            name = '.\\' + dest_path + '_f' + str(currentframe) + '.jpg'
            if currentframe % 100 == 0 :
                cv2.imwrite(name, frame)
            
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

create_folder_structure()  
convert_all_videos_to_images(False)  