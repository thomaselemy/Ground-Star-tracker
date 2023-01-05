#Implementation of object detection by ROI and tracking by built-in OpenCV trackers

import argparse
import cv2
import numpy as np
from imutils.video import FPS
import imutils
from collections import deque
import sys
import time
#import pyserial
from buttons import create_GUI
import serial

#SerialObj = serial.Serial('COM7', 9600) #open serial port

'''SerialObj.baudrate = 9600  # set Baud rate to 9600
SerialObj.bytesize = 8     # Number of data bits = 8
SerialObj.parity   ='N'    # No parity
SerialObj.stopbits = 1     # Number of Stop bits = 1'''


Px,Ix,Dx=-1/320,0,0
Py,Iy,Dy=-0.2/240,0,0
integral_x,integral_y=0,0
differential_x,differential_y=0,0
prev_x,prev_y=0,0
pixelmovement = 10
# Argument input
#parser= argparse.ArgumentParser() #creating a parser
#parser.add_argument("-v", "--video",required=True, help="path to video")
#parser.add_argument("-t", "--tracker", type=str,
#default="csrt", help="OpenCV tracker type")
#parser.add_argument(, required=True, help="path to output")
#args = vars(parser.parse_args()) #parsing arguments

# Process argument
print("[INFO] Start to process video")
vs = cv2.VideoCapture(0)  # Initialize the video
writer = None
label = " "
fps = None
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.legacy.TrackerCSRT_create,
    "kcf": cv2.legacy.TrackerKCF_create,
    "boosting": cv2.legacy.TrackerBoosting_create,
    "mil": cv2.legacy.TrackerMIL_create,
    "tld": cv2.legacy.TrackerTLD_create,
    "medianflow": cv2.legacy.TrackerMedianFlow_create,
    "mosse": cv2.legacy.TrackerMOSSE_create
}
tracker = OPENCV_OBJECT_TRACKERS["csrt"]()  # Initialize the tracker

box = None
position = deque()
print("[INFO] Initialization")
state = 0

video_frame_rate = vs.get(cv2.CAP_PROP_FPS)  # Obtain video frame rate
create_GUI()
while True:
    (grabbed, frame) = vs.read()  # Loop frame by frame
    if frame is None:  # End if there is no frame left
        break
    # frame=frame[100:900,800:1900] Reshape frame if necessary

    (H, W) = frame.shape[:2]

    """if writer is None:  # Initialize the writer
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(
           (c:path/to/video/vid.mp4), fourcc, video_frame_rate, (W, H), True)"""

    if box is not None:  # If the initial position of object is given, the tracking is handled by tracker automatically
        (success, box) = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            #center of star
            (center_x, center_y) = (x + w // 2, y + h // 2)  # x and y position = star center
            (frame_center_x, frame_center_y) = (W // 2, H // 2)#center of display
            error_x=frame_center_x-center_x
            error_y=frame_center_y-center_y

            integral_x=integral_x+error_x
            integral_y=integral_y+error_y

            differential_x= prev_x+error_x
            differential_y= prev_y=error_y
            #print('center x pos=', center_x)
            #print('center y pos=', center_y)
            print('error x pos=', error_x)

            prev_x=error_x
            prev_y=error_y

            valx=Px*error_x +Dx*differential_x + integral_x
            valy=Px*error_y +Dx*differential_y + integral_y

            valx=round(valx,2)
            valy=round(valy,2)

            nMovementx = error_x / pixelmovement
            nMovementy = error_y / pixelmovement
            #print('pixelerrorx=',error_x,'valx=',valx)
            #print('pixelerrory=',error_y, 'valy=', valy)
            if error_x > 5 and error_x < 20:#if star x pos greater than +5, move camera right
               # text#SerialObj.write(b'R')
                print('print small move right')
                motorCommand = b'R'
            elif error_x >= 20:
                motorCommand = b'r'
                print("big right move")

            elif error_x < -5 and error_x >-20:
                print("small move left")
                motorCommand = b'L'
            elif error_x <= -20:
                print("big left move")
                motorCommand = b'l'
            # YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY direction
            if error_y > 5 and error_y < 20:#if star y pos greater than +5, move camera right
               # text#SerialObj.write(b'A')
                print('print small move right')
            elif error_y >= 20:
                print("big right move")

            elif error_y < -5 and error_y >-20:
                print("small move left")


            '''
             elif error_x < -5 and error_x >-20:
                print("small move left")
                        elif error_x >= 20:
                print("big move")
                
                
            '''



            if error_y > 5:



                if abs(valx) > 0.5: #if star y pos less than t5, move camera left
                    sign = valx / abs(valx)
                    valx = 0.5 * sign
                #print('valuex', valx)
                #ser.setposx(valx)

            #if abs(error_y) < 20:
                #ser.setdcy(0)
                #print('erry <20')
            #else:
                if abs(valy) > 0.5:
                    sign = valy / abs(valy)
                    valy = 0.5 * sign
                #print('valuey',valy)
                #ser.setposy(valy)

                #(offset_x, offset_y) = (frame_center_x - center_x, frame_center_y - center_y)
            #while center_x != frame_center_x and center_y != frame_center_y:  # while we are not centered in the box we defined
                #if center_x: center_y  # if star within


            # Draw a rectangle around the object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            position.appendleft((int(x + w / 2), int(y + h / 2)))
            for i in range(0, len(position)):
                if i + 1 < len(position):
                    # Draw the trajectory
                    cv2.line(frame, position[i], position[i + 1], (255, 0, 0), 2)

        # Count frame rate of tracker
        fps.update()
        fps.stop()

        # Print info in each frame
        info = [("Tracker", "csrt"), ("Success", "Yes" if success else "No"),
                ("FPS:", "{:.2f}".format(fps.fps())), ("Position", position[0])]
        for (i, (k, v)) in enumerate(info):
            text = "{}:{}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Slow down video until the object is chosen
    if state == 1:
        cv2.imshow("Select the area", frame)
        key = cv2.waitKey(1)
    else:
        cv2.imshow("Select the area", frame)
        key = cv2.waitKey(100)

    # Press s to select position of object
    # Press space or enter to select the box
    if key == ord("s"):
        state = 1
        box = cv2.selectROI(
            "Select the area", frame, fromCenter=False, showCrosshair=False)
        tracker.init(frame, box)
        fps = FPS().start()
    elif key == ord("q"):
        break
    elif key == ord("c"):
        box = None
        state = 0
        tracker = OPENCV_OBJECT_TRACKERS["csrt"]()
        position = deque()

    #writer.write(frame)

if writer:
    writer.release()
vs.release()
cv2.destroyAllWindows()
#SerialObj.close()          # Close the port