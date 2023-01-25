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

use a library for arduino stepper control( AccelStepper) https://www.airspayce.com/mikem/arduino/AccelStepper/classAccelStepper.html
