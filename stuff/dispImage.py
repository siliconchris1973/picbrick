#!/usr/bin/env python

import os, pygame, time

class pyscope :
    # class def. from http://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer
    # blah, blah...
    
    scope = pyscope()
    image1 = pygame.image.load('test.jpg').convert()
    isize = image1.get_size()
    dsize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    xp = (dsize[0] - isize[0]) / 2  # find location to center image on screen
    yp = (dsize[1] - isize[1]) / 2
    scope.screen.blit(image1,(xp,yp))
    pygame.display.update()
    time.sleep(3)

