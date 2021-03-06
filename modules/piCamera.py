#!/usr/bin/env python
__author__ = 'chris'

import Logger
from theCamera import camera

try:
    import picamera
except:
    print "could not load picamera\n" \
          "you may either be missing an installed instance of the picamera, in which case it might\n" \
          "be sufficient to do a 'sudo pip install picamera'.\n" \
          "Or you tried to start this script on a system other than a Raspberry PI."

class picam(camera):
    def __init__(self):
        self.logger = Logger.Logger(self.__class__.__name__).get()
        self.logger.debug("initializing camera")

        try:
            camera = picamera.PiCamera()
        #except picamera.exc.PiCameraError, e:
        except:
            Logger.error("Could not initialize the camera, something's wrong with it")
            #syslog.syslog("Could not initialize the camera, something's wrong with it: " + str(e))
            #raise Exception("Camera Error. This is serious as it prevents me from fullfilling my one and only duty, taking photos")

    def startPreview(self):
        self.logger.debug("starting live preview")
        self.camera.start_preview()

    def stopPreview(self):
        self.logger.debug("stopping live preview")
        self.camera.stop_preview()

if __name__ == '__main__':
    print "piCamera.py is NOT intended to be started from command line  ... "
