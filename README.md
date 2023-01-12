# Ground-Star-tracker
Use a low light webcam camera and stepper motors to follow star movments and cancel out the movement of the earth for Deep sky photography. 

Use OpenCV trackers to command a telescope to follow objects. 

Python code is for tracking of stars and sending commands. CSRT and medianflow seem to work well for the apparent slow moving of the stars.

The current control method moves the telescope via serial commands. Up is "u", down is "d", etc. for left and right. the distances these move the telescope are are predefined in the arduino code via the number of steps to take. 

Python code tries to center selected star in center of frame(pixels 320, 240) 




IDK if this is the best control method. the telescope arduino currently has predefined movement commands. Variable velocity control and may be a better control method. 

Loosing tracking of a star or object(ie cloud blocking sky) stops movement. May be good idea to find apparent star velocity after a few minutes and use that to update movements.

Issues:

As the telescope approches center, number of moves to center camera on object to large and only hovers around center 

Need to be able to use tkinter to select com port in windows.

combine tkinter code to position telescope when not tracking

Set exposure value for webcam 

set higher resolution 

these commands dont seem to work https://docs.arducam.com/UVC-Camera/Adjust-the-minimum-exposure-time/

use a library for arduino stepper control( AccelStepper) https://www.airspayce.com/mikem/arduino/AccelStepper/classAccelStepper.html


**********************************
new arduino code. 

60,000 steps required to go 360 (0.006 deg a step)not including microstepping

with microstepping(x 64)=3,840,000 

calculated fov of camera=10.54deg

number of steps in fov=1,756.67

with microstepping accounted for=10,666.67

pixels per degree=182.16 in horizontal fov 
pixels per degree=102.47 in vertical fov 

logic 

start at zero position

find object, distance from center 
