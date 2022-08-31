from ar.segmenter import create_segmentation_image, visualize_result
import cv2
from navigator import Navigator 
import numpy as np
import ar.marker_placement as mp
import wayfinding.wayfinding as wf

#creates a video with image segmentation at every frame
def create_segmentation_video(video_path, segmenter):
    cap = cv2.VideoCapture(video_path)
    success, img = cap.read()
    images = []
    framesize = (270 * 2, 480)
    i = 0
    while success:
        img = cv2.resize(img, (270, 480))
        cv2.imwrite("backend_indoor_nav\\tests\\test_videos\\temp.jpg", img)
        seg_pred = create_segmentation_image(segmenter, "backend_indoor_nav\\tests\\test_videos\\temp.jpg", None)
        seg_img = visualize_result(np.array(seg_pred), img=np.array(img), return_image=True )
        images.append(np.array(seg_img))
        # read next frame
        success, img = cap.read()
        i += 1
    out = cv2.VideoWriter('output_video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, framesize)

    for img in images:
        out.write(img)
    out.release()

#creates a video with ar markers  and faked positions.
def create_armarker_video(video_path, navigator):
    cap = cv2.VideoCapture(video_path)
    success, img = cap.read()
    framesize = (270, 480)
    i = 0
    
    temp_path = "backend_indoor_nav\\tests\\test_videos\\temp.jpg"
    i = 0 
    navigator.current_pos = "D0022"
    navigator.current_path = wf.find_path("D002", 'D0.04')
    navigator.destination = 'D0.04'
    out = cv2.VideoWriter('ar_markers.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, framesize)

    while success:
        img = cv2.resize(img, (270, 480))
        cv2.imwrite(temp_path, img)
        #find position 
        pos = navigator.do_navigation(False, navigator.destination, temp_path)
        
        if pos == {"navigation_error": "Navigation konnte nicht durchgeführt werden"}:
            pos = navigator.current_pos
        
        elif 'pos_dir' in pos:
            print("pos: " + pos['pos_dir'])
            navigator.current_pos = pos['pos_dir']
        #find path
        marker = mp.calc_markers(navigator.segmenter, navigator.current_path, int(navigator.current_pos[-1:][0]), navigator.destination, temp_path, False, False) 
        marker_img = mp.show_image_with_marker(diagonal_marker=(marker['up_down_pos'], marker['up_down_dir']), horizontal_marker=(marker['left_right_pos'], marker['left_right_dir']), src_img=img, return_image=True)
        out.write(marker_img)
        # read next frame
        success, img = cap.read()
        i += 1
    out.release()

#fake position for video D0
def fake_pos_for_D0(frame_num):
    #video_path = "backend_indoor_nav\\tests\\test_videos\\20220802_151731.mp4"
    sec = get_second_for_frame_num(frame_num)
    if sec == 0:
        return 'D0183'
    elif sec == 1 or sec == 2:
        return 'D0173'
    elif sec == 3 or sec == 4:
        return 'D0094'
    elif sec == 5 or sec == 6:
        return 'D0084'
    elif sec == 7 or sec == 8 or sec == 9:
        return 'D0074'
    elif sec == 10 or sec == 11:
        return 'D0064'
    else:
        return 'D0054'

#fake position for video BA   
def fake_pos_for_B2A(frame_num):
    #video_path = "backend_indoor_nav\\tests\\test_videos\\B2A.mp4"
    if frame_num >= 0 and frame_num <= 30:
        return 'B0063'
    elif frame_num > 30 and frame_num <= 60:
        return 'B0053'
    elif frame_num > 60 and frame_num <= 150:
        return 'B0043'
    elif frame_num > 150 and frame_num <= 180:
        return 'B0033'
    elif frame_num > 180 and frame_num <= 240:
        return 'B0023'
    elif frame_num > 240 and frame_num <= 330:
        return 'B0013'
    elif frame_num > 330 and frame_num <= 420:
        return 'B0003'
    elif frame_num > 420 and frame_num <= 630:
        return 'A0012'
    elif frame_num > 630 and frame_num <= 750:
        return 'A0022'
    elif frame_num > 750 and frame_num <= 780:
        return 'A0032'
    elif frame_num > 780 and frame_num <= 810:
        return 'A0042'
    elif frame_num > 810 and frame_num <= 900:
        return 'A0052'
    elif frame_num > 900 and frame_num <= 1020:
        return 'A0062'
    elif frame_num > 1020 and frame_num <= 1050:
        return 'A0072'
    elif frame_num > 1050 and frame_num <= 1120:
        return 'A0082'
    elif frame_num > 1120 and frame_num <= 1180:
        return 'A0092'
    else:
        return 'A0102'

#fake position for video A0
def fake_pos_for_A0(frame_num):
    sec = get_second_for_frame_num(frame_num)
    if sec == 0 or sec == 1:
        return 'A0022'
    if sec == 2 or sec == 3:
        return 'A0032'
    if sec == 4 or sec == 5:
        return 'A0042'
    if sec == 6 or sec == 7:
        return 'A0052'
    if sec == 8 or sec == 9:
        return 'A0062'
    if sec == 10 or sec == 11 or sec == 12:
        return 'A0072'
    if sec == 13 or sec == 14:
        return 'A0082'
    if sec == 15 or sec == 16:
        return 'A0092'
    if sec == 17:
        return 'A0102'

#fake position for video FA
def fake_pos_for_FA(frame_num):
    #video_path = "backend_indoor_nav\\tests\\test_videos\\B2A.mp4"
    sec = get_second_for_frame_num(frame_num)
    if sec == 0:
        return 'F0043'
    elif sec == 1:
        return 'F0053'
    elif sec == 2:
        return 'F0063'
    elif sec == 3:
        return 'F0073'
    elif sec == 4:
        return 'F0083'
    elif sec >= 5 and sec < 7:
        return 'F0093'
    elif sec == 7:
        return 'F0103'
    elif sec >= 8 and sec < 11:
        return 'F0113'
    elif sec >= 11 and sec < 13:
        return 'F0123'
    elif sec >= 13 and sec < 15:
        return 'F0133'
    elif sec >= 15 and sec < 17:
        return 'F0143'
    elif sec == 17:
        return 'F0153'
    elif sec >= 17 and sec < 20:
        return 'F0163'
    elif sec == 20:
        return 'F0174'
    elif sec >= 21 and sec < 25:
        return 'A0114'
    elif sec >= 25 and sec < 30:
        return 'A0104'
    elif sec >= 30 and sec < 32:
        return 'A0094'
    elif sec >= 32 and sec < 35:
        return 'A0084'
    elif sec >= 35 and sec < 37:
        return 'A0074'
    elif sec >= 37 and sec < 39:
        return 'A0064'
    elif sec >= 39 and sec < 42:
        return 'A0054'
    elif sec >= 42 and sec < 44:
        return 'A0044'
    elif sec == 44:
        return 'A0034'
    elif sec >= 45 and sec < 48:
        return 'A0024'
    elif sec >= 48 and sec < 52:
        return 'A0011'
    elif sec >= 52 and sec < 54:
        return 'A1S001'
    elif sec >= 54 and sec < 60:
        return 'A1S003'
    elif sec >= 60 and sec < 62:
        return 'A1013'
    elif sec >= 62 and sec < 66:
        return 'A1014'
    elif sec >= 66 and sec < 69:
        return 'A1011'
    elif sec >= 69 and sec < 77:
        return 'A2S003'
    elif sec >= 77 and sec < 83:
        return 'A2012'
    elif sec >= 83 and sec < 96:
        return 'A2022'
    elif sec >= 96 and sec < 99:
        return 'A2032'
    elif sec >= 99 and sec < 101:
        return 'A2042'
    elif sec >= 101 and sec < 103:
        return 'A2052'
    elif sec >= 103 and sec < 106:
        return 'A2062'
    elif sec >= 106 and sec < 109:
        return 'A2072'
    else:
        return 'A2082'


#creates a video with ar markers  and faked positions.
# fake_pos is a callback used to manually determine the position
def create_armarker_video_with_faked_positioning(video_path, navigator, fake_pos):
    cap = cv2.VideoCapture(video_path)
    success, img = cap.read()
    framesize = (270, 480)
    i = 0
    out = cv2.VideoWriter('ar_markers_fake.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, framesize)
    temp_path = "backend_indoor_nav\\tests\\test_videos\\temp.jpg"
    i = 0 

    pos = fake_pos(i)
    img = cv2.resize(img, framesize)
    cv2.imwrite(temp_path, img)
    #find path
    dest = "A0.13"
    path = wf.find_path(pos[:-1], dest)
    marker = mp.calc_markers(navigator.segmenter, path, int(pos[-1:][0]), dest, temp_path, False, False)
    while success:
        img = cv2.resize(img, framesize)
        cv2.imwrite(temp_path, img)
        pos = fake_pos(i)
        
        #find path
        dest = "A0.13"
        path = wf.find_path(pos[:-1], dest)
        
        if i % 15 == 0:
            marker = mp.calc_markers(navigator.segmenter, path, int(pos[-1:][0]), dest, temp_path, False, False)
        if not marker == ({'dest_reached': True}, 200):
            marker_img = mp.show_image_with_marker(diagonal_marker=(marker['up_down_pos'], marker['up_down_dir']), horizontal_marker=(marker['left_right_pos'], marker['left_right_dir']), src_img=img, return_image=True)
            out.write(marker_img)
            # read next frame
        success, img = cap.read()
        print("Img created " + str(i))
        i += 1
    out.release()

def get_second_for_frame_num(frame_idx):
    fps = 30
    sec = int(frame_idx / fps)
    return sec

# writes positions down into a textfile to validate how many positions 
# are right. The evaluation is a manual process
# (difference of positions is 2 maximum)
def write_positions(video_path, navigator, get_fake_pos):
    cap = cv2.VideoCapture(video_path)
    success, img = cap.read()
    temp_path = "backend_indoor_nav\\tests\\test_videos\\temp.jpg"
    navigator.current_pos = "D0183"
    navigator.current_path = wf.find_path("D0183", 'A0.13')
    navigator.destination = 'A0.13'
    i = 0
    equal_pos = 0
    none_counter = 0
    res = ""
    with open('positions.txt', 'a') as the_file:
      the_file.truncate()
      the_file.write( 'model | actual\n')
      while success:
        img = cv2.resize(img, (180, 320))
        cv2.imwrite(temp_path, img)
        pos = navigator.do_navigation(False, navigator.destination, temp_path)
        actual_pos = get_fake_pos(i)

        
        if 'pos_dir' in pos:
            if pos.get('pos_dir') == actual_pos:
                equal_pos += 1 
            #toadd = pos.get('pos_dir')  + ' | ' + actual_pos  + ' | ' + str(pos.get('possibility')) +'\n'
            #res += toadd
            the_file.write(pos.get('pos_dir')  + ' | ' + actual_pos  + ' | ' + str(pos.get('possibility')) +'\n')
        else:
            none_counter += 1
            #res += 'None\n'
            the_file.write('None\n')
        i += 1
        # read next frame
        success, img = cap.read()
      #the_file.write(res)    
    print(str(equal_pos) + "/" + str(i) + '\n')
    print(str(none_counter) + "/" + str(i) + '\n')

    the_file.close()

#initialize navigator and call desired function
navigator = Navigator()
navigator.init_segmenter()
navigator.init_localizer()
video_path = "backend_indoor_nav\\tests\\test_videos\\F.mp4"
create_armarker_video_with_faked_positioning(video_path, navigator, fake_pos_for_FA)

