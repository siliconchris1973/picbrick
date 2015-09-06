#!/usr/bin/env python
__author__ = 'chris'

#
# GPIO ports
#
gpic = 21     # GPIO pin connected to the take a picture button
gvid = 20     # GPIO pin connected to the take a video button
gpir = 16     # GPIO pin connected to the PIR

camEnabled = False # if set to False, the system will not take pictures, but rather log and print an information that it would take a pictur or a video.

#
# default input state for the GPIO connections'
#
input_state_pic = True
input_state_vid = True
input_state_pir = True


#
# directory structure
#
baseDataDirectory = "/usr/local/var/picbrick"
core_data = baseDataDirectory + "/" + "data"
imageDir = baseDataDirectory + "/" + "images"
videoDir = baseDataDirectory + "/" + "videos"
initial_image = 'HAL900_320x240.png'

logging_dir = baseDataDirectory + "/" + "log"

#
# screen/display definition
#
screenWidth = 320
screenHeight = 240
screenSize = (screenWidth, screenHeight)


#
# picture and video size
#
pictureWidth = 320
pictureHeight = 240
videoWidth = 640
videoHeight = 240
videoDuration = 10


#
# how long to wait after taking photos and the like
#
waitTimeAfterPicture = 0
waitTimeAfterVideo = 0
waitTimeAfterEvent = 0


#
# run in automatic mode
#
# if set to true - button or command line argument -
# the camera will take pictures and videos, if the
# motion detector detects movement
autoMode = False


#
# color definitions
#
#color    R    G    B
white = (255, 255, 255)
red   = (255,   0,   0)
green = (  0, 255,   0)
blue  = (  0,   0, 255)
black = (  0,   0,   0)
cyan  = (  0, 255, 255)

backgroundColor = black

btnCycle_col = white
btnPrev_col = white
btnNext_col = white