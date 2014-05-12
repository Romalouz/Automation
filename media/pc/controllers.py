#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: controllers.py
#	Package: Pc
#   Author: Romain Gigault
#   Date: 27-Apr-2014
#   Info: Applcation views dispatching 
from media import media
from flask import render_template, request, Blueprint
from media.pc.manager import PCManager

# Define the blueprint: 'app', set its url prefix: app.url/
pc = Blueprint('pc', __name__, url_prefix='/pc')

@pc.route('/wol/')
def wol():
    """Send WOL command on network with target PC_MAC_ADDRESS from config"""
    if not(PCManager().wake_on_lan(media.config.get("PC_MAC_ADDRESS"))):
        return "OK"
    else:
        return "NoK"
