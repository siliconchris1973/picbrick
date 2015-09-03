#!/usr/bin/env python
__author__ = 'chris'

import cv
import logging
from theCamera import camera


class usbcam(camera):
    KAMERA_NR = 0

    def __init__(self):
        logger = logging.getLogger(__name__)

        cam = cv.CaptureFromCAM(self.KAMERA_NR)

    def startPreview(self, cam):
        logger = logging.getLogger(__name__)

        taste = 0
        while taste <> ord("q"):
            bild = cv.QueryFrame(cam)
            cv.ShowImage("Livebild", bild)
            taste = cv.WaitKey(2)