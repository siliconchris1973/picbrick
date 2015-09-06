#!/usr/bin/env python
__author__ = 'chris'

import json

import logger


class configuration:
    def __init__(self):
        self.logger = logger(self.__class__.__name__).get()
        self.logger.debug("importing json configuration file config.json")
        with open('config.json') as json_data_file:
            self.data = json.load(json_data_file)

        config = json.loads(open('config.json').read())
        self.logger.debug("configuration is " + str(config))

    def print_config(self):
        print "\n\nThis is the configuration class of the picbrick. It is usually not intended to be invoked by itself.\n" \
          "For your \"convenients\" it will print the configuration if you do invoke it directly. So here it comes:\n\n"
        print(self.data)

if __name__ == "__main__":
    config = configuration()
    config.print_config()