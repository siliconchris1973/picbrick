#!/usr/bin/env python
__author__ = 'chris'
try:
    import RPi.GPIO as GPIO
    import picamera
except:
    print "could not load any of GPIO or picamera\n" \
          "this is possible because you run this script on a system other than a Raspberry PI.\n" \
          "In this case you can ignore this error, if you just do debugging, or should go and get\n" \
          "one of those fine mini computers and start inventing, in case you really want to use the script"
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

##### NO NEED TO CHANGE ANYTHING BELOW HERE #####
input_state_pic = True
input_state_vid = True
input_state_pir = True

class tftDisplay:
    #
    # screen/display definition
    #
    #screen size
    screenWidth = 320
    screenHeight = 240
    screenSize = (screenWidth, screenHeight)
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

    backgroundColor = black

    btnCycle_col = white
    btnPrev_col = white
    btnNext_col = white

    def __init__(self, width=320, height=240):
        self.screenWidth = width
        self.screenHeight = height
        self.screenSize = (width, height)

    def get_display(self):
        pygame.init()
        screen = pygame.display.set_mode(self.screenSize)

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

        screen.fill(self.backgroundColor)
        pygame.display.update()
        return screen

    # some fundamental getter and setter
    def getBackgroundColor(self):
        return self.backgroundColor
    def setBackgroundColor(self, color):
        self.backgroundColor = color

    def getScreenSize(self):
        return self.screenSize
    def setScreenSize(self, width, height):
        self.screenWidth = width
        self.screenHeight = height
        self.screenSize(width, height)

    #
    # image functions
    #
    def display_image(self, screen, filename):
        try:
            # load from subfolder 'data'
            image = pygame.image.load(filename)
        except:
            syslog.syslog("Unable to find the image "+filename+" :-( ")

        screen.blit(image,(0,0))

class theCamera:
    camera = object
    pictureWidth = 320
    pictureHeight = 240
    videoWidth = 640
    videoHeight = 240
    videoDuration = 10

    def __init__(self):
        try:
            camera = picamera.PiCamera()
        #except picamera.exc.PiCameraError, e:
        except:
            syslog.syslog("Could not initialize the camera, something's wrong with it")
            #syslog.syslog("Could not initialize the camera, something's wrong with it: " + str(e))
            #raise Exception("Camera Error. This is serious as it prevents me from fullfilling my one and only duty, taking photos")

    def getCamera(self):
        return self.camera

    def takePicture(self, pic, picWidth=pictureWidth, picHeight=pictureHeight):
        try:
            self.camera.resolution = (picWidth, picHeight)
            self.camera.capture(pic)
        except picamera.exc.PiCameraError, e:
            syslog.syslog("Could not take picture, something's wrong with the camera: " + str(e))
            #raise Exception("Camera Error. This is serious")

    def takeVideo(self, vid, vidWidth=videoWidth, vidHeight=videoHeight, vidDur=videoDuration):
        try:
            self.camera.resolution = (vidWidth, vidHeight)
            self.camera.start_recording(vid)
            self.camera.wait_recording(vidDur)
            self.camera.stop_recording()
        except picamera.exc.PiCameraError, e:
            syslog.syslog("Could not record video, something's wrong with the camera: " + str(e))
            #raise Exception("Camera Error. This is serious")



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
    pictureWidth = 320
    pictureHeight = 240
    videoWidth = 640
    videoHeight = 240
    videoDuration = 10
    #
    waitTimeAfterPicture = 0
    waitTimeAfterVideo = 0
    waitTimeAfterEvent = 0
    #
    # if set to true - button or command line argument -
    # the camera will take pictures and videos, if the
    # motion detector detects movement
    autoMode = False
    #
    # directory structure
    #
    # directory structure
    core_data = 'data'
    initial_image = 'HAL900_320x240.png'
    imageDir = "images"
    videoDir = "videos"

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpic, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(gvid, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(gpir, GPIO.IN)
    except:
        syslog.syslog("could not set the GPIOs. \n")

    # set and initialize the screen
    myTFT = tftDisplay()
    myScreen = myTFT.get_display()
    myCamera = theCamera()

    clock = pygame.time.Clock()
    syslog.syslog('picbrick initialized')

    fullname = os.path.join(core_data, initial_image)
    myTFT.display_image(myScreen, fullname)
    syslog.syslog('Ready to take pictures, videos or wait for the bad guys')

    while True:
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)

        try:
            input_state_pic = GPIO.input(gpic)
            input_state_vid = GPIO.input(gvid)
            input_state_pir = GPIO.input(gpir)
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
                pic = (imageDir)+("/img_")+(b)+(".jpg")
                vid = (videoDir)+("/vid_")+(b)+(".h264")

                txtmessage = ("captured event (" + eventSource + ") at "+str(a))
                syslog.syslog(txtmessage)

                if takePicture:
                    #myCamera.takePicture(pic, pictureWidth, pictureHeight)
                    myCamera.takePicture(pic)
                    syslog.syslog("picture taken, waiting " + str(waitTimeAfterPicture) + " seconds...")

                    fullname = os.path.join(imageDir, pic)
                    myTFT.display_image(myScreen, fullname)

                    time.sleep(waitTimeAfterPicture)
                    time.sleep(3)

                    fullname = os.path.join(core_data, initial_image)
                    myTFT.display_image(myScreen, fullname)

                if takeVideo:
                    #myCamera.takeVideo(vid, videoWidth, videoHeight, videoDuration)
                    myCamera.takeVideo(vid)
                    syslog.syslog(str(videoDuration) + " seconds of video taken, waiting " + str(waitTimeAfterVideo) + " seconds...")
                    time.sleep(waitTimeAfterVideo)

                if sendSms:
                    message = (txtmessage),(pic),(vid)
                    sms(to,message,hash)



                syslog.syslog("event processed, waiting " + str(waitTimeAfterEvent) + " seconds...")
                time.sleep(waitTimeAfterEvent)

                syslog.syslog("all done, waiting for next event...")
        except:
            syslog.syslog("could not process input event")

    try:
        GPIO.cleanup()
    except:
        syslog.syslog("could not clean GPIO")

if __name__ == '__main__':
    main(sys.argv)

