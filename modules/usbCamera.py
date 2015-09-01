#!/usr/bin/env python
__author__ = 'chris'

import syslog
import cv
from theCamera import camera

class usbcam(camera):
    KAMERA_NR = 0

    def __init__(self):
        cam = cv.CaptureFromCAM(self.KAMERA_NR)

    def startPreview(self):
        taste = 0
        while taste <> ord("q"):
            bild = cv.QueryFrame(cam)
            cv.ShowImage("Livebild", bild)
            taste = cv.WaitKey(2)