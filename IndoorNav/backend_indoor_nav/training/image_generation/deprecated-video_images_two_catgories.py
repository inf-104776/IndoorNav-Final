import cv2
import os

"""this script restructures the folder structure of src_folder_name for 
training of a model for (floor and direction) and (position) """

src_folder_name = "backend_indoor_nav\\training\\one_category"
dest_dir_floor = 'backend_indoor_nav\\training\\dir_floor\\'
dest_position = 'backend_indoor_nav\\training\\position\\'

def create_folder(path):

    try:
        # creating a folder named data
        if not os.path.exists(path):
            os.makedirs(path)

    # if not created then raise error
    except OSError:
        print ('Error: Creating directory of' + path)

def create_folders():
    for root, dirs, files in os.walk(src_folder_name):
        for folder in dirs:
            p1 = folder.replace(src_folder_name, "")
            p1 = p1.replace("\\", "")
            folder_dir_floor = p1[0:2] + p1[-1:]
            
            folder_position = folder[2:4]

            dest_path_dir_floor = os.path.join(dest_dir_floor, folder_dir_floor)
            dest_path_position = os.path.join(dest_position, folder_position)
            src_path = os.path.join(root, folder)

            create_folder(dest_path_dir_floor)
            create_folder(dest_path_position)
        
        create_files(files, root)

                  
def create_files(files, root):
    for file in files:
            
        src = root + "\\" + file
        original_foldernames = root.split("\\", 4)
        original_foldername = original_foldernames[3]
        
        frame_names = file.split("_", 1)
        frame_name = "_" + frame_names[1]
        
        dest_image_name = original_foldername + frame_name
        
        foldername_floor_dir = original_foldername[0:2] + original_foldername[-1:]
        foldername_pos = original_foldername[2:4]

        file_name_dir_floor = dest_dir_floor + foldername_floor_dir +"\\" + dest_image_name
        file_name_pos = dest_position + foldername_pos + "\\" + dest_image_name

        #reads the image and copies it to the acording folders
        img_src = cv2.imread(src)
        img_clone = img_src.copy()
        cv2.imwrite(file_name_dir_floor, img_clone)
        cv2.imwrite(file_name_pos, img_clone)

create_folders()