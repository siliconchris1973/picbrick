#!/usr/bin/env python
__author__ = 'chris'

import Logger
import config_simple as CONFIG

try:
    import picamera
except:
    print "could not load picamera\n" \
          "you may either be missing an installed instance of the picamera, in which case it might\n" \
          "be sufficient to do a 'sudo pip install picamera'.\n" \
          "Or you tried to start this script on a system other than a Raspberry PI."

class camera(object):
    camera = object

    pictureWidth = 320
    pictureHeight = 240
    videoWidth = 640
    videoHeight = 240
    videoDuration = 10

    def __init__(self):
        self.logger = Logger.Logger(self.__class__.__name__).get()
        self.logger.debug("initializing camera")
        if CONFIG.camEnabled:
            try:
                camera = picamera.PiCamera()
            #except picamera.exc.PiCameraError, e:
            except:
                self.logger.error("Could not initialize the camera, something's wrong with it")
                #syslog.syslog("Could not initialize the camera, something's wrong with it: " + str(e))
                #raise Exception("Camera Error. This is serious as it prevents me from fullfilling my one and only duty, taking photos")

    def getCamera(self):
        self.logger.debug("returning camera object")
        return self.camera

    def takePicture(self, pic, picWidth=pictureWidth, picHeight=pictureHeight):
        self.logger.debug("taking picture with " + str(picWidth) + "x" + str(picHeight))
        if CONFIG.camEnabled:
            try:
                self.camera.resolution = (picWidth, picHeight)
                self.camera.capture(pic)
            except picamera.exc.PiCameraError, e:
                self.logger.error("Could not take picture, something's wrong with the camera: " + str(e))
                #raise Exception("Camera Error. This is serious")

    def takeVideo(self, vid, vidWidth=videoWidth, vidHeight=videoHeight, vidDur=videoDuration):
        self.logger.debug("taking " + str(vidDur) + " seconds of video with " + str(vidWidth) + "x" + str(vidHeight))
        if CONFIG.camEnabled:
            try:
                self.camera.resolution = (vidWidth, vidHeight)
                self.camera.start_recording(vid)
                self.camera.wait_recording(vidDur)
                self.camera.stop_recording()
            except picamera.exc.PiCameraError, e:
                self.logger.error("Could not record video, something's wrong with the camera: " + str(e))
                #raise Exception("Camera Error. This is serious")

    def startPreview(self):
        self.logger.debug("starting live preview")
        if CONFIG.camEnabled:
            self.camera.start_preview()

    def stopPreview(self):
        self.logger.debug("stopping live preview")
        if CONFIG.camEnabled:
            self.camera.stop_preview()

if __name__ == '__main__':
    print "theCamera.py is NOT intended to be started from command line  ... "
