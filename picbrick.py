#!/usr/bin/env python
__author__ = 'chris'


from modules import display
from modules import pictureviewer
import sys


def main(argv):
    d = display.pbScreen()
    print 'display is ' + str(d)

    i = pictureviewer.picView()

    d.show_controls()

if __name__ == '__main__':
    main(sys.argv)

