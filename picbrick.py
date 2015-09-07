#!/usr/bin/env python
__author__ = 'chris'
try:
    import RPi.GPIO as GPIO
except:
    print "could not load GPIO - you probably run this script on a system other than a Raspberry PI."
import datetime
import time
import sys
import string
import os
import argparse
#import logging
import pygame
from pygame.locals import *

from modules.theCamera import camera
from modules.theDisplay import display
from modules.smsService import sms
from modules import config_simple as CONFIG
from modules import logger


class picbrick:
    def __init(self):
        self.logger = logger(self.__class__.__name__).get()

    # This function takes the name of an image to load.
    # It also optionally takes an argument it can use to set a colorkey for the image.
    # A colorkey is used in graphics to represent a color of the image that is transparent.
    # we also use this this function to initialize filenav.py -- see modules
    def load_image(self, directory, filename, colorkey=None):
        fullname = os.path.join(directory, filename)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            self.logger.error('Cannot load image:' + filename + ' from directory ' + directory)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()

    def format_filename(self, s):
        """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.

    Note: this method may produce invalid filenames such as ``, `.` or `..`
    When I use this method I prepend a date string like '2009_01_15_19_46_32_'
    and append a file extension like '.txt', so I avoid the potential of using
    an invalid filename.

    """
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in s if c in valid_chars)
        filename = filename.replace(' ','_') # I don't like spaces in filenames.
        return filename


    def run(self, argv):
        parser = argparse.ArgumentParser(description='Take and display pictures and videos.')
        parser.add_argument('--automode', dest='autoMode',
                       help='shall the system run in automatic mode)')
        parser.add_argument('--picturewidth', dest='pictureWidth', type=int, default=320,
                       help='# of pixels for the width of the picture)')
        parser.add_argument('--pictureheight', dest='pictureHeight', type=int, default=240,
                       help='# of pixels for the height of the picture)')
        parser.add_argument('--videowidth', dest='videoWidth', type=int, default=640,
                       help='# of pixels for the width of the video)')
        parser.add_argument('--videoheight', dest='videoHeight', type=int, default=480,
                       help='# of pixels for the height of the video)')
        parser.add_argument('--videoduration', dest='videoDuration', type=int, default=10,
                       help='# of seconds to record a video - can be over ruled by keeping the video button pressed)')
        parser.add_argument('--imagedir', dest='imageDirectory', default="/usr/local/var/picbrick/images",
                       help='default directory path for the images)')
        parser.add_argument('--videodir', dest='videoDirectory', default="/usr/local/var/picbrick/videos",
                       help='default directory path for the videos)')

        args = parser.parse_args()

        myTFT = display()
        myScreen = myTFT.get_display()
        myCamera = camera()
        autoMode = CONFIG.autoMode
        clock = pygame.time.Clock()

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(CONFIG.gpic, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(CONFIG.gvid, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(CONFIG.gpir, GPIO.IN)
        except:
            self.logger.error("could not set the GPIOs. \n")

        fullname = os.path.join(CONFIG.core_data, CONFIG.initial_image)
        #fullname = CONFIG.core_data + "/" + CONFIG.initial_image
        self.logger.debug('PIcBrick initialized - displaying start picture ' + str(fullname))
        myTFT.display_image(myScreen, fullname)
        self.logger.info('Ready to take pictures, videos or wait for the bad guys')

        while True:
            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.
            clock.tick(10)

            try:
                input_state_pic = GPIO.input(CONFIG.gpic)
                input_state_vid = GPIO.input(CONFIG.gvid)
                input_state_pir = GPIO.input(CONFIG.gpir)
            except:
                self.logger.error("could not watch GPIO-ports, we should bail out here")
                #raise Exception("could not watch GPIO-ports, we should bail out here")

            try:
                if input_state_pic == False or input_state_vid == False or (input_state_pir == True and autoMode == True):
                    if input_state_pic == False:
                        takePicture = True
                        takeVideo = False
                        sendSms = False
                        eventSource = "picture_button"
                        self.logger.debug("captured "+eventSource+" event")
                    elif input_state_vid == False:
                        takePicture = False
                        takeVideo = True
                        sendSms = False
                        eventSource = "video_button"
                        self.logger.debug("captured "+eventSource+" event")
                    elif input_state_pir == True:
                        takePicture = True
                        takeVideo = True
                        sendSms = True
                        eventSource = "PIR motion detector"
                        self.logger.debug("captured "+eventSource+" event")
                    else:
                        takePicture = False
                        takeVideo = False
                        sendSms = False
                        eventSource = "unknown"
                        self.logger.warn("captured "+eventSource+" event")


                    a = datetime.datetime.now()
                    a = str(a)
                    a = a[0:19]
                    b = self.format_filename(a)
                    pic = (CONFIG.imageDir)+("/img_")+(b)+(".jpg")
                    vid = (CONFIG.videoDir)+("/vid_")+(b)+(".h264")

                    txtmessage = ("captured event (" + eventSource + ") at "+str(a))
                    self.logger.info(txtmessage)

                    if takePicture:
                        #myCamera.takePicture(pic, pictureWidth, pictureHeight)
                        if CONFIG.camEnabled:
                            myCamera.takePicture(pic)
                            self.logger.info("picture taken, waiting " + str(CONFIG.waitTimeAfterPicture) + " seconds...")

                        fullname = os.path.join(CONFIG.imageDir, pic)
                        if CONFIG.camEnabled:
                            myTFT.display_image(myScreen, fullname)
                        else:
                            self.logger.info('I would have taken a picture with name ' + str(pic) + ' now.')

                        time.sleep(CONFIG.waitTimeAfterPicture)
                        time.sleep(3)

                        fullname = os.path.join(CONFIG.core_data, CONFIG.initial_image)
                        myTFT.display_image(myScreen, fullname)

                    if takeVideo:
                        #myCamera.takeVideo(vid, videoWidth, videoHeight, videoDuration)
                        if CONFIG.camEnabled:
                            myCamera.takeVideo(vid)
                            self.logger.info(str(CONFIG.videoDuration) + " seconds of video taken, waiting " + str(CONFIG.waitTimeAfterVideo) + " seconds...")
                        else:
                            self.logger.info('I would have taken a video with name ' + str(vid) + ' now.')

                        time.sleep(CONFIG.waitTimeAfterVideo)

                    if sendSms:
                        message = (txtmessage),(pic),(vid)
                        sms(message)



                    self.logger.info("event processed, waiting " + str(CONFIG.waitTimeAfterEvent) + " seconds...")
                    time.sleep(CONFIG.waitTimeAfterEvent)

                    self.logger.debug("all done, waiting for next event...")
            except:
                self.logger.error("could not process input event")

        try:
            GPIO.cleanup()
        except:
            self.logger.error("could not clean GPIO")

if __name__ == '__main__':
    print "PIcBrick started ... "
    pib = picbrick()
    pib.run(sys.argv)

