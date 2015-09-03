#!/usr/bin/env python
__author__ = 'chris'

import syslog
import pygame
import os
import config_simple as CONFIG

class display:
    screenWidth = CONFIG.screenWidth
    screenHeight = CONFIG.screenHeight
    screenSize = (screenWidth, screenHeight)
    backgroundColor = CONFIG.backgroundColor

    def __init__(self, width=CONFIG.screenWidth, height=CONFIG.screenHeight):
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

        screen.fill(CONFIG.backgroundColor)
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
            image = pygame.image.load(filename)
        except:
            syslog.syslog("Unable to find the image "+filename+" :-( ")

        screen.blit(image,(0,0))
