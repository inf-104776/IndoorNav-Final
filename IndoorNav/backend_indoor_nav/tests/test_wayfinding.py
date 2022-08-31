import math
import unittest

import wayfinding.wayfinding as wf

from wayfinding.rooms import get_nodes, get_rooms

class TestWayfinding(unittest.TestCase):
    ''' Tests the wayfinding module'''

    def is_path_equal(self, path, path_exp):
        '''tests that the given path and the expected path are identical '''
        self.assertEqual(len(path.get_nodes()), len(path_exp.get_nodes()))
        self.assertEqual(len(path.get_directions()), len(path_exp.get_directions()))

        for i in range(len(path.get_nodes())):
            self.assertEqual(path.get_nodes()[i].name, path_exp.get_nodes()[i])

        for i in range(len(path.get_directions())):
            self.assertEqual(path.get_directions()[i], path_exp.get_directions()[i])

    def test_way_within_a0(self):
        ''' tests a way from A000 to A0.08 within one hallway'''
        start_node = 'A000'
        dest_node = 'A0.08'
        p = wf.find_path(start_node, dest_node)
        p_exp_nodes = ['A000', 'A001', 'A002', 'A003', 'A004', 'A005', 'A0.08']
        p_exp_dir = [2, 2, 2, 2, 2, 1]
        p_exp = wf.Path(p_exp_nodes, p_exp_dir)
        self.is_path_equal(p, p_exp)

    def test_way_between_a0_and_a1(self):
        ''' tests the correct usage when changing floor'''
        start_node = 'A000'
        dest_node = 'A1.03'
        p = wf.find_path(start_node, dest_node)
        p_exp_nodes = ['A000', 'A001', 'A1S00', 'A101', 'A102', 'A1.03']
        p_exp_dir = [2, 1, 3, 2, 1]
        p_exp = wf.Path(p_exp_nodes, p_exp_dir)
        self.is_path_equal(p, p_exp)

    def test_all_rooms_are_reachable_from_every_node(self):
        ''' tests if all rooms can be reach from an node. Long runtime'''
        rooms = get_rooms()
        nodes = get_nodes()

        for start_node in nodes:
            for room in rooms:
                path = wf.find_path(start_node.name, room.name)
                self.assertIsNotNone(path)

    def test_distance_to_end_of_hallway(self):
        ''' tests the distance to the end of the hallway'''
        start_node = 'A203'
        looking_dir = '2'

        self.assertEqual(wf.calc_distance_to_end_of_hallway(start_node, looking_dir), 7)

    def test_distance_to_end_of_hallway(self):
        ''' tests the distance to the end of the hallway'''
        start_node = 'A203'
        looking_dir = '2'

        self.assertEqual(wf.calc_distance_to_end_of_hallway(start_node, looking_dir), 7)
    
    def test_distance_to_end_of_hallway_to_be_0(self):
        ''' tests the distance to the end of the hallway'''
        start_node = 'A210'
        looking_dir = '2'

        self.assertEqual(wf.calc_distance_to_end_of_hallway(start_node, looking_dir), 0)

    def test_distance_to_end_of_hallway_at_corner(self):
        ''' tests the distance to the end of the hallway'''
        start_node = 'D108'
        looking_dir = '2'

        self.assertEqual(wf.calc_distance_to_end_of_hallway(start_node, looking_dir), 0)

    def test_distance_to_visible_door(self):
        ''' tests the distance to the door '''
        start_node = 'A203'
        looking_dir = '2'
        room_name = 'A2.06'

        self.assertEqual(wf.calc_distance_to_door_if_visible(start_node, room_name, 
                        looking_dir), 4)

    def test_distance_to_not_visible_door(self):
        ''' tests the distance to the door '''
        start_node = 'A203'
        looking_dir = '2'
        room_name = 'A2.03'

        self.assertEqual(wf.calc_distance_to_door_if_visible(start_node, room_name, 
                        looking_dir), math.inf)

    def test_distance_to_visible_door_next_to_another_door(self):
        ''' tests the distance to the door '''
        start_node = 'A003'
        looking_dir = '2'
        room_name = 'A0.12'

        self.assertEqual(wf.calc_distance_to_door_if_visible(start_node, room_name, 
                        looking_dir), 7)

    def test_floor_switch_up(self):
        ''' tests if the user has to walk up the stairs'''
        path = wf.find_path('B002', 'A1.03')

        self.assertEqual(wf.calc_stairs_up_or_down(path), 'stairs_up')

    def test_floor_switch_up(self):
        ''' tests if the user has to walk up the stairs'''
        path = wf.find_path('A103', 'A0.06')

        self.assertEqual(wf.calc_stairs_up_or_down(path), 'stairs_down')    

if __name__ == '__main__':
    unittest.main()
    