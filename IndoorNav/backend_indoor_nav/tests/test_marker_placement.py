import unittest
from ar.constants import DIR_TEST_IMAGES
import ar.helper as helper
from navigator import Navigator
import wayfinding.wayfinding as wf
import ar.marker_placement as mp
from cv2 import cv2

import time
class TestMarkerPlacement(unittest.TestCase):
    
    def test_calc_markers_turn_left(self):
        navigator = Navigator()
        navigator.init_segmenter()
        path = wf.find_path("A202", "A2.06") #Turn left after a couple meters
        curr_dir = 2
        dest = "A2.06"
        img_path = "backend_indoor_nav\\tests\\test_images\\A2022.jpg"
        res = mp.calc_markers(navigator.segmenter, path, curr_dir, dest, img_path, True, True)
        cv2.imshow("res", res)
        cv2.waitKey(0)

    def test_calc_markers_turn_left2(self):
        navigator = Navigator()
        navigator.init_segmenter()
        path = wf.find_path("A109", "D008") #User should turn around #TODO draw
        curr_dir = 4
        dest = "D008"
        img_path = DIR_TEST_IMAGES + "\\0.jpg" 
        mp.calc_markers(navigator.segmenter, path, curr_dir, dest, img_path, True, True)
       

    def test_calc_markers_turn_right(self):
        navigator = Navigator()
        navigator.init_segmenter()
        path = wf.find_path("A202", "A2.10") #Turn right after at nearly end of hallway
        curr_dir = 2
        dest = "A2.10"
        img_path = "backend_indoor_nav\\tests\\test_images\\A2022.jpg" 
        res = mp.calc_markers(navigator.segmenter, path, curr_dir, dest, img_path, True, True)
        cv2.imshow("res", res)
        cv2.waitKey(0)

if __name__ == '__main__':
    unittest.main()