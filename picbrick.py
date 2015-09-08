#!/usr/bin/env python
__author__ = 'chris'
try:
    import RPi.GPIO as GPIO
except ImportError, e:
    print "could not load GPIO - you probably run this script on a system other than a Raspberry PI.\n" \
          "As it might be, that you are simply debugging this script on a desktop, I will try to go on"

try:
    import datetime
    import time
    import sys
    import string
    import os
    import argparse
    import pygame
    from pygame.locals import *
except ImportError, e:
    print "\nCould not load one or more essential dependencies, so cowardly refusing to go any further\n>>> Error was: " + str(e)
    sys.exit(-1)

try:
    from modules.theCamera import camera
    from modules.theDisplay import display
    from modules.smsService import sms
    from modules import config_simple as CONFIG
    from modules import Logger
    from modules import fileWatcher
    from modules.event import Event
except ImportError, e:
    print "\nCould not load one or more essential modules from my modules directory, so cowardly refusing to go any further\n" \
          "Did you clone picbrick from github? If not, take a look at the README.md from\n" \
          "     https://github.com/siliconchris1973/picbrick\n" \
          "on how to correctly build and setup the system\n" \
          ">>> Error was: " + str(e)
    sys.exit(-1)


class picbrick:
    def __init__(self):
        # we only want to log the GPIO-Errors ONE time.
        self.alreadyLoggedGPIOError = False
        self.logger = Logger.Logger(self.__class__.__name__).get()

    """
    def __del__(self):
        #fullname = "/usr/local/var/picbrick/data/endPicture.png"
        #self.myTFT.display_image(self.myScreen, fullname)
        #self.clock.tick(100)
        try:
            GPIO.cleanup()
        except:
            raise Exception("could not clean GPIO-ports")
    """

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

    def getCommandLineArguments(self, argv):
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

    def log_file_change(source_path):
        print "%r changed." % (source_path,)

    def log_file_change2(source_path):
        print "%r changed!" % (source_path,)

    def run(self):
        myTFT = display()
        myScreen = myTFT.get_display()
        if CONFIG.camEnabled:
            myCamera = camera()
        autoMode = CONFIG.autoMode
        clock = pygame.time.Clock()

        # initialize file watcher
        watcher              = fileWatcher(CONFIG.imageDir)
        watcher.fileChanged += self.log_file_change2
        watcher.fileChanged += self.log_file_change
        watcher.fileChanged -= self.log_file_change2
        watcher.watchFiles()

        if CONFIG.gpioEnabled:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(CONFIG.gpic, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(CONFIG.gvid, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(CONFIG.gpir, GPIO.IN)
            except:
                self.logger.error("could not set the GPIOs. \n")
                self.alreadyLoggedGPIOError = True
        else:
            self.logger.info("Would have setup the GPIO-Ports now.")

        fullname = os.path.join(CONFIG.core_data, CONFIG.initial_image)
        #fullname = CONFIG.core_data + "/" + CONFIG.initial_image
        self.logger.debug('PIcBrick initialized - displaying start picture ' + str(fullname))
        myTFT.display_image(myScreen, fullname)
        self.logger.info('Ready to take pictures, videos or wait for the bad guys')

        while True:
            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.
            clock.tick(10)

            if CONFIG.gpioEnabled:
                try:
                    input_state_pic = GPIO.input(CONFIG.gpic)
                    input_state_vid = GPIO.input(CONFIG.gvid)
                    input_state_pir = GPIO.input(CONFIG.gpir)
                except:
                    if (self.alreadyLoggedGPIOError==False):
                        self.logger.error("could not watch GPIO-ports, we should bail out here")
                        self.alreadyLoggedGPIOError = True
                    raise Exception("could not watch GPIO-ports, we should bail out here")
            else:
                self.logger.info("Would have setup the GPIO-Ports now.")

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
                e = sys.exc_info()[1]
                t = sys.exc_info()[0]
                self.logger.error("could not process input event. \n Error was: " + str(e) + " / " + str(t))
                sys.exit(-1)

        if CONFIG.gpioEnabled:
            try:
                GPIO.cleanup()
            except:
                self.logger.error("could not clean GPIO")
        else:
            self.logger.info("Would have cleaned the GPIO-Ports now.")

if __name__ == '__main__':
    print "PIcBrick started ... "
    pib = picbrick()
    pib.getCommandLineArguments(sys.argv)
    pib.run()

