#!/usr/bin/env python
__author__ = 'chris'

#
# GPIO ports
#
gpic = 21     # GPIO pin connected to the take a picture button
gvid = 20     # GPIO pin connected to the take a video button
gpir = 16     # GPIO pin connected to the PIR


# if set to False, the system will not take pictures and/or try to use the GPIO ports,
# but rather log and print an information on what it would do
camEnabled = False
gpioEnabled = False


#
# default input state for the GPIO connections'
#
input_con_ground_inactive = True
input_con_ground_active = False
input_con_vcc_inactive = False
input_con_vcc_active = True

# choose the GPIO connection for the buttons,
# these can either be connected to ground (in which case a button press would cause current to be interrupted)
# or a button could be connected to a vcc line (in which case a button press would cause current to flow)
picture_button = "ground"
video_button = "ground"


if picture_button == "ground":
    input_state_pic = input_con_ground_inactive
else:
    input_state_pic = input_con_vcc_inactive

if video_button == "ground":
    input_state_vid = input_con_ground_inactive
else:
    input_state_vid = input_con_vcc_inactive

# the PIR sensor will always cause current to flow, in case a movement is detected
input_state_pir = input_con_vcc_inactive



#
# directory structure
#
baseDataDirectory = "/usr/local/var/picbrick"
core_data = baseDataDirectory + "/" + "data"
imageDir = baseDataDirectory + "/" + "images"
videoDir = baseDataDirectory + "/" + "videos"
initial_image = 'HAL900_320x240.png'
end_image = 'endPicture.png'

logging_dir = baseDataDirectory + "/" + "log"
log_level = "DEBUG"
printLogToConsole = True

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
endColor = red

btnCycle_col = white
btnPrev_col = white
btnNext_col = white