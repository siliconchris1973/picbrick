#!/usr/bin/env python

import os
import pygame

class pbScreen:
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


    def show_controls(self):
        # Draw a rectangle outline
        pygame.draw.rect(self.screen, self.btnPrev_col, [self.btnPrev_x, self.btnPrev_y, self.btnPrev_width, self.btnPrev_height], 2)
        pygame.draw.rect(self.screen, self.btnNext_col, [self.btnNext_x, self.btnNext_y, self.btnNext_width, self.btnNext_height], 2)
        pygame.draw.rect(self.screen, self.btnCycle_col, [self.btnCycle_x, self.btnCycle_y, self.btnCycle_width, self.btnCycle_height], 2)

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

    def hide_controls(self):
        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()


    def get_display(self):
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

    def __init__(self, width=320, height=240):
        self.width = width
        self.height = height

        self.clock = pygame.time.Clock()

        self.get_display()
