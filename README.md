# Hand_Gesture_Volume_Control
* A simple Computer Vision project created to learn uses of OpenCV.
* Uses hand gestures (pinch) to control the volume of a device.

## Hand_Tracking_Module.py
* A general module created for all my hand gesture tracking programs.
* Uses mediapipe for tracking landmarks on the hand.

## volume_control.py
* Uses the hand tracking module to track the hand visible on screen and calculates the volume according to the gesture.
* Uses the Pycaw library to control the volume of the system - works for windows machines.

![alt-text](https://github.com/Rai-Sama/Hand_Gesture_Volume_Control/blob/master/Demo.gif)
