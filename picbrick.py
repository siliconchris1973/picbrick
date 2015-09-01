#!/usr/bin/env python
__author__ = 'chris'
try:
    import RPi.GPIO as GPIO
except:
    print "could not load GPIO \n" \
          "this is possible because you run this script on a system other than a Raspberry PI."
import datetime
import time
import sys
import string
import syslog
import os
import pygame
from pygame.locals import *

from modules.theCamera import camera
from modules.theDisplay import display
from modules.smsService import sms
from modules.config import configuration

# This function takes the name of an image to load.
# It also optionally takes an argument it can use to set a colorkey for the image.
# A colorkey is used in graphics to represent a color of the image that is transparent.
# we also use this this function to initialize filenav.py -- see modules
def load_image(directory, filename, colorkey=None):
    fullname = os.path.join(directory, filename)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        syslog.syslog('Cannot load image:' + filename + ' from directory ' + directory)
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def format_filename(s):
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


def main(argv):
    myTFT = display()
    myScreen = myTFT.get_display()
    myCamera = camera()
    myConf = configuration()
    autoMode = myConf.autoMode
    clock = pygame.time.Clock()

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(myConf.gpic, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(myConf.gvid, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(myConf.gpir, GPIO.IN)
    except:
        syslog.syslog("could not set the GPIOs. \n")

    syslog.syslog('picbrick initialized')

    fullname = os.path.join(myConf.core_data, myConf.initial_image)
    myTFT.display_image(myScreen, fullname)
    syslog.syslog('Ready to take pictures, videos or wait for the bad guys')

    while True:
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)

        try:
            input_state_pic = GPIO.input(myConf.gpic)
            input_state_vid = GPIO.input(myConf.gvid)
            input_state_pir = GPIO.input(myConf.gpir)
        except:
            syslog.syslog("could not watch GPIO-ports, we should bail out here")
            #raise Exception("could not watch GPIO-ports, we should bail out here")

        try:
            if input_state_pic == False or input_state_vid == False or (input_state_pir == True and autoMode == True):
                if input_state_pic == False:
                    takePicture = True
                    takeVideo = False
                    sendSms = False
                    eventSource = "picture_button"
                elif input_state_vid == False:
                    takePicture = False
                    takeVideo = True
                    sendSms = False
                    eventSource = "video_button"
                elif input_state_pir == True:
                    takePicture = True
                    takeVideo = True
                    sendSms = True
                    eventSource = "PIR motion detector"
                else:
                    takePicture = False
                    takeVideo = False
                    sendSms = False
                    eventSource = "unknown"


                a = datetime.datetime.now()
                a = str(a)
                a = a[0:19]
                b = format_filename(a)
                pic = (myConf.imageDir)+("/img_")+(b)+(".jpg")
                vid = (myConf.videoDir)+("/vid_")+(b)+(".h264")

                txtmessage = ("captured event (" + eventSource + ") at "+str(a))
                syslog.syslog(txtmessage)

                if takePicture:
                    #myCamera.takePicture(pic, pictureWidth, pictureHeight)
                    myCamera.takePicture(pic)
                    syslog.syslog("picture taken, waiting " + str(myConf.waitTimeAfterPicture) + " seconds...")

                    fullname = os.path.join(myConf.imageDir, pic)
                    myTFT.display_image(myScreen, fullname)

                    time.sleep(myConf.waitTimeAfterPicture)
                    time.sleep(3)

                    fullname = os.path.join(myConf.core_data, myConf.initial_image)
                    myTFT.display_image(myScreen, fullname)

                if takeVideo:
                    #myCamera.takeVideo(vid, videoWidth, videoHeight, videoDuration)
                    myCamera.takeVideo(vid)
                    syslog.syslog(str(myConf.videoDuration) + " seconds of video taken, waiting " + str(myConf.waitTimeAfterVideo) + " seconds...")
                    time.sleep(myConf.waitTimeAfterVideo)

                if sendSms:
                    message = (txtmessage),(pic),(vid)
                    sms(message)



                syslog.syslog("event processed, waiting " + str(myConf.waitTimeAfterEvent) + " seconds...")
                time.sleep(myConf.waitTimeAfterEvent)

                syslog.syslog("all done, waiting for next event...")
        except:
            syslog.syslog("could not process input event")

    try:
        GPIO.cleanup()
    except:
        syslog.syslog("could not clean GPIO")

if __name__ == '__main__':
    main(sys.argv)

