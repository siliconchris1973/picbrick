#!/usr/bin/env python
__author__ = 'chris'

import urllib
import urllib2
import os
import Logger


class sms:
    # sms-service
    #
    #Replace the xxxxxxx with the number you wish to text.
    to = "+4915112240942"
    def __init__(self, message):
        self.logger = Logger.Logger(self.__class__.__name__).get()
        hash = os.environ["environment"]
        self.logger.debug("initializing sms service with os environment " + str(hash))

        values = {
              'to' : self.to,
              'message' : message,
              'hash' : self.hash }

        url = 'http://www.smspi.co.uk/send/'

        postdata = urllib.urlencode(values)
        req = urllib2.Request(url, postdata)

        self.logger.info('Attempting to send SMS ...')
        self.logger.debug("  postdata: " + str(postdata))
        self.logger.debug("  req: " + str(req))

        try:
            response = urllib2.urlopen(req)
            response_url = response.geturl()
            if response_url==url:
                self.logger.debug(response.read())
        except urllib2.URLError, e:
            self.logger.error('Send failed!' + e.reason)

if __name__ == '__main__':
    print "smsService.py is NOT intended to be started from command line  ... "
