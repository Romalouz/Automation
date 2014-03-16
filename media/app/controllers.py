#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: controllers.py
#	Package: App
#   Author: Romain Gigault
#   Date: 09-Mar-2014
#   Info: Applcation views dispatching 
from media import media
from flask import render_template, request, Blueprint
from media.receiver.manager import ReceiverManager
from media.tv.manager import TvManager

# Define the blueprint: 'app', set its url prefix: app.url/
app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    #Call devices manager objects and read their status
    receiver = ReceiverManager()
    receiver.read_status()
    tv = TvManager()
    tv.read_status()
    devices = {"receiver" : receiver.__dict__, "tv" : tv.__dict__ }
    return render_template("index.html", title = 'Home', devices = devices)