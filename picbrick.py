#!/usr/bin/env python
__author__ = 'chris'

import RPi.GPIO as GPIO
import picamera
import datetime
import time
import urllib
import urllib2
import sys
import string
import syslog
import os
import pygame
from pygame.locals import *

# define some global vars

#
# screen/display definition
#
#screen size
screenWidth = 320
screenHeight = 240
size = (screenWidth, screenHeight)
# picture and video size
pictureWidth = 320
pictureHeight = 240
videoWidth = 640
videoHeight = 480


#
# color definitions
#
#define some colors
#color    R    G    B
white = (255, 255, 255)
red   = (255,   0,   0)
green = (  0, 255,   0)
blue  = (  0,   0, 255)
black = (  0,   0,   0)
cyan  = (  0, 255, 255)

btnCycle_col = white
btnPrev_col = white
btnNext_col = white



#
# sms-service
#
#Replace the xxxxxxx with the number you wish to text.
to = "+4915112240942"
#Replace the xxxxxx with the hash given to you by smspi.co.uk
hash = "bfd626d66e9ca13b1f21843725f2eef2"


#
# GPIO ports
#
gpic = 21     # GPIO pin connected to the take a picture button
gvid = 20     # GPIO pin connected to the take a video button
gpir = 16     # GPIO pin connected to the PIR


#
# Picture and video
#
# define what to do on each event type picture_button, video_button or PIR
picTakePicture = True
picTakeVideo = False
picSendSms = False

vidTakePicture = False
vidTakeVideo = True
vidSendSms = False

pirTakePicture = True
pirTakeVideo = True
pirSendSms = False

waitTimeAfterPicture = 2
waitTimeAfterVideo = 0
waitTimeAfterEvent = 5

videoDuration = 10

# if set to true - button or command line argument -
# the camera will take pictures and videos, if the
# motion detector detects movement
autoMode = False

#
# directory structure
#
# directory structure
core_data = '/usr/local/var/picture_brick/data'
initial_image = 'HAL900_320x240.png'
imageDir = "/usr/local/var/picture_brick/images"
videoDir = "/usr/local/var/picture_brick/videos"


##### NO NEED TO CHANGE ANYTHING BELOW HERE #####

# these three are set accoridng to event (picture- or video button or PIR)
takeVideo = False
takePicture = False
sendSms = False
eventSource = "NULL"

#
# image functions
#
def display_image(screen, directory, filename):
    fullname = os.path.join(directory, filename)
    try:
        # load from subfolder 'data'
        image = pygame.image.load(fullname)
    except:
        #raise UserWarning, "Unable to find the images in the folder 'data' :-( "
        syslog.syslog("Unable to find the images in the folder 'data' :-( ")
    screen.blit(image,(0,0))


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



def get_display():
    disp_no = os.getenv('DISPLAY')
    if disp_no:
        syslog.syslog("I'm running under X display = {0}".format(disp_no))
        pygame.mouse.set_visible(True)
    else:
        drivers = ['directfb', 'fbcon', 'svgalib']
        found = False
        for driver in drivers:
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                syslog.syslog('Driver: {0} failed.'.format(driver))
                continue
            found = True
            syslog.syslog("I'm running on the framebuffer using driver " + str(driver))
            pygame.mouse.set_visible(False)
            break

        if not found:
            raise Exception('No suitable video driver found!')


    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
    os.environ["SDL_MOUSEDRV"] = "TSLIB"


def takePic(camera, pic, picWidth, picHeight):
    try:
        camera.resolution = (picWidth, picHeight)
        camera.capture(pic)
    except picamera.exc.PiCameraError, e:
        syslog.syslog("Could not take picture, something's wrong with the camera: " + str(e))
        #raise Exception("Camera Error. This is serious")

def takeVid(camera, vid, vidWidth, vidHeight):
    try:
        camera.resolution = (vidWidth, vidHeight)
        camera.start_recording(vid)
        camera.wait_recording(videoDuration)
        camera.stop_recording()
    except picamera.exc.PiCameraError, e:
        syslog.syslog("Could not record video, something's wrong with the camera: " + str(e))
        #raise Exception("Camera Error. This is serious")

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


### sms sending
def sms(to,message,hash):
    values = {
          'to' : to,
          'message' : message,
          'hash' : hash } # Grab your hash from http://www.smspi.co.uk

    url = 'http://www.smspi.co.uk/send/'

    postdata = urllib.urlencode(values)
    req = urllib2.Request(url, postdata)

    syslog.syslog('Attempt to send SMS ...')

    try:
        response = urllib2.urlopen(req)
        response_url = response.geturl()
        if response_url==url:
            syslog.syslog(response.read())
    except urllib2.URLError, e:
        syslog.syslog(syslog.LOG_ERR, 'Send failed!' + e.reason)


def main(argv):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpic, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(gvid, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(gpir, GPIO.IN)
    try:
        camera = picamera.PiCamera()
    except picamera.exc.PiCameraError, e:
        syslog.syslog("Could not initialize the camera, something's wrong with it: " + str(e))
        #raise Exception("Camera Error. This is serious as it prevents me from fullfilling my one and only duty, taking photos")

    get_display()

    pygame.init()
    screen = pygame.display.set_mode(size)
    screen.fill((black))
    pygame.display.update()
    clock = pygame.time.Clock()

    """
    disp_no = os.getenv('DISPLAY')
    if disp_no:
        syslog.syslog("I'm running under X display = {0}".format(disp_no))
        pygame.mouse.set_visible(True)
    else:
        drivers = ['directfb', 'fbcon', 'svgalib']
        found = False
        for driver in drivers:
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                syslog.syslog('Driver: {0} failed.'.format(driver))
                continue
            found = True
            syslog.syslog("I'm running on the framebuffer using driver " + str(driver))
            pygame.mouse.set_visible(False)
            break

        if not found:
            raise Exception('No suitable video driver found!')


    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
    os.environ["SDL_MOUSEDRV"] = "TSLIB"
    """

    syslog.syslog('picbrick initialized')

    display_image(screen, core_data, initial_image)
    syslog.syslog('Ready to take pictures, videos or wait for the bad guys')

    while True:
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)

        input_state_pic = GPIO.input(gpic)
        input_state_vid = GPIO.input(gvid)
        input_state_pir = GPIO.input(gpir)

        if input_state_pic == False or input_state_vid == False or (input_state_pir == True and autoMode == True):
            if input_state_pic == False:
                takePicture = picTakePicture
                takeVideo = picTakeVideo
                sendSms = picSendSms
                waitTimeAfterPicture = 0
                waitTimeAfterVideo = 0
                waitTimeAfterEvent = 0
                eventSource = "picture_button"
            elif input_state_vid == False:
                takePicture = vidTakePicture
                takeVideo = vidTakeVideo
                sendSms = vidSendSms
                waitTimeAfterPicture = 0
                waitTimeAfterVideo = 0
                waitTimeAfterEvent = 0
                eventSource = "video_button"
            elif input_state_pir == True:
                takePicture = pirTakePicture
                takeVideo = pirTakeVideo
                sendSms = pirSendSms
                waitTimeAfterPicture = 2
                waitTimeAfterVideo = 0
                waitTimeAfterEvent = 5
                eventSource = "PIR motion detector"
            else:
                takePicture = False
                takeVideo = False
                sendSms = False
                waitTimeAfterPicture = 0
                waitTimeAfterVideo = 0
                waitTimeAfterEvent = 5
                eventSource = "unknown"

            a = datetime.datetime.now()
            a = str(a)
            a = a[0:19]
            b = format_filename(a)

            txtmessage = ("captured event (" + eventSource + ") at "+str(a))
            syslog.syslog(txtmessage)
            pic = (imageDir)+("/img_")+(b)+(".jpg")
            vid = (videoDir)+("/vid_")+(b)+(".h264")

            message = (txtmessage),(pic),(vid)

            if takePicture:
                takePic(camera, pic, pictureWidth, pictureHeight)
                syslog.syslog("picture taken, waiting " + str(waitTimeAfterPicture) + " seconds...")
                display_image(screen, imageDir, ("img_")+(b)+(".jpg"))
                time.sleep(waitTimeAfterPicture)
                time.sleep(3)
                display_image(screen, core_data, initial_image)

            if takeVideo:
                takeVid(camera, vid, videoWidth, videoHeight)
                syslog.syslog(str(videoDuration) + " seconds of video taken, waiting " + str(waitTimeAfterVideo) + " seconds...")
                time.sleep(waitTimeAfterVideo)

            if sendSms:
                sms(to,message,hash)



            syslog.syslog("event processed, waiting " + str(waitTimeAfterEvent) + " seconds...")
            time.sleep(waitTimeAfterEvent)

            syslog.syslog("all done, waiting for next event...")

    GPIO.cleanup()

if __name__ == '__main__':
    main(sys.argv)

