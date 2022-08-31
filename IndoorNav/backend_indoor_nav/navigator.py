from ar import constants
from ar.helper import get_next_different_direction_and_dist_in_meter
from ar.segmenter import create_model
from tensorflow import keras

from ar.marker_placement import calc_horizontal_or_vertical_marker_direction


from training.localization import SRC_TEST_IMG, initial_localization, normal_localization
from wayfinding.wayfinding import find_path, calc_stairs_up_or_down

class Navigator:

    segmenter = None
    localizer = None
    current_path = None
    current_pos = None
    destination = None
    
    def init_segmenter(self):
        self.segmenter = create_model() 

    def init_localizer(self):
        self.localizer = keras.models.load_model('backend_indoor_nav\\training\\models320')

    def check_validity_of_position(self, current_pos, last_pos):
        """valid, when the position is realistically reached by foot (max 2 skipped positions)"""
        max_dist = 3
        path = find_path(last_pos, current_pos)
        return len(path.directions) <= max_dist 

    def do_navigation(self, is_init_loc, destination, img_path = SRC_TEST_IMG):
        is_valid = True
        path = []
        nodes = []
        if is_init_loc:
            pos_dir = initial_localization(self.localizer)
            possibility = 0.0
        else: 
            pos_dir, possibility = normal_localization(self.localizer, img_path)
            if pos_dir:
                is_valid = self.check_validity_of_position(pos_dir[:-1], self.current_pos[:-1])

        #take last known position
        if pos_dir is None or not is_valid:
            pos_dir = self.current_pos

        #pathfinding
        path = find_path(pos_dir[:-1], destination)
        (dist, dir) = get_next_different_direction_and_dist_in_meter(path, pos_dir[-1:] )
        dir_next_turn = calc_horizontal_or_vertical_marker_direction(int(pos_dir[-1:]), dir)
        if dir_next_turn is constants.NO_DIR:
            dir_next_turn = calc_stairs_up_or_down(path)
        
        #node names for conversion to json
        for node in path.nodes:
            nodes.append(node.name)

        if len(path.directions) <= 1 :
            return {'dest_reached': True}
        
        current_path = path
        dist2goal = len(path.directions) * constants.LENGTH_PER_UNIT
        self.current_pos = pos_dir
        self.current_path = current_path
        
        return {'directions': path.directions, 'positions': nodes, 'dist_next_turn': dist, 'dir_next_turn': dir_next_turn, 'pos_dir': pos_dir, 'dist2goal': dist2goal, 'possibility': float(possibility)}
