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
        core_data = 'data'
        initial_image = 'HAL900_320x240.png'
        imageDir = "images"
        videoDir = "videos"
