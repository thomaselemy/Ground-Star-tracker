# Ground-Star-tracker
Use a low light webcam camera and stepper motors to follow star movments and cancel out the movement of the earth for Deep sky photography. 

Use OpenCV trackers to command a telescope to follow objects. 

Python code is for tracking of stars and sending commands. CSRT and medianflow seem to work well for the apparent slow moving of the stars.

The current control method moves the telescope via serial commands. Up is "u", down is "d", etc. for left and right. the distances these move the telescope are are predefined in the arduino code via the number of steps to take. 

Usage: connect webcam and microcontroller for reading serial inputs and motor control. 
Run code or compiled .exe(im using pyinstaller). 
Select com port from dropdown. 
close tkinter window. 
tkinter window and video feed should open. 
Hit "S" and draw bounding box around star/object. Space or enter to run tracking  

https://user-images.githubusercontent.com/33559754/230535231-52e4be6b-03f1-47fd-a07e-e609f3b29b0a.mp4

Python code tries to center selected star in center of frame(pixels x, y) 

Test image captured 1/24/2023

 ![captured 1/24/23](https://user-images.githubusercontent.com/33559754/214767967-a20d18a1-c12f-4a5a-ac38-775e32d15f9e.jpg)

Image of pan/tilt telescope: Svbony 50mm guide scope as main telescope, two 1:300 gear ratio nema 14 steppers
![20221009_211214](https://user-images.githubusercontent.com/33559754/219271229-4c7deb0b-f984-4c4a-bffe-3e087eabbda8.jpg)
