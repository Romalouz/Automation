#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: controllers.py
#	Package: Receiver
#   Author: Romain Gigault
#   Date: 17-Sept-2014
#   Info: First test to communicate with arduino
from media import media
from flask import render_template, request, Blueprint, jsonify
from media.arduino.model import ArduinoModel

# Define the blueprint: 'light', set its url prefix: app.url/light
arduino = Blueprint('arduino', __name__, url_prefix='/arduino')

@arduino.route('/light/<string:device>/<string:status>', methods = ['GET'])
def power_light(device,status):
    """Set light on or off"""
    #TODO fix broken pipe error
    myLight = ArduinoModel(media.config.get("AD_PORT_VAL"))
    data = myLight.switch_status(device,status)
    del myLight
    return data

@arduino.route('/killThread', methods = ['GET'])
def kill_thread():
    "Test routine to kill arduino thread"
    global arduino_thread
    arduino_thread.stop()
    if arduino_thread.isAlive():
        return 'Nok'
    else:
        return 'OK'