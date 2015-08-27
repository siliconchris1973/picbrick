#!/usr/bin/env python

import os
from time import sleep
import pygame
from pygame.locals import *

# directory structure
core_data = 'data'
image_dir = 'images'
video_dir = 'videos'
initial_image = 'HAL900_320x240.png'


class picView:
    # This function takes the name of an image to load.
    # It also optionally takes an argument it can use to set a colorkey for the image.
    # A colorkey is used in graphics to represent a color of the image that is transparent.
    # we also use this this function to initialize filenav.py -- see modules
    def load_image(self, directory, filename, colorkey=None):
        fullname = os.path.join(directory, filename)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', filename
            raise SystemExit, message
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()


    def run(self, done=False):
        self.load_image(core_data, self.current_image)

        while not done:
            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.
            sleep(1)



    def __init__(self):
        self.current_image = initial_image
        self.run()

