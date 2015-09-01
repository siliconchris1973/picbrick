# picbrick
The Picture Brick - a Raspberry PI system to take photos and videos controlled by a python program

It is possibly best to clone this release in /opt via 
  git clone https://github.com/siliconchris1973/picbrick

PicBrick is intened to be run via a call in /etc/rc.local on your Raspberry Pi such as
  /opt/picbrick/picbrick.py

It will display a nicwe HAL9000 eye on the framebuffer and watch two buttons - one to take a photo and one to take a video.
After taking a photo, it will automatically display that image on the framebuffer device for a configurable amount of time, 
or until you press one of the buttons again.

All configuration can be done in the file config.py in the modules directory.

It also supports an automatic mode in which it will watch a third GPIO port. To this you may connect an infrared motion
detector. When in automatic mode, the picbrick will take a phot AND a video (default 10 seconds) and will send an SMS
vis the smspi.co.uk sevice.

picbrick expects a os variable smsHash containing the hash provided from smspi.co.uk.


