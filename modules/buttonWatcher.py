__author__ = 'chris'


import event as Event
import Logger
import config_simple as CONFIG

class fileWatcher:
    def __init__(self, button=None):
        self.logger = Logger.Logger(self.__class__.__name__).get()
        self.logger.debug("initializing buttonWatcher event handler for button " + str(button))
        self.buttonTriggered = Event()

        self.watchButton(button)

    def watchButton(self, button, state=False):
        if state:
            self.logger.debug("button " + button + " fired an event")