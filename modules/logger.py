#!/usr/bin/env python
__author__ = 'chris'
import os
import logging
import config_simple as CONFIG

class Logger(object):

    def __init__(self, name):
        name = name.replace('.log','')
        logger = logging.getLogger('log.%s' % name)
        #logger.setLevel(logging.DEBUG)
        logger.setLevel(CONFIG.log_level)
        if not logger.handlers:
            file_name = os.path.join(CONFIG.logging_dir, '%s.log' % name)
            handler = logging.FileHandler(file_name)
            formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s %(message)s')
            handler.setFormatter(formatter)
            handler.setLevel(CONFIG.log_level)
            logger.addHandler(handler)
        self._logger = logger

    def get(self):
        return self._logger