import math
from os import truncate
from cv2 import cv2
from matplotlib.pyplot import hlines
from ar.segmenter import get_floor_lines

import wayfinding.wayfinding as wf 
import ar.helper as helper
import ar.constants as constants

""" This module calculates the marker positions and orientations"""

def calc_marker_direction_for_floor(current_direction, next_direction):
    """ calculates the marker direction for markers on the floor """
    if helper.get_inverse_direction(current_direction) == next_direction:
        return constants.DOWN_DIR
    elif current_direction == next_direction:
        return constants.UP_DIR
    else:
        return constants.NO_DIR

def get_endpoint_of_arrowed_line(marker_pos, direction):
    ''' only to debug drawing - calculates the endposition of arrow '''
    arrow_length = 18
    marker_pos = (int(marker_pos[0]), int(marker_pos[1])) 
    if( direction == constants.UP_DIR):
        return (marker_pos[0], marker_pos[1] - arrow_length)
    elif(direction == constants.DOWN_DIR or direction == constants.TURN_AROUND_DIR):
        return (marker_pos[0], marker_pos[1] + arrow_length)
    elif(direction == constants.LEFT_DIR):
        return (marker_pos[0] - arrow_length, marker_pos[1])
    elif(direction == constants.RIGHT_DIR):
       return (marker_pos[0] + arrow_length, marker_pos[1])
    return constants.NO_DIR

def show_image_with_marker(horizontal_marker, diagonal_marker, src_img, return_image=False):
    ''' Shows image with all markers'''
    
    marker_img = src_img.copy()
    if not diagonal_marker is None and len(diagonal_marker) > 0 and not diagonal_marker[1] == constants.NO_DIR:
        if len(diagonal_marker) > 1 and diagonal_marker[1] == constants.DOWN_DIR:
            marker_img = cv2.arrowedLine(marker_img, (int(marker_img.shape[0]), int(marker_img.shape[1])), get_endpoint_of_arrowed_line((int(marker_img.shape[0]), int(marker_img.shape[1])), diagonal_marker[1]), color=(255, 255, 0), thickness=2)
    
        for marker in diagonal_marker[0]:
            marker_img = cv2.arrowedLine(marker_img, (int(marker[0]), int(marker[1])), get_endpoint_of_arrowed_line(marker, diagonal_marker[1]),color=(255, 255, 0), thickness=2)
    
    if len(horizontal_marker) > 0:
        if not horizontal_marker[0] is None and not horizontal_marker[1] is None:
            marker_img = cv2.arrowedLine(marker_img, (int(horizontal_marker[0][0]), int(horizontal_marker[0][1])), get_endpoint_of_arrowed_line(horizontal_marker[0], horizontal_marker[1]), color=(255, 0, 255), thickness=2)

    if return_image:
        return marker_img

def calc_horizontal_or_vertical_marker_direction(current_direction, next_direction, is_stairs = False):
    ''' calculates the direction the horizontal/vertical marker is pointing'''
    if int(helper.get_left_neighbor_dir(current_direction)) == next_direction:
        return constants.LEFT_DIR
    if int(helper.get_right_neighbor_dir(current_direction)) == next_direction:
        return constants.RIGHT_DIR
    if int(helper.get_inverse_direction(current_direction)) == next_direction:
        #TODO check if stairs are near then the next direction is also inverse direction
        return constants.TURN_AROUND_DIR
    return constants.NO_DIR

def calculate_end_of_floor_marker(lines, x=None):
    """calculates the height (in pixels) when the floor ends. 
    If x is given, the corresponding line is searched """
    y_height = helper.find_min_y(lines)
    h_lines = helper.find_lines_near_given_height(lines, y_height)
    if x: 
        return (x, y_height)
    if h_lines:
        min = helper.find_min_x(h_lines)
        max = helper.find_max_x(h_lines)
        
        mid_x = (min + max) / 2
        return mid_x, y_height
    else:
        # The point according to y_height
        return helper.find_point_from_given_y_value(lines, y_height)

def find_vanishing_point(lines, img=None):
    """calculates the vanishing point by albertis method"""
    is_60_deg_line = None
    is_120_deg_line = None
    if not lines is None: 
        #finds the right diagonal lines
        for line in lines:
            line = line[0]
            angle = helper.calc_angle(line[0], line[1], line[2], line[3])
            
            if (helper.is_approx_angle(angle, constants.DIAGONAL_ANGLE_BOTTOM_LEFT_MIN60, 30) or  
                helper.is_approx_angle(angle, constants.DIAGONAL_ANGLE_BOTTOM_LEFT_120, 30) ):
                is_120_deg_line = line
            elif(helper.is_approx_angle(angle, constants.DIAGONAL_ANGLE_BOTTOM_RIGHT_60, 30) or
                helper.is_approx_angle(angle, constants.DIAGONAL_ANGLE_BOTTOM_RIGHT_60, 30)):
                is_60_deg_line = line
        if not is_120_deg_line is None and not is_60_deg_line is None:
            #calculate intersection of found lines
            van_point = helper.line_intersection(
                (is_60_deg_line[0], is_60_deg_line[1]), 
                (is_60_deg_line[2], is_60_deg_line[3]),
                (is_120_deg_line[0], is_120_deg_line[1]),
                (is_120_deg_line[2], is_120_deg_line[3]))

            return (int(van_point[0]), int(van_point[1]))    
                
    else:
        print("No vertical lines have been found to create vanishing point")

def calculate_markerpos_floor(lines, img):
    """ calculates the marker positions for markers on the floor"""
    vanishing_point = find_vanishing_point(lines, img)
    offset_y = 50
    offset_x = 500
    if vanishing_point is None:
        vanishing_point = (int(img.shape[0] / 3), int(img.shape[1]/2))
    d_point = (vanishing_point[0] + offset_x, vanishing_point[1] - offset_y)
    res = []
    NUM_LINES_D_TO_FLOOR = 3
    size_per_part = int(constants.IMG_WIDTH_AR / (NUM_LINES_D_TO_FLOOR - 1))
    x_pos = []
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    #make rays through x-axis
    for i in range(NUM_LINES_D_TO_FLOOR):
        x_pos.append((i * size_per_part, constants.IMG_HEIGHT_AR) )
    
    #use negative for lines that result in lower y-values
    for i in range(NUM_LINES_D_TO_FLOOR):
        if i > 0:
            x_pos.append((-i * size_per_part, constants.IMG_HEIGHT_AR) )

    vert_line = (constants.IMG_WIDTH_AR, 0, constants.IMG_WIDTH_AR, constants.IMG_HEIGHT_AR )
    for pos in x_pos:
        #Intersection from the line that goes from pos to d 
        # and the vertical line from (0, IMG_WIDTH)
        intersection_points= helper.line_intersection(
            (pos[0], pos[1]), 
            (d_point[0], d_point[1]),
            (vert_line[0], vert_line[1]),
            (vert_line[2], vert_line[3]))

        res.append((int(vanishing_point[0]), int(intersection_points[1])))

    return res

def calc_horizontal_or_vertical_marker_position(path, dest, curr_dir, lines, marker_pos_up_down, img=None):
    """ calcs the markerposition that shows left or right turn"""
    dest_in_hw = helper.dest_in_hallway(path, dest, curr_dir)
    new_y = 240
    if not dest_in_hw:
        return calculate_end_of_floor_marker(lines, marker_pos_up_down[0][0])
    else: 
        sorted_pos = sorted(marker_pos_up_down, key=lambda tup: tup[1], reverse=True)

        distance_end = wf.calc_distance_to_end_of_hallway(path.nodes[0].name, curr_dir)
        distance_door = wf.calc_distance_to_door_if_visible(path.nodes[0].name, path.get_last_node().name,
                                                        curr_dir)
        num_parts = len(marker_pos_up_down) 
        size_d = distance_end / num_parts
        #select correct interval in which the destination lies
        interval = int((distance_door / size_d) + 1.0) #also index of sorted_pos
        
        if(interval + 1 < len(sorted_pos)):
            pixel_dist = sorted_pos[interval][1] - sorted_pos[interval + 1][1]
            dist_per_pixel = size_d / pixel_dist
            remaining_distance = distance_door -((interval - 1) * size_d)
            #calculate the offset from the interval to mark the destintion
            to_add_pixel = remaining_distance / dist_per_pixel
            new_y = int(to_add_pixel + sorted_pos[interval][1])

        return [marker_pos_up_down[0][0], new_y]        

def calc_markers(segmenter, path, curr_dir, dest, img_path, show_image=False, return_image=False):
    """ calculates all marker directions and positions """
    next_dir = path.directions[0]
    
    marker_dir_up_down = calc_marker_direction_for_floor(curr_dir, next_dir)

    #marker dir
    marker_dir_left_right = None
    marker_pos_up_down = None
    marker_pos_left_right = None
    json_marker_pos_up_down = []
    json_marker_pos_left_right = None

    if marker_dir_up_down != constants.DOWN_DIR:
        lines, hull_img = get_floor_lines(segmenter, img_path) 
 
        marker_pos_up_down = calculate_markerpos_floor(lines, hull_img)

        dist, next_diff_dir = helper.get_next_different_direction_and_dist_in_meter(path, curr_dir)
        marker_dir_left_right = calc_horizontal_or_vertical_marker_direction(curr_dir, next_diff_dir)
        marker_pos_left_right = calc_horizontal_or_vertical_marker_position(path, dest, curr_dir, lines, marker_pos_up_down, hull_img)
        
        #remove all positions that come after the destination
        marker_pos_up_down = list(filter(lambda pos: pos[1] > (marker_pos_left_right[1] + 30), marker_pos_up_down))
        
        #convert for json format
        for pos in marker_pos_up_down:
            json_marker_pos_up_down.append([pos[0], pos[1]])
        
        if marker_pos_left_right and not marker_pos_left_right[1] is math.inf:
            json_marker_pos_left_right = [int(marker_pos_left_right[0]), int(marker_pos_left_right[1])]

    if show_image or return_image:
        #show image for testing
        img = cv2.imread(img_path) 
        img = cv2.resize(img, (constants.IMG_WIDTH_AR, constants.IMG_HEIGHT_AR))
        diag_marker = (marker_pos_up_down, marker_dir_up_down)
        if marker_dir_up_down == constants.NO_DIR or marker_pos_up_down is None: #TODO bei down show inverted arrow
            diag_marker = None
        if return_image:
            pass
            return show_image_with_marker(horizontal_marker=(marker_pos_left_right, marker_dir_left_right), diagonal_marker=diag_marker, src_img=img, return_image=return_image)

    if len(path.directions) <= 1 :
        return {'dest_reached': True}, 200

    return {'up_down_dir': marker_dir_up_down, 'up_down_pos': json_marker_pos_up_down,
            'left_right_dir': marker_dir_left_right, 'left_right_pos': json_marker_pos_left_right}


