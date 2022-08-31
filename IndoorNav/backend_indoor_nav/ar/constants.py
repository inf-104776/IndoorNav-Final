"""This module contains all constants for AR """

UP_DIR = 'up'
DOWN_DIR = 'down'
LEFT_DIR = 'left'
RIGHT_DIR = 'right'
TURN_AROUND_DIR = 'turn'
STAIRS_UP_DIR = 'stairs_up'
STAIRS_DOWN_DIR = 'stairs_down'
NO_DIR = 'none'

DIR_1 = 1
DIR_2 = 2
DIR_3 = 3
DIR_4 = 4


########
## AR ##
########

LENGTH_PER_UNIT = 2.5
IMG_HEIGHT_AR = 480
IMG_WIDTH_AR = 270

DIR_TEST_IMAGES = "backend_indoor_nav\\training\\test_images"
DIR_CAM_CAPTURES = "backend_indoor_nav\\training\\cam_captures"

BASE_DIR_AR = "backend_indoor_nav\\ar\\"

# atan Angle Constants for line detection
DIAGONAL_ANGLE_BOTTOM_LEFT_MIN60 = -60 
DIAGONAL_ANGLE_BOTTOM_LEFT_120 = 120 

DIAGONAL_ANGLE_BOTTOM_RIGHT_60 = 60 
DIAGONAL_ANGLE_BOTTOM_RIGHT_MIN120 = -120 

HORIZONTAL_ANGLE_0 = 0
HORIZONTAL_ANGLE_180 = 180
HORIZONTAL_ANGLE_MIN180 = -180

VERTICAL_ANGLE_90 = 90 
VERTICAL_ANGLE_MIN90 = -90 
