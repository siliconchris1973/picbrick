#!/usr/bin/env python

import os
import pygame
from pygame.locals import *
from modules import filenav

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
btnF1_col = cyan
btnF2_col = blue
btnF3_col = red
btnF4_col = green
btnF5_col = cyan


# directory structure
core_data = 'data'
image_dir = 'images'
video_dir = 'videos'
initial_image = 'HAL900_320x240.png'


"""
    Screen layout:

    |------------- 320 -------------|

                C y c l e
    +-------------------------------+        ---
 20 |### ####################### ###| 20      |
    |###                         ###|         |
    |###                         ###|         |
 P  |###                         ###| N       |
 R  |###                         ###| E      240
 E  |###                         ###| X       |
 V  |###                         ###| T       |
    |###                         ###|         |
    |###                         ###|         |
    |### ### ### ### ### ### ### ###|         |
    +-------------------------------+        ---
     40   F1  F2  F3  F4  F5  F6  40

"""
#screen size
width = 320
height = 240
size = (width, height)

# button definitions
# pressed button 21, 219
number_of_x_buttons = 5
number_of_y_buttons = 2
btn_width = 40
btn_height = 40
safetyMargin = 2

# evenly distribute function buttons
btnDistance_x = ((width - 2 * btn_width) - (number_of_x_buttons * btn_width)) / (number_of_x_buttons + 1)
btnDistance_y = ((height - btn_height) - (number_of_y_buttons * btn_height)) / (number_of_y_buttons + 1)

# these are the two big area to "scroll" left and right
btnPrev_x = 0
btnPrev_y = safetyMargin
btnPrev_width = btn_width
btnPrev_height = height - safetyMargin

btnNext_x = width - btn_width
btnNext_y = safetyMargin
btnNext_width = btn_width
btnNext_height = height - safetyMargin

btnCycle_x = 0 + (btn_width + safetyMargin)
btnCycle_y = 0
btnCycle_width = width - (2 * btn_width + 2 * safetyMargin)
btnCycle_height = btn_height

btnF1_x = 0 + (btn_width + safetyMargin)
btnF1_y = height - btn_height
btnF1_width = btn_width
btnF1_height = btn_height

btnF2_x = btnF1_x + btnDistance_x
btnF2_y = height - btn_height
btnF2_width = btn_width
btnF2_height = btn_height / 2

btnF3_x = btnF2_x + btnDistance_x
btnF3_y = height - btn_height
btnF3_width = btn_width
btnF3_height = btn_height / 2

btnF4_x = btnF3_x + btnDistance_x
btnF4_y = height - btn_height
btnF4_width = btn_width
btnF4_height = btn_height / 2

btnF5_x = btnF4_x + btnDistance_x
btnF5_y = height - btn_height
btnF5_width = btn_width
btnF5_height = btn_height / 2

# initialize pyGame and the screen
pygame.init()
screen = pygame.display.set_mode(size)
screen.fill((black))

touch_buttons = {
    'btnPrev.png':(btnPrev_x, btnPrev_y, btnPrev_width, btnPrev_height)     # Previous image button
    ,'btnNext.png':(btnNext_x,btnNext_y,btnNext_width, btnNext_height)      # Next image button
    ,'btnCycle.png':(btnCycle_x,btnCycle_y,btnCycle_width, btnCycle_height) # Cycle screen button
    ,'btnF1.png':(btnF1_x,btnF1_y,btnF1_width, btnF1_height)                # function 1 button
    ,'btnF1.png':(btnF2_x,btnF2_y,btnF2_width, btnF2_height)                # function 2 button
    ,'btnF1.png':(btnF3_x,btnF3_y,btnF3_width, btnF3_height)                # function 3 button
    ,'btnF1.png':(btnF4_x,btnF4_y,btnF4_width, btnF4_height)                # function 4 button
    ,'btnF5.png':(btnF5_x,btnF5_y,btnF5_width, btnF5_height)                # function 5 button
}


# functions
def prev_picture():
    print 'prev picture called'

    display_image(s.previous)

def next_picture():
    print 'next picture called'

    display_image(s.next)

def cycle_function():
    print 'cycle function called'

def display_image(directory, filename):
    try:
        # load from subfolder 'data'
        img = pygame.image.load(os.path.join(directory,filename))
    except:
        raise UserWarning, "Unable to find the images in the folder 'data' :-( "
    screen.blit(img,(0,0))


# This function takes the name of an image to load.
# It also optionally takes an argument it can use to set a colorkey for the image.
# A colorkey is used in graphics to represent a color of the image that is transparent.
# we also use this this function to initialize filenav.py -- see modules
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def show_controls():
    # Draw a rectangle outline
    pygame.draw.rect(screen, btnPrev_col, [btnPrev_x, btnPrev_y, btnPrev_width, btnPrev_height], 2)
    #pygame.blit(source, dest, area=None, special_flags = 0) -> Rect

    pygame.draw.rect(screen, btnNext_col, [btnNext_x, btnNext_y, btnNext_width, btnNext_height], 2)
    pygame.draw.rect(screen, btnCycle_col, [btnCycle_x, btnCycle_y, btnCycle_width, btnCycle_height], 2)

    #pygame.draw.rect(screen, btnF1_col, [btnF1_x, btnF1_y, btnF1_width, btnF1_height], 2)
    #pygame.draw.rect(screen, btnF2_col, [btnF2_x, btnF2_y, btnF2_width, btnF2_height], 2)
    #pygame.draw.rect(screen, btnF3_col, [btnF3_x, btnF3_y, btnF3_width, btnF3_height], 2)
    #pygame.draw.rect(screen, btnF4_col, [btnF4_x, btnF4_y, btnF4_width, btnF4_height], 2)
    #pygame.draw.rect(screen, btnF5_col, [btnF5_x, btnF5_y, btnF5_width, btnF5_height], 2)

    """
    for i,v in touch_buttons.items():
        btn_image = pygame.image.load(os.path.join('data', i))
                                #  X     Y     W     H
        rect = btn_image.set_rect(v[0], v[1], v[2], v[3])
        screen.blit(btn_image, rect)
    """

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

def hide_controls():
    display_image(core_data, current_image)

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()


def get_display():
    disp_no = os.getenv('DISPLAY')
    if disp_no:
        print "I'm running under X display = {0}".format(disp_no)
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
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            print "I'm running on the framebuffer using driver " + str(driver)
            pygame.mouse.set_visible(False)
            break

        if not found:
            raise Exception('No suitable video driver found!')


    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
    os.environ["SDL_MOUSEDRV"] = "TSLIB"


def run_me(done, toggle_controls):
    display_image(core_data, current_image)

    show_controls()

    while not done:
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)

        # Scan touchscreen events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if(event.type is MOUSEBUTTONDOWN):
                # get list of images in picture folder

                pos = pygame.mouse.get_pos()
                # Find which quarter of the screen we're in
                x,y = pos
                print 'pos is ' + str(pos)

                # check which button was pressed
                if btnPrev_x <= x <= btnPrev_x + btnPrev_width and btnPrev_y <= y <= btnPrev_y + btnPrev_height:
                    prev_picture()
                elif btnNext_x <= x <= btnNext_x + btnNext_width and btnNext_y <= y <= btnNext_y + btnNext_height:
                    next_picture()
                elif btnCycle_x <= x <= btnCycle_x + btnCycle_width and btnCycle_y <= y <= btnCycle_y + btnCycle_height:
                    cycle_function()
                else:
                    print 'event outside of control buttons'

                    if (toggle_controls == True):
                        toggle_controls = False

                        print 'showing controls'
                        show_controls()
                    else:
                        toggle_controls = True
                        print 'hiding controls'

                    # Go ahead and update the screen with what we've drawn.
                    # This MUST happen after all the other drawing commands.
                    pygame.display.flip()
            elif(event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()


if __name__ == "__main__":
    s = filenav.FileNav(image_dir)

    done = False
    toggle_controls = True

    get_display()

    #define font
    font = pygame.font.Font(None, 20)
    font_big = pygame.font.Font(None, 50)

    pygame.display.update()
    current_image = initial_image
    clock = pygame.time.Clock()

    #background = pygame.Surface(screen.get_size())
    #background = background.convert()
    #background.fill((black))

    run_me(done, toggle_controls)

    # Be IDLE friendly
    pygame.quit()