#!/usr/bin/env python
__author__ = 'chris'

import urllib
import urllib2
import syslog


class sms:
    # sms-service
    #
    #Replace the xxxxxxx with the number you wish to text.
    to = "+4915112240942"
    #Replace the xxxxxx with the hash given to you by smspi.co.uk
    hash = "bfd626d66e9ca13b1f21843725f2eef2"

    def __init__(self, message):
        values = {
              'to' : self.to,
              'message' : message,
              'hash' : self.hash }

        url = 'http://www.smspi.co.uk/send/'

        postdata = urllib.urlencode(values)
        req = urllib2.Request(url, postdata)

        syslog.syslog('Attempt to send SMS ...')

        try:
            response = urllib2.urlopen(req)
            response_url = response.geturl()
            if response_url==url:
                syslog.syslog(response.read())
        except urllib2.URLError, e:
            syslog.syslog(syslog.LOG_ERR, 'Send failed!' + e.reason)