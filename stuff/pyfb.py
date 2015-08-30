import os
import pygame

disp_no = os.getenv('DISPLAY')
if disp_no:
    print "I'm running under X display = {0}".format(disp_no)

driver = 'directfb'
drivers = ['directfb', 'fbcon', 'svgalib']

found = False
for driver in drivers:
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
    try:
        pygame.display.init()
    except pygame.error:
        print 'Driver: {0} failed.'.format(driver)
        continue
    found = True
    break

if not found:
   raise Exception('No suitable video driver found!')
else:
   print "using " + str(driver) + " as video driver"

