#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: __init__.py
#   Author: Romain Gigault
#   Date: 21-Fev-2014
#   Info: Communicate with devices via HTTP GET / POST requests 
from media import media
from media.arduino.model import ArduinoThread
from time import sleep

#Start Arduino thread before starting webserver
arduino_thread = ArduinoThread(iface_address = media.config.get("AD_PORT_VAL"), timer =  media.config.get("DETECTION_TIME"))
sleep(1)
if arduino_thread.isAlive():
    print('Thread is running')
media.run(host='0.0.0.0', port=3000, debug=True, use_reloader=False)

#Kill thread
arduino_thread.stop()
sleep(1)
if(not arduino_thread.isAlive()):
    print "Exiting web server and Arduino thread"
