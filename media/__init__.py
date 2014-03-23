#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: __init__.py
#   Author: Romain Gigault
#   Date: 21-Fev-2014
#   Info: Communicate with devices via HTTP GET / POST requests  
from flask import Flask, jsonify
from flask_bootstrap import Bootstrap

#debugging purpose
#import ptvsd
#import os


media = Flask(__name__)
Bootstrap(media)

#DEBUG Trick to start debug env
#try:
#    print(os.environ['DEBUG_FOR_FLASK'])
#except:
#    print('Create Variable')
#    os.environ['DEBUG_FOR_FLASK'] = '1'
#    print(os.environ['DEBUG_FOR_FLASK'])
#    pass

# Configurations
media.config.from_object('media.config')

# Import a module / component using its blueprint handler variable
from media.receiver.controllers import receiver as receiver_module
from media.tv.controllers import tv as tv_module
from media.app.controllers import app as app_module

# Register blueprint(s)
media.register_blueprint(receiver_module)
media.register_blueprint(tv_module)
media.register_blueprint(app_module)

#DEBUG
#os.environ['DEBUG_FOR_FLASK'] = str(int(os.environ['DEBUG_FOR_FLASK'])+1)
##ptvsd.enable_attach(secret = media.config.get('DEBUG_SECRET'), address = ('0.0.0.0', int(media.config.get('DEBUG_PORT'))))
#if (int(os.environ['DEBUG_FOR_FLASK']) >= 2):
#    print ('In debug mode....')
#    ptvsd.enable_attach(secret = 'test')#, address = ('192.168.1.16', 8090))
# app.register_blueprint(xyz_module)
# ..