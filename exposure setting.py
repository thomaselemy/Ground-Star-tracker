import os
import time

import cv2

# open video0
cap = cv2.VideoCapture(0)

def set_manual_exposure(dev_video_id, exposure_time):
    commands = [
        #("v4l2-ctl --device /dev/video"+str(id)+" -c exposure_auto=3"),
        # ("v4l2-ctl --device /dev/video"+str(id)+" -c exposure_auto=1"),
        ("v4l2-ctl --device /dev/video"+str(id)+" -c exposure_absolute="+str(exposure_time))
    ]
    for c in commands:
        os.system(c)
# usage
set_manual_exposure(1, -1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
