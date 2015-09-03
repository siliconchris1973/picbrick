# PIcBrick
The PI Picture Brick - a Raspberry PI photo system named brick, because the first case I
build for it, roughly resembled the dimensions of a brick stone :-)


PIcBrick will display a nice HAL9000 eye on the framebuffer and watch two buttons - one to take a
photo and one to take a video. After taking a photo, it will automatically display that image
on the framebuffer device /dev/fb1 for a configurable amount of time, or until you press either
of the buttons again.

It also supports an automatic mode in which it will watch a third GPIO port. To this you may
connect an infrared motion detector. When in automatic mode, the picbrick will take a photo AND
a video (default 10 seconds) and will send an SMS via the smspi.co.uk service.


It is possibly best to clone this release in /opt via 
  git clone https://github.com/siliconchris1973/picbrick

PicBrick is intended to be run via a call in /etc/rc.local on your Raspberry Pi such as
  /opt/picbrick/picbrick.py
or
  /opt/picbrick/start.sh

As PIcBrick needs access to the framebuffer device and to the GPIO ports, it is probably best
to run it as root.


All configuration can be done in the file config_simple.py in the modules directory. The file
should be pretty self explanatory. The most important settings are those for the screen and picture
sizes.


If you want to make full use of the automatic mode, PIcBrick will need access to a cloud sms service
from smspi.co.uk. The service is protected with a hash key and this key is expected to be present as
an operation system environment variable smsHash.
The variable can be set in the file env/environment (a file not present in the github repository) or
as a normal env variable on the start line of picbrick.py.
If you opt for the environment file, then you can use the start.sh shell script to start PIcBrick.
in the other case you would call the application like this:

  env smsHash=YOURHASHKEYFROMSMSPI picbrick.py



The PIcBrick is written entirely in python and makes use of a number of libraries, such as
* pygame
* picamera
* RPI.GPIO


