#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: __init__.py
#   Author: Romain Gigault
#   Date: 21-Fev-2014
#   Info: Communicate with devices via HTTP GET / POST requests 
from flask import Flask, jsonify

media = Flask(__name__)

# Configurations
media.config.from_object('media.config')

# Import a module / component using its blueprint handler variable
from media.receiver.controllers import receiver as receiver_module
from media.tv.controllers import tv as tv_module

# Register blueprint(s)
media.register_blueprint(receiver_module)
media.register_blueprint(tv_module)
# app.register_blueprint(xyz_module)
# ..