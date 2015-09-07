#!/usr/bin/env python
__author__ = 'chris'

import cv
import Logger
from theCamera import camera


class usbcam(camera):
    KAMERA_NR = 0

    def __init__(self):
        self.logger = Logger.Logger(self.__class__.__name__).get()
        self.logger.debug("initializing camera")

        cam = cv.CaptureFromCAM(self.KAMERA_NR)

    def startPreview(self, cam):
        self.logger.debug("starting live preview")
        taste = 0
        while taste <> ord("q"):
            bild = cv.QueryFrame(cam)
            cv.ShowImage("Livebild", bild)
            taste = cv.WaitKey(2)

    def stopPreview(self):
        self.logger.debug("stopping live preview")
        self.cam.stop_preview()

if __name__ == '__main__':
    print "usbCamera.py is NOT intended to be started from command line  ... "
