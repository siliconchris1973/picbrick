#!/usr/bin/env python
__author__ = 'chris'

import logging
from theCamera import camera

try:
    import picamera
except:
    print "could not load picamera\n" \
          "you may either be missing an installed instance of the picamera, in which case it might\n" \
          "be sufficient to do a 'sudo pip install picamera'.\n" \
          "Or you tried to start this script on a system other than a Raspberry PI."

class picam(camera):
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        try:
            camera = picamera.PiCamera()
        #except picamera.exc.PiCameraError, e:
        except:
            logger.error("Could not initialize the camera, something's wrong with it")
            #syslog.syslog("Could not initialize the camera, something's wrong with it: " + str(e))
            #raise Exception("Camera Error. This is serious as it prevents me from fullfilling my one and only duty, taking photos")

    def startPreview(self):
        self.logger = logging.getLogger(__name__)
        self.camera.start_preview()

    def stopPreview(self):
        self.logger = logging.getLogger(__name__)
        self.camera.stop_preview()