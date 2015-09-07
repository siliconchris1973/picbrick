#!/usr/bin/env python
__author__ = 'chris'

import cv
import logger
from theCamera import camera


class usbcam(camera):
    KAMERA_NR = 0

    def __init__(self):
        self.logger = logger(self.__class__.__name__).get()
        cam = cv.CaptureFromCAM(self.KAMERA_NR)

    def startPreview(self, cam):
        taste = 0
        while taste <> ord("q"):
            bild = cv.QueryFrame(cam)
            cv.ShowImage("Livebild", bild)
            taste = cv.WaitKey(2)