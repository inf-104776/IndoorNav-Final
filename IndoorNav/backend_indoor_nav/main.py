from ar.helper import get_next_different_direction_and_dist_in_meter
import cv2
from flask import Flask, request
from flask_cors import CORS
from ar.marker_placement import calc_markers
from navigator import Navigator

from training.localization import initial_localization
import ar.constants as constants

import os

app = Flask(__name__)
api = CORS(app)

navigator = Navigator()

def save_images(uploaded_files):
    for uploaded_file in uploaded_files:
        if uploaded_file.filename != '':
            uploaded_file.save("backend_indoor_nav\\training\\cam_captures\\" + uploaded_file.filename)
                        
            img = cv2.imread("backend_indoor_nav\\training\\cam_captures\\" + uploaded_file.filename)
            cv2.imwrite("backend_indoor_nav\\training\\cam_captures\\" + uploaded_file.filename, img)


@app.route('/navigation', methods=['POST'])
def navigation():
    uploaded_files = request.files.getlist('images')
    
    #TODO speichern sparen
    save_images(uploaded_files)
    res = navigator.do_navigation(False, navigator.destination)
    return res, 201

@app.route('/ar', methods=['POST'])
def ar():
    print("ar request received")
    img_path = constants.DIR_CAM_CAPTURES + '\\0.jpg'
    markers = calc_markers(navigator.segmenter, navigator.current_path, int(navigator.current_pos[-1:]), navigator.destination, img_path)
    return markers, 201

@app.route('/initial_navigation', methods=['POST'])
def initial_navigation():
    print("initial_navigation request received")
    uploaded_files = request.files.getlist('images')
    navigator.destination = request.form.get('destination') 

    #TODO speichern sparen
    save_images(uploaded_files)

    location = initial_localization(navigator.localizer)
    navigator.current_pos = location

    
    return navigator.do_navigation(True, navigator.destination, uploaded_files), 201


if __name__ == '__main__':
    # initialize navigator module
    navigator.init_localizer()
    navigator.init_segmenter()
    
    app.run()
