#Import Necessary Packages
import cv2
import time  
import numpy as np
import math
from enum import Enum
import self as self
from grip import GripPipeline
#from playsound import playsound
#from pygame import mixer
from picamera.array import PiRGBArray
from picamera import PiCamera

# Pipeline Constructor
pipeline = GripPipeline()

# Constructing Camera Object
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))
time.sleep(0.1)

# Initializing Sound Object
#mixer.init()
#mixer.music.load("beep-04.mp3")
#mixer.music.set_volume(0.5)
#mixer.music.play()

# Loop reads from camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	
    frame = rawCapture.array 
    vidgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #
    contours, hierarchy = cv2.findContours(vidgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    try:
        # Process the Grip Pipeline
        pipeline.process(frame)
        # Populate data from contours
        contour_data = pipeline.find_contours_output
    except (ZeroDivisionError):
        self.logger.logMessage("Divide by 0 exception in GRIP Pipeline")
            
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        if len(approx) > 25:
            cv2.drawContours(frame, contour_data, -1, (0, 255, 0), 3)
    
    # show the frame
    cv2.imshow("Frame", frame)
    
    # play noise if red light detected
    if len(contour_data) > 1:
        print("beep")
        #playsound("beep-03.wav")
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
    # if the `q` key was pressed, break from the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()

