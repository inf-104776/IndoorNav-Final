import math
from ar.constants import DIR_1, DIR_4, LENGTH_PER_UNIT
from ar.constants import HORIZONTAL_ANGLE_180, HORIZONTAL_ANGLE_MIN180

""" This module contains helper functions for AR calculations """

def find_min_y(lines):
    min_y = math.inf
    if not lines is None:
        for line in lines:
            line = line[0]
            if line[1] < min_y:
                min_y = line[1]
            if line[3] < min_y:
                min_y = line[3]
    return min_y

def find_min_x(lines):
    min_x = math.inf
    if not lines is None:
        for line in lines:
            if line[0] < min_x:
                min_x = line[0]
            if line[2] < min_x:
                min_x = line[2]
    return min_x

def find_max_x(lines):
    '''finds the max x value of all given lines'''
    max_x = -math.inf
    if not lines is None:
        for line in lines:
            if line[0] > max_x:
                max_x = line[0]
            if line[2] > max_x:
                max_x = line[2]
    return max_x

def len_of_line(line):
    '''cals the length of the given line'''
    if line: 
        return math.sqrt(((line[2] - line[0]) ** 2) + ((line[3] - line[1])** 2) )
    else:
        math.inf

def dist_of_points(x_1, y_1, x_2, y_2):
    ''' calculates the distance between the given points'''
    return len_of_line((x_1, y_1, x_2, y_2))

def get_left_neighbor_dir(curr_dir):
    ''' gets the left neighbor'''
    res = int(curr_dir) - 1
    return str(res) if res > 0 else DIR_4

def get_right_neighbor_dir(curr_dir):
    ''' gets the right neighbor'''
    res = int(curr_dir) + 1
    return str(res) if res <= int(DIR_4) else DIR_1

def get_inverse_direction(dir):
    '''Returns the inverse direction of the given direction'''
    if dir == 1: return 3 
    if dir == 3: return 1 
    if dir == 2: return 4 
    if dir == 4: return 2 

def find_lines_near_given_height(lines, y_height):
    '''Finds lines that mark the end of the floor'''
    found_lines = []
    threshold = 30
    if not lines is None:
        for line in lines:
            line = line[0]
            if (line[1] < y_height + threshold) and (line[3] < y_height + threshold):
                found_lines.append(line)
    return found_lines

def find_point_from_given_y_value(lines, y_height):
    """ finds the point belonging to the given y_height
    This is used for when the convex hull of the hallway has
    a cone shape
    """
    if not lines is None:
        for line in lines:
            line = line[0]
            if line[1] == y_height:
                return line[0], line[1]
            if line[3] == y_height:
                return line[2], line[3]
    return None

def get_next_different_direction_and_dist_in_meter(path, current_dir):
    ''' Gets the first direction in path that is not the current looking direction of user'''
    dir_idx = 0
        #find next direction
    while(dir_idx < len(path.directions) and path.directions[dir_idx] == int(current_dir)):
        dir_idx +=1
    direction = path.directions[dir_idx]
    dist = LENGTH_PER_UNIT * (dir_idx)

    return dist, direction

def calc_angle(x1, y1, x2, y2):
    return math.degrees(math.atan2(y2-y1, x2-x1)) 

def is_approx_angle(angle, angle_to_test, angle_range):
    ''' checks if a given angle matches approx. an angle that is useful to detect'''
    if angle_to_test == HORIZONTAL_ANGLE_180 or angle_to_test == HORIZONTAL_ANGLE_MIN180: #180 == -180
        #between -175 and -180
        is_higher_than_lower_range = angle < HORIZONTAL_ANGLE_MIN180 - (angle_range/2) and angle >= HORIZONTAL_ANGLE_MIN180
        #between 175 and 180
        is_lower_than_higher_range = angle > HORIZONTAL_ANGLE_180 - (angle_range/2) and angle <= HORIZONTAL_ANGLE_180
        return is_higher_than_lower_range or is_lower_than_higher_range

    return angle > (angle_to_test - (angle_range / 2.0)) and angle < (angle_to_test + (angle_range / 2.0))

def build_line_equation_from_two_points(p1, p2):
    """ Line p1p2 represented as ax + by = c"""
    a = p2[1] - p1[1]
    b = p1[0] - p2[0]
    return a, b

def line_intersection(A, B, C, D):
    """ Calculates the intersection of line AB und CD"""
   # Line AB represented as a1x + b1y = c1
    a1 = B[1] - A[1]
    b1 = A[0] - B[0]
    c1 = a1*(A[0]) + b1*(A[1])
 
    # Line CD represented as a2x + b2y = c2
    a2 = D[1] - C[1]
    b2 = C[0] - D[0]
    c2 = a2*(C[0]) + b2*(C[1])
 
    determinant = a1*b2 - a2*b1
 
    if (determinant == 0):
        raise Exception("No intersection found. The vanishing point could not be calculated")
    else:
        x = (b2*c1 - b1*c2)/determinant
        y = (a1*c2 - a2*c1)/determinant
        return (x, y)

def dest_in_hallway(path, dest, current_dir):
    ''' calculates if the destination is already visible
    since there are corners in some hallways one  cannot just check 
    if its the same hallway. Instead when the direction changes, 
    check if the next location is the destination'''
    for dir_idx in range(len(path.directions)):
        if path.directions[dir_idx] != current_dir:
            return path.nodes[dir_idx + 1].name == dest
    return False

