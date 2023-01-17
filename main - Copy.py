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
#from buttons import create_GUI
import serial
from serial.tools import list_ports

import simple_pid
from tkinter import NW, Tk, Canvas, PhotoImage, Button


def photo_image(img):
    h, w = img.shape[:2]
    data = f'P6 {w} {h} 255 '.encode() + img[..., ::-1].tobytes()
    return PhotoImage(width=w, height=h, data=data, format='PPM')


def serial_ports():
    return [p.device for p in list_ports.comports()]


# when the user selects one serial port from the combobox, this function will execute
def on_select(event=None):
    
    COMPort = cb.get()
    string_separator = "-"
    COMPort = COMPort.split(string_separator, 1)[0]  # remove everything after '-' character
    #COMPort = COMPort[:-1]  # remove last character of the string (which is a space)
    SerialObj = serial.Serial(port=COMPort, baudrate=9600, timeout=0)
    # readSerial() #start reading shit. DELETE. later to be placed in a button
    # get selection from event
    # print("event.widget:", event.widget.get())
    # or get selection directly from combobox
    print("opened port")

    print(COMPort)
    return SerialObj


##############################################################################
#SerialObj = serial.Serial('COM9', 9600) #open serial port

comPort_tk = Tk()
cb = tkinter.ttk.Combobox(comPort_tk, values=serial_ports())
cb.pack()
# assign function to combobox
cb.bind('<<ComboboxSelected>>', on_select)
comPort_tk.mainloop()

#serial_object = serial.Serial('/dev/tty' + str(port), baud)
top = Tk()

top.geometry("200x200")
                                  # ttyUSBx format on Linux


def left():
        SerialObj.write(b'L')      #transmit 'A'
        print('Left')

def right():
        SerialObj.write(b'R')      #transmit 'A'
        print('Right')

def up():
        SerialObj.write(b'U')      #transmit 'up'
        print("Up")
                #time.sleep(1)
def down():
        SerialObj.write(b'D')      #transmit 'A'
        print('Down')

def focusfwd():
        SerialObj.write(b'F')  # transmit 'A'
        print('Fword')

def focusbwd():
        for _ in range(focusbwd()):
                SerialObj.write(b'B')  # transmit 'A'
                print('backwrd')

b1 = Button(top, text="LEFT", command=left, activeforeground="red", activebackground="pink", pady=10)

b2 = Button(top, text="RIGHT", command=right, activeforeground="blue", activebackground="pink", pady=10)

b3 = Button(top, text=" UP ",  command=up, activeforeground="green", activebackground="pink", pady=10, padx = 10)

b4 = Button(top, text="DOWN", command=down, activeforeground="yellow", activebackground="pink", pady=10)

b5 = Button(top, text = "focus Bwd", command=focusbwd, activeforeground = "yellow",activebackground = "pink",pady = 10)

b6 = Button(top, text = "focus Fwd", command=focusfwd, activeforeground = "yellow",activebackground = "pink",pady = 10)

b1.pack(side= 'left')

b2.pack(side = 'right')

b3.pack(side= 'top')

b4.pack(side= 'bottom')

b5.place(x=0, y=140)

# Set the position of button to coordinate (100, 20)
b6.place(x=130, y=140)

#############################################################################

if __name__ == '__main__':



    Px,Ix,Dx=-1/320,0,0

    Py,Iy,Dy=-0.2/240,0,0

    integral_x,integral_y=0,0

    differential_x,differential_y=0,0

    prev_x,prev_y=0,0

    pixelmovement = 10

    # Process argument
    print("[INFO] Start to process video")
    vs = cv2.VideoCapture(0)  # Initialize the video

    ## Turn off auto exposure
    vs.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    # set exposure time
    vs.set(cv2.CAP_PROP_EXPOSURE, 0)
    trackrType = "csrt"
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
    tracker = OPENCV_OBJECT_TRACKERS[trackrType]()  # Initialize the tracker

    #root = Tk()
    #root.title("Video")
    #canvas = Canvas(root, width=1200, height=700)
    #canvas.pack()


    box = None
    position = deque()
    print("[INFO] Initialization")
    state = 0
    tstart = None
    tstart2 = None
    elapsed_duration = 0
    elapsed_duration2 = 0
    video_frame_rate = vs.get(cv2.CAP_PROP_FPS)  # Obtain video frame rate
    #create_GUI()
    while True:
        (grabbed, frame) = vs.read()  # Loop frame by frame

        if frame is None:  # End if there is no frame left
            break
        # frame=frame[100:900,800:1900] Reshape frame if necessary

        (H, W) = frame.shape[:2]





        #root.after(15, update)

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



                nMovementx = error_x / pixelmovement
                nMovementy = error_y / pixelmovement
                #print('pixelerrorx=',error_x,'valx=',valx)
                #print('pixelerrory=',error_y, 'valy=', valy)
                #right movment
                if 5 < error_x < 20:  # if star x pos greater than +5 and less than 20, move camera slowly right
                    # text#SerialObj.write(b'R')
                    #print('print small move right')
                    horz_motorCommand = b'r' # r is 2500 steps right
                elif error_x >= 20:
                    #print("small move left")
                    horz_motorCommand = b'k' #k was added as 1000 steps right
                #left movment
                elif -5 > error_x > -20:
                    #print("small move left")
                    motorCommand = b'l'
                    horz_motorCommand = b'l'
                elif error_x <= -20:
                    motorCommand = b'k'
                    horz_motorCommand = b'k'#k was added as 1000 steps right
                else:
                    horz_motorCommand = None  # dont need to move camera

                    # check if horizontal correction necessary
                if horz_motorCommand:
                    # check if motor command is small movement
                    if horz_motorCommand.isupper():
                        deltaX = 5  # THOMAS NEED TO DETERMINE THIS NUMBER
                        move_duration = 0.1  # seconds. THOMAS NEED TO DETERMINE THIS
                    else:
                        deltaX = 60  # THOMAS NEED TO DETERMINE THIS NUMBER BIG MOVEMENTS
                        move_duration = 0.2  # seconds. THOMAS NEED TO DETERMINE THIS
                    if tstart:
                        elapsed_duration = time.time() - tstart
                    # compute number of commands that need to be sent to motor
                    nHorizontal_moves = round(abs(error_x) / deltaX)
                    print(f"N moves: {nHorizontal_moves}")
                    if elapsed_duration > 5: #nHorizontal_moves * move_duration:
                        tstart = None
                    if not tstart:

                        tstart = time.time()
                        # send movement commands to motor
                        for _ in range(nHorizontal_moves):
                                SerialObj.write(horz_motorCommand)
                                #print("move right/left")

                #  yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy movement

                if 5 < error_x < 20:  # if star y pos greater than +5 and less than 20, move camera down
                    #print('print small down')# needs to move up??
                    vert_motorCommand = b'u' #2500 steps up
                elif error_y >= 20:# if star y pos greater than +5 and less than 20, move camera down
                    print("small move up")
                    vert_motorCommand = b'i' #smallest up movment 1000 steps in 1us x 1000steps
                #down movment
                elif -5 > error_y > -20:
                    #print("small move down")
                    motorCommand = b'd' #2500 steps down
                    horz_motorCommand = b'd'
                elif error_y <= -20:
                    motorCommand = b'c'
                    horz_motorCommand = b'c'#c was added as 1000 steps down

                else:
                    vert_motorCommand = None  # dont need to move camera

                    # check if vertical correction necessary
                if vert_motorCommand:
                    # check if motor command is small movment
                    if vert_motorCommand.isupper():
                        deltaY = 50  # THOMAS NEED TO DETERMINE THIS NUMBER
                        move_duration2 = 0.1  # seconds. THOMAS NEED TO DETERMINE THIS
                    else:
                        deltaY = 60  # THOMAS NEED TO DETERMINE THIS NUMBER BIG MOVEMENTS
                        move_duration2 = 0.2  # seconds. THOMAS NEED TO DETERMINE THIS
                    if tstart2:
                        elapsed_duration2 = time.time() - tstart2
                    # compute number of commands that need to be sent to motor
                    nVertical_moves = round(abs(error_y) / deltaY)
                    if elapsed_duration2 > 5: #nVertical_moves * move_duration2:
                        tstart2 = None
                    if not tstart2:

                        tstart2 = time.time()
                        # send movement commands to motor
                        for _ in range(nVertical_moves):
                            SerialObj.write(vert_motorCommand )
                            print("move up/down")


                print(error_x, error_y)
                print(center_x, center_y)
                # Draw a rectangle around the object
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                position.appendleft((int(x + w / 2), int(y + h / 2)))
                for i in range(0, len(position)):
                    if i + 1 < len(position):
                        #print()
                        # Draw the trajectory
                        cv2.line(frame, position[i], position[i + 1], (255, 0, 0), 2)

            # Count frame rate of tracker
            fps.update()
            fps.stop()

            # Print info in each frame
            info = [("Tracker", trackrType), ("Success", "Yes" if success else "No"),
                    ("FPS:", "{:.2f}".format(fps.fps())), ("Position", position[0])]
            for (i, (k, v)) in enumerate(info):
                text = "{}:{}".format(k, v)
                cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


        '''if grabbed:
            photo = photo_image(frame)
            canvas.create_image(0, 0, image=photo, anchor=NW)
            canvas.image = photo
            if box is not None:

                canvas.create_rectangle(x, y, x + w, y + h, fill="blue", stipple="gray12")'''


        top.update_idletasks()
        top.update()

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
            time.sleep(1)
            tracker.init(frame, box)
            fps = FPS().start()
        elif key == ord("q"):
            break
        elif key == ord("c"):
            box = None
            state = 0
            tracker = OPENCV_OBJECT_TRACKERS[trackrType]()
            position = deque()

        #writer.write(frame)

    if writer:
        writer.release()
    vs.release()
    cv2.destroyAllWindows()
    SerialObj.close()          # Close the port
