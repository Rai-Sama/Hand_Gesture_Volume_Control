import cv2 
import time
import numpy as np
import hand_tracking_module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam, hCam = 640, 720 # Width & Height of the video

WINDOW_NAME = "Volume Controller"
cap = cv2.VideoCapture(0)

cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# cap.set(3, wCam) # 3 means width cam
# cap.set(4, hCam) # 4 means height cam
ptime = 0

detector = htm.handDetector(detectionCon=0.7)


# Using Pycaw library to control system volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
initVol = volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)

minVol = volRange[0]
maxVol = volRange[1]

vol = 0 # So volume does not become a local variable
volBar = 400 # Same reason as vol
volPer = 0
#volPer = 100*((initVol+65)/65) # Not working as expected
#print(initVol)
#print(volPer)

while True:
	success, img = cap.read()

	img = cv2.flip(img, 1) # Flipping the image horizontally (since, my webcam is fliped by default)
	img = detector.findHands(img) 

	lmList = detector.findPosition(img, draw=False)
	
	
	
	if(len(lmList)):
		# print(lmList[4], lmList[8])
		x1, y1 = lmList[4][1], lmList[4][2] # co-ordinates of thumb
		x2, y2 = lmList[8][1], lmList[8][2] # Co-ordinates of index finger
		cx, cy = (x1 + x2)//2, (y1+y2)//2 # Mid-point b/w the two

		cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED) # Drawing circles at both fingers
		cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
		cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3) # Drawing a line between the fingers
		cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
		length = math.hypot(x1 - x2, y1 - y2)
		# print(length)

		# We saw that extending the hand completely gives a length of around 300 and min. should be around 50px
		# Note that 300 only works if the hand is in close proximity. If your use case is from further away you may decrease it
		# Volume range(From Pycaw.) -> -65 to 0 

		vol = np.interp(length, [50, 300], [minVol, maxVol]) # Actual volume
		volBar = np.interp(length, [50, 300], [400, 150]) # Bar to be displayed
		volPer = np.interp(length, [50, 300], [0, 100]) # Volume in percentage
		
		# print(int(length), vol)
		volume.SetMasterVolumeLevel(vol, None)
		if length < 50: # Very close (button effect) --> Decreasing further gave unstable results even when fingers were touching
			cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED) # Changes colour so it feels like a button

	cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3) # Initial volume bar
	cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED) # Adjusting the bar
	cv2.putText(img, f'Volume: {int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 3) # printing volume percentage

	# Calculating and displaying FPS
	ctime = time.time()
	fps = 1/(ctime - ptime)
	ptime = ctime
	cv2.putText(img, f'FPS: {int(fps)}', (5, 30), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 3)

	cv2.imshow(WINDOW_NAME, img)
	if cv2.waitKey(1) & 0xFF == 27: # Stop when Esc is pressed
		break	