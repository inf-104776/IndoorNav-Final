import math
from ar.constants import DIR_TEST_IMAGES, DOWN_DIR, LEFT_DIR, NO_DIR, RIGHT_DIR, UP_DIR
from ar.helper import find_max_x, find_min_x, get_inverse_direction, get_left_neighbor_dir, get_next_different_direction_and_dist_in_meter, get_right_neighbor_dir, len_of_line
from cv2 import cv2
import numpy as np
from wayfinding.wayfinding import calc_distance_to_door_if_visible, calc_distance_to_end_of_hallway

DIAGONAL_COLOR = (255, 0, 0)
VERTICAL_COLOR = (0, 255, 0)
HORIZONTAL_COLOR = (0, 0, 255)

LINETYPE_HORIZONTAL = 'h'
LINETYPE_VERTICAL = 'v'
LINETYPE_DIAGONAL = 'd'

IMG_HEIGHT_AR = 960
IMG_WIDTH_AR = 540

# when a line is considered unusable
VERTICAL_LINE_LEN_THRESHOLD = IMG_HEIGHT_AR / 8
DIAGONAL_LINE_LEN_THRESHOLD = IMG_HEIGHT_AR / 8

# atan Angle Constants for line detection
HORIZONTAL_ANGLE_0 = 0
HORIZONTAL_ANGLE_180 = 180
HORIZONTAL_ANGLE_MIN180 = -180

VERTICAL_ANGLE_90 = 90 
VERTICAL_ANGLE_MIN90 = -90 

DIAGONAL_ANGLE_BOTTOM_LEFT_MIN60 = -60 
DIAGONAL_ANGLE_BOTTOM_LEFT_120 = 120 

DIAGONAL_ANGLE_BOTTOM_RIGHT_60 = 60 
DIAGONAL_ANGLE_BOTTOM_RIGHT_MIN120 = -120 

# range in which angles from lines are detected
# diagonal lines have +-10 degrees, others +-5    
ANGLE_RANGE_DIAGONAL = 20
ANGLE_RANGE_OTHER = 8

MARKER_DISTANCE_DIAGONAL = IMG_HEIGHT_AR / 8


HORIZONTAL_SEARCH_WINDOW_UPPER = IMG_HEIGHT_AR -IMG_HEIGHT_AR * 1/3
HORIZONTAL_SEARCH_WINDOW_LOWER = IMG_HEIGHT_AR * 1/3

HORIZONTAL_MARKER_OFFSET = IMG_HEIGHT_AR / 20

def split_diagonals_to_left_and_right(diagonal_lines):
    """ Splits the given diagonal lines in left and right """
    left = []
    right = []
    for line in diagonal_lines:
        angle = calc_angle(line[0], line[1], line[2], line[3])
        if( is_approx_angle(angle, DIAGONAL_ANGLE_BOTTOM_LEFT_MIN60, ANGLE_RANGE_OTHER)
            or is_approx_angle(angle, DIAGONAL_ANGLE_BOTTOM_LEFT_120, ANGLE_RANGE_OTHER)):
            left.append(line)
        else:
            right.append(line)
    return (left, right)

def find_longest_line(lines):
    max_len = 0
    max_line = None
    for line in lines:
        len = len_of_line(line)
        if (len > max_len):
            max_line = line
    return max_line 

def find_mid_from_given_diagonals(left, right):
    min_x_l = find_min_x(left)
    max_x_r = find_max_x(right)
    return ((max_x_r - min_x_l ) / 2) + min_x_l

def calc_diagonal_marker_direction(current_direction, next_direction):
    if get_inverse_direction(current_direction) == next_direction:
        return DOWN_DIR
    elif current_direction == next_direction:
        return UP_DIR
    else:
        return None

def calc_diagonal_marker_placement(diagonal_lines, start_height, current_direction, next_direction):
    '''Sets the marker between both diagonal lines if present 
    stop_height is set the end of the hallway or where the corresponding door is located'''
    marker = []

    if diagonal_lines != []:
        (left, right) = split_diagonals_to_left_and_right(diagonal_lines)
        mid_x = find_mid_from_given_diagonals(left, right)

        curr_height =  IMG_HEIGHT_AR
        idx_marker = 1
        while curr_height > start_height:
            marker.append((mid_x, curr_height))
            #makes the distance between markers smaller when farther away
            curr_height -= (IMG_HEIGHT_AR / 2.5) / (2 * idx_marker)
            idx_marker += 1

        marker_dir = calc_diagonal_marker_direction(current_direction, next_direction)
        
        return (marker, marker_dir)


def calc_horizontal_or_vertical_marker_direction(current_direction, next_direction):
    ''' calculates the direction the horizontal/vertical marker is pointing'''

    if int(get_left_neighbor_dir(current_direction)) == next_direction:
        return LEFT_DIR
    if int(get_right_neighbor_dir(current_direction)) == next_direction:
        return RIGHT_DIR
    return None


def calc_horizontal_marker(horizontal_lines, current_direction, next_direction):
    ''' calculates the marker position for the horizontal markers and the direction
    to which the marker is pointing'''
    if horizontal_lines != []:
        max_height = 0
        max_line = None
        for line in horizontal_lines:
            if line[1] > max_height:
                max_height = line[1]
                max_line = line
        marker_dir = calc_horizontal_or_vertical_marker_direction(current_direction, next_direction)
        return (((max_line[0] + max_line[2])/2, max_height - HORIZONTAL_MARKER_OFFSET), marker_dir)
    return None

def calc_vertical_marker(vertical_lines, path, current_direction, next_direction, end_hallway, mid_floor):
    ''' calculates the marker position for the vertical markers and the direction
    to which the marker is pointing'''
    arrow_dir = calc_horizontal_or_vertical_marker_direction(current_direction, next_direction)
    if not arrow_dir is None:
        distance_end = calc_distance_to_end_of_hallway(path.nodes[0].name, current_direction)
        distance_door = calc_distance_to_door_if_visible(path.nodes[0].name, path.get_last_node(),
                                                        current_direction, next_direction)

        pos_relative = distance_end / distance_door
        dist_absolute = (IMG_HEIGHT_AR - end_hallway)
        pos_absolute = end_hallway + (dist_absolute * pos_relative)

        return ((mid_floor, pos_absolute), arrow_dir)
    return None

def get_endpoint_of_arrowed_line(marker_pos, direction):
    ''' only to debug drawing - calculates the endposition of arrow '''
    arrow_length = 30
    marker_pos = (int(marker_pos[0]), int(marker_pos[1])) 
    if( direction == UP_DIR):
        return (marker_pos[0], marker_pos[1] - arrow_length)
    elif(direction == DOWN_DIR):
        return (marker_pos[0], marker_pos[1] + arrow_length)
    elif(direction == LEFT_DIR):
        return (marker_pos[0] - arrow_length, marker_pos[1])
    elif(direction == RIGHT_DIR):
       return (marker_pos[0] + arrow_length, marker_pos[1])
    return NO_DIR

def show_image_with_marker(horizontal_marker, vertical_marker, diagonal_marker, src_img):
    ''' Shows image with all markers'''
    img = cv2.imread(src_img, 2) 
    img = cv2.resize(img, (IMG_WIDTH_AR, IMG_HEIGHT_AR))
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    
    marker_img = img.copy()
    if len(diagonal_marker) > 0:
        for marker in diagonal_marker[0]:
            marker_image = cv2.arrowedLine(marker_img, (int(marker[0]), int(marker[1])), get_endpoint_of_arrowed_line(marker, diagonal_marker[1]),color=DIAGONAL_COLOR, thickness=2)
    
    if len(horizontal_marker) > 0:
        if not horizontal_marker[0] is None and not horizontal_marker[1] is None:
            marker_image = cv2.arrowedLine(marker_img, (int(horizontal_marker[0][0]), int(horizontal_marker[0][1])), get_endpoint_of_arrowed_line(horizontal_marker[0], horizontal_marker[1]), color=HORIZONTAL_COLOR, thickness=2)

    if len(vertical_marker) > 0:
        if not vertical_marker[0] is None and not vertical_marker[1] is None:
            marker_image = cv2.arrowedLine(marker_img, (int(vertical_marker[0][0]), int(vertical_marker[0][1])), get_endpoint_of_arrowed_line(vertical_marker[0], vertical_marker[1]), color=VERTICAL_COLOR, thickness=2)
     

    cv2.imshow("Marker Pos", marker_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def calc_marker_positions_depr(path, current_direction):
    ''' calculates all marker positions'''
    current_direction = int(current_direction)

    src_img = DIR_TEST_IMAGES + '\\10.jpg'
    stop_height = 0

    (vertical_lines, horizontal_lines, diagonal_lines) = detect_relevant_lines_depcrecated(src_img)
    #check beforehand if marker is needed
    _, next_different_direction = get_next_different_direction_and_dist_in_meter(path, current_direction)
    horizontal_marker = calc_horizontal_marker(horizontal_lines,
                                                    current_direction, next_different_direction)
    if not horizontal_marker is None :
        stop_height = horizontal_marker[0][1] + HORIZONTAL_MARKER_OFFSET
    diagonal_marker = calc_diagonal_marker_placement(diagonal_lines, stop_height,current_direction, path.directions[0])
    
    if not horizontal_marker[0] is None: 
        vertical_marker = calc_vertical_marker(vertical_lines, path, current_direction, next_different_direction, stop_height, horizontal_marker[0][0])

    show_image_with_marker(horizontal_marker, vertical_marker, diagonal_marker, src_img)

    return (horizontal_marker, vertical_marker, diagonal_marker)

def is_approx_angle(angle, angle_to_test, angle_range):
    ''' checks if a given angle matches an angle that is useful to detect'''
    if angle_to_test == HORIZONTAL_ANGLE_180 or angle_to_test == HORIZONTAL_ANGLE_MIN180: #180 == -180
        #between -175 and -180
        is_higher_than_lower_range = angle < HORIZONTAL_ANGLE_MIN180 - (angle_range/2) and angle >= HORIZONTAL_ANGLE_MIN180
        #between 175 and 180
        is_lower_than_higher_range = angle > HORIZONTAL_ANGLE_180 - (angle_range/2) and angle <= HORIZONTAL_ANGLE_180
        return is_higher_than_lower_range or is_lower_than_higher_range

    return angle > (angle_to_test - (angle_range / 2.0)) and angle < (angle_to_test + (angle_range / 2.0))

def choose_color(angle):
    ''' detects the angle and specifies the line type'''
    if (is_approx_angle(angle, DIAGONAL_ANGLE_BOTTOM_LEFT_MIN60, ANGLE_RANGE_DIAGONAL)
        or is_approx_angle(angle, DIAGONAL_ANGLE_BOTTOM_LEFT_120, ANGLE_RANGE_DIAGONAL)
        or is_approx_angle(angle, DIAGONAL_ANGLE_BOTTOM_RIGHT_60, ANGLE_RANGE_DIAGONAL)
        or is_approx_angle(angle, DIAGONAL_ANGLE_BOTTOM_RIGHT_MIN120, ANGLE_RANGE_DIAGONAL) ):
        return DIAGONAL_COLOR
    
    elif (is_approx_angle(angle,VERTICAL_ANGLE_90, ANGLE_RANGE_OTHER)
        or is_approx_angle(angle, VERTICAL_ANGLE_MIN90, ANGLE_RANGE_OTHER)):
        return VERTICAL_COLOR

    elif (is_approx_angle(angle, HORIZONTAL_ANGLE_0, ANGLE_RANGE_OTHER)
        or is_approx_angle(angle, HORIZONTAL_ANGLE_180, ANGLE_RANGE_OTHER)
        ):
        return HORIZONTAL_COLOR
    
    return None

def calc_angle(x1, y1, x2, y2):
    return math.degrees(math.atan2(y2-y1, x2-x1)) 

def filter_line(line, color):
    ''' filters useful lines'''
    if color == HORIZONTAL_COLOR:
        return True
        #return line[1] < (IMG_HEIGHT - (IMG_HEIGHT  * 1 / 10)) and line[1] < (IMG_HEIGHT  * 2 / 3) and line[1] > IMG_HEIGHT * (1/3)
    if color == VERTICAL_COLOR:
        dist = len_of_line(line)
        return dist > VERTICAL_LINE_LEN_THRESHOLD
    if color == DIAGONAL_COLOR:
        dist = len_of_line(line)
        return (line[1] > (IMG_HEIGHT_AR /2) or line[3] > (IMG_HEIGHT_AR /2) ) and dist > DIAGONAL_LINE_LEN_THRESHOLD

def change_brightness_and_contrast(img, brightness, contrast=1.0):
    '''changes brightness and contrast'''
    for row in range(len(img)):
        print("Row " + str(row))
        for col in range(len(img[row])):
            new_val =  int(img[row][col] + brightness) * contrast
            if new_val > 255: 
                new_val = 255
            elif new_val < 0:
                new_val = 0
            img[row][col] = new_val
    return img

def detect_relevant_lines_depcrecated(src_image):
    ''' detects all relevant lines for marker positioning'''
    img = cv2.imread(src_image, 2)
    img = cv2.resize(img, (IMG_WIDTH_AR, IMG_HEIGHT_AR))
    cv2.imshow("Orig", img)
    cv2.waitKey(0)

    best_brightness = 120.0
    brightness_correction = best_brightness - np.average(img)
    img = change_brightness_and_contrast(img, brightness=brightness_correction, contrast=1.0)
    img = cv2.normalize(img, None, alpha=0, beta=230, norm_type=cv2.NORM_MINMAX) 

    cv2.imshow("adjusted brightness and contrast", img)
    cv2.waitKey(0)
    
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img, (3,3), 0)

    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=80, threshold2=200) # Canny Edge Detection
    cv2.imshow("Canny", edges)
    cv2.waitKey(0)
    
    filtered = edges.copy()
    vertical_size = int(len(filtered) / (IMG_HEIGHT_AR / 4 ))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (vertical_size, vertical_size))
    lines_dilated = cv2.dilate(filtered, kernel, iterations=3) 
    lines_eroded = cv2.erode(lines_dilated, kernel, iterations=3)
    
    cv2.imshow("Eroded", lines_eroded)
    cv2.waitKey(0)

    lines_hough_p = cv2.HoughLinesP(lines_eroded, 1, np.pi / 180, 50, None, 10, 30)

    horizontal_lines = []
    vertical_lines = []
    diagonal_lines = []
    lines_dst = cv2.cvtColor(lines_eroded, cv2.COLOR_GRAY2BGR)

    #detect lines in various degrees
    if lines_hough_p is not None:
        for i in range(0, len(lines_hough_p)):
            l = lines_hough_p[i][0]
            angle = calc_angle(l[0], l[1], l[2], l[3])
            color = choose_color(angle)
            
            if( filter_line(l, color)):
                cv2.line(lines_dst, (l[0], l[1]), (l[2], l[3]), color, 3, cv2.LINE_AA)
                if(color == VERTICAL_COLOR):
                    vertical_lines.append(l)
                if(color == HORIZONTAL_COLOR):
                    horizontal_lines.append(l)
                if(color == DIAGONAL_COLOR):
                    diagonal_lines.append(l)

    cv2.imshow("Detected relevant Lines", lines_dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return (vertical_lines, horizontal_lines, diagonal_lines)
    
def visualize_relevant_lines(src_image, lines_hough_p):
    img = cv2.imread(src_image, 2)
    img = cv2.resize(img, (IMG_WIDTH_AR, IMG_HEIGHT_AR))
    lines_dst = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    #detect lines in various degrees
    if lines_hough_p is not None:
        for i in range(0, len(lines_hough_p)):
            l = lines_hough_p[i][0]
            color = (0, 240, 230)
            cv2.line(lines_dst, (l[0], l[1]), (l[2], l[3]), color, 3, cv2.LINE_AA)
    
    cv2.imshow("Detected relevant Lines", lines_dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return lines_hough_p

src_image = DIR_TEST_IMAGES + "\\2.jpg"
lines_hough_p = detect_relevant_lines_depcrecated(src_image) 
visualize_relevant_lines(src_image, lines_hough_p)