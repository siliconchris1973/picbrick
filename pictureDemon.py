#!/usr/bin/env python

import RPi.GPIO as GPIO
import picamera
import datetime
import time
import urllib
import urllib2
import sys
import string
import syslog

# define some global vars
#Replace the xxxxxxx with the number you wish to text.
to = "+4915112240942"
#Replace the xxxxxx with the hash given to you by smspi.co.uk
hash = "bfd626d66e9ca13b1f21843725f2eef2"

# GPIO ports
gpic = 21     # GPIO pin connected to the take a picture button
gvid = 20     # GPIO pin connected to the take a video button
gpir = 16     # GPIO pin connected to the PIR

# define what to do on each event type picture_button, video_button or PIR
picTakePicture = True
picTakeVideo = False
picSendSms = False

vidTakePicture = False
vidTakeVideo = True
vidSendSms = False

pirTakePicture = True
pirTakeVideo = True
pirSendSms = False

waitTimeAfterPicture = 2
waitTimeAfterVideo = 0
waitTimeAfterEvent = 5

videoDuration = 10

imageDir = "/usr/local/var/picture_brick/images"
videoDir = "/usr/local/var/picture_brick/videos"


##### NO NEED TO CHANGE ANYTHING BELOW HERE #####

# these three are set accoridng to event (picture- or video button or PIR)
takeVideo = False
takePicture = False
sendSms = False

eventSource = "NULL"

# setup everything
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpic, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gvid, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpir, GPIO.IN)
camera = picamera.PiCamera()


def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
Uses a whitelist approach: any characters not present in valid_chars are
removed. Also spaces are replaced with underscores.
 
Note: this method may produce invalid filenames such as ``, `.` or `..`
When I use this method I prepend a date string like '2009_01_15_19_46_32_'
and append a file extension like '.txt', so I avoid the potential of using
an invalid filename.
 
"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename


### sms sending
def sms(to,message,hash):
    values = {
          'to' : to,
          'message' : message,
          'hash' : hash } # Grab your hash from http://www.smspi.co.uk
     
    url = 'http://www.smspi.co.uk/send/'
     
    postdata = urllib.urlencode(values)
    req = urllib2.Request(url, postdata)
     
    syslog.syslog('Attempt to send SMS ...')
     
    try:
        response = urllib2.urlopen(req)
        response_url = response.geturl()
        if response_url==url:
            print response.read()
    except urllib2.URLError, e:
        syslog.syslog(syslog.LOG_ERR, 'Send failed!' + e.reason)



syslog.syslog('Ready to take pictures, videos or wait for the bad guys')

while True:
    input_state_pic = GPIO.input(gpic)
    input_state_vid = GPIO.input(gvid)
    input_state_pir = GPIO.input(gpir)
    
    if input_state_pic == False or input_state_vid == False or input_state_pir == True:
        if input_state_pic == False:
            takePicture = picTakePicture
            takeVideo = picTakeVideo
            sendSms = picSendSms
            waitTimeAfterPicture = 0
            waitTimeAfterVideo = 0
            waitTimeAfterEvent = 0
            eventSource = "picture_button"
        elif input_state_vid == False:
            takePicture = vidTakePicture
            takeVideo = vidTakeVideo
            sendSms = vidSendSms
            waitTimeAfterPicture = 0
            waitTimeAfterVideo = 0
            waitTimeAfterEvent = 0
            eventSource = "video_button"
        elif input_state_pir == True:
            takePicture = pirTakePicture
            takeVideo = pirTakeVideo
            sendSms = pirSendSms
            waitTimeAfterPicture = 2
            waitTimeAfterVideo = 0
            waitTimeAfterEvent = 5
            eventSource = "PIR motion detector"
        else:
            takePicture = False
            takeVideo = False
            sendSms = False
            waitTimeAfterPicture = 0
            waitTimeAfterVideo = 0
            waitTimeAfterEvent = 5
            eventSource = "unknown"
         
        a = datetime.datetime.now()
        a = str(a)
        a = a[0:19]
        b = format_filename(a)
         
        txtmessage = ("captured event (" + eventSource + ")  at "+str(a))
        syslog.syslog(txtmessage)
        pic = (imageDir)+("/img_")+(b)+(".jpg")
        vid = (videoDir)+("/vid_")+(b)+(".h264")
        
        message = (txtmessage),(pic),(vid)
        
        if takePicture:
            #camera.resolution = (1024, 768)
            camera.resolution = (320, 240)
            camera.capture(pic)
            syslog.syslog("picture taken, waiting " + str(waitTimeAfterPicture) + " seconds...")
            time.sleep(waitTimeAfterPicture)
        
        if takeVideo:
            camera.resolution = (640, 480)
            camera.start_recording(vid)
            camera.wait_recording(videoDuration)
            camera.stop_recording()
            syslog.syslog(str(videoDuration) + " seconds of video taken, waiting " + str(waitTimeAfterVideo) + " seconds...")
            time.sleep(waitTimeAfterVideo)
        
        if sendSms:
            sms(to,message,hash)
         
         
         
        syslog.syslog("event processed, waiting " + str(waitTimeAfterEvent) + " seconds...")
        time.sleep(waitTimeAfterEvent)
        
        syslog.syslog("all done, waiting for next event...")

GPIO.cleanup()

