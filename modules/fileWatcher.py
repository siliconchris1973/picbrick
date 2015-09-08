#!/usr/bin/env python
__author__ = 'chris'

import event as Event
import Logger
import config_simple as CONFIG

class fileWatcher:
    def __init__(self, directory=None):
        self.logger = Logger.Logger(self.__class__.__name__).get()
        self.logger.debug("initializing fileWatcher event handler")
        self.fileChanged = Event()
        if directory <> None:
            self.watchFiles(directory)

    def watchFiles(self, directory):
        source_path = directory
        self.fileChanged(source_path)

