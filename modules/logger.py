#!/usr/bin/env python
__author__ = 'chris'
import os
import sys
import logging
import config_simple as CONFIG

class Logger(object):

    def __init__(self, name):

        name = name.replace('.log','')
        logger = logging.getLogger('log.%s.py' % name)
        logger.setLevel(CONFIG.log_level)

        if not logger.handlers:
            file_name = os.path.join(CONFIG.logging_dir, '%s.log' % name)
            handler = logging.FileHandler(file_name)
            formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s %(message)s')
            handler.setFormatter(formatter)
            handler.setLevel(CONFIG.log_level)
            logger.addHandler(handler)

        if CONFIG.printLogToConsole:
            ch = logging.StreamHandler(sys.stdout)
            ch.setLevel(CONFIG.log_level)
            formatter_ch = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter_ch)
            logger.addHandler(ch)

        self._logger = logger

    def get(self):
        return self._logger