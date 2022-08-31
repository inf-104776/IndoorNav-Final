import unittest
import ar.helper as helper
import wayfinding.wayfinding as wf


class TestARHelper(unittest.TestCase):
    ''' Tests the AR helper module'''

    def test(self):
        exp = [[30, 310, 180, 307]]
        lines = [[[30, 310, 180, 307], [200, 200, 400, 200], [10, 15, 270, 305], 
                [20, 250, 75, 380], [20, 380, 50, 380]]]
        y_height = 300

        self.assertEqual(helper.find_lines_near_given_height(lines, y_height), exp)

    def test_find_point_of_given_y_value(self):
        lines = [[[30, 300, 180, 307], [200, 200, 400, 200], [10, 15, 270, 305], 
                [20, 250, 75, 380], [20, 380, 50, 380]]]
        y_height = 300
        self.assertEqual(helper.find_point_from_given_y_value(lines, y_height), (30, 300))

    def test_get_next_dif_and_dist(self):
        path = wf.find_path('B003', 'A0.08')
        current_dir = '3'
        exp = (4 * 2.5, 2)
        self.assertEqual(helper.get_next_different_direction_and_dist_in_meter(path, current_dir), exp)

    def test_calc_line_intersection(self):
        A = [200, -200]
        B = [100, -400]
        C = [400, -200]
        D = [500, -400]

        self.assertEqual(helper.line_intersection(A, B, C, D), (300.0, 0.0))

    def test_dest_in_current_hallway_and_visible(self):
        dest = 'A2.06'
        path = wf.find_path('A202', dest)
        current_dir = 2
        self.assertEqual(helper.dest_in_hallway(path, dest, current_dir), True)
    
    def test_dest_in_current_hallway_and_not_visible(self):
        dest = 'A2.06'
        path = wf.find_path('A202', dest)
        current_dir = 4
        self.assertEqual(helper.dest_in_hallway(path, dest, current_dir), False)
    
    def test_dest_not_in_current_hallway(self):
        dest = 'A0.08'
        path = wf.find_path('A202', dest)
        current_dir = 2
        self.assertEqual(helper.dest_in_hallway(path, dest, current_dir), False)

    def test_get_right_neighbor(self):
        dest = 'D0.02'
        path = wf.find_path('D005', dest)
        current_dir = 4
        self.assertEqual(helper.get_right_neighbor_dir(current_dir), 1)
        
        

if __name__ == '__main__':
    unittest.main()