#!/usr/bin/env python
__author__ = 'chris'

import sys

from broken import display
from modules import pictureviewer


def main(argv):
    d = display.pbScreen()
    print 'display is ' + str(d)

    i = pictureviewer.picView()

    d.show_controls()

if __name__ == '__main__':
    main(sys.argv)

