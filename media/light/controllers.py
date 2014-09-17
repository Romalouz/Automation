#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: controllers.py
#	Package: Receiver
#   Author: Romain Gigault
#   Date: 17-Sept-2014
#   Info: First test to communicate with arduino
from media import media
from flask import render_template, request, Blueprint, jsonify
from media.light.model import LightModel

# Define the blueprint: 'light', set its url prefix: app.url/light
light = Blueprint('light', __name__, url_prefix='/light')

@light.route('/<string:device>/<string:status>', methods = ['GET'])
def power_light(device,status):
    """Set light on or off"""
    #TODO fix broken pipe error
    myLight = LightModel(media.config.get("AD_PORT_VAL"))
    data = myLight.switch_status(device,status)
    del myLight
    return data
    

