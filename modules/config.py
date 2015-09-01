#!/usr/bin/env python
__author__ = 'chris'

class configuration:
    def __init__(self):
        # GPIO ports
        gpic = 21     # GPIO pin connected to the take a picture button
        gvid = 20     # GPIO pin connected to the take a video button
        gpir = 16     # GPIO pin connected to the PIR

        input_state_pic = True
        input_state_vid = True
        input_state_pir = True

        pictureWidth = 320
        pictureHeight = 240
        videoWidth = 640
        videoHeight = 240
        videoDuration = 10

        #
        # screen/display definition
        #
        #screen size
        screenWidth = 320
        screenHeight = 240
        screenSize = (screenWidth, screenHeight)
        # picture and video size
        pictureWidth = 320
        pictureHeight = 240
        videoWidth = 640
        videoHeight = 480


        #
        # color definitions
        #
        #define some colors
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

        #
        # how long to wait after taking photos and the like
        waitTimeAfterPicture = 0
        waitTimeAfterVideo = 0
        waitTimeAfterEvent = 0

        #
        # if set to true - button or command line argument -
        # the camera will take pictures and videos, if the
        # motion detector detects movement
        autoMode = False

        #
        # directory structure
        #
        # directory structure
        baseDataDirectory = "/usr/local/var/picbrick"
        core_data = baseDataDirectory + "/" + "data"
        initial_image = 'HAL900_320x240.png'
        imageDir = baseDataDirectory + "/" + "images"
        videoDir = baseDataDirectory + "/" + "videos"

