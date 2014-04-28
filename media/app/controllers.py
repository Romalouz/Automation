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
from media.andro.manager import AndroManager

# Define the blueprint: 'app', set its url prefix: app.url/
app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    """Call main page to control devices"""
    #Call devices manager objects and read their status
    receiver = ReceiverManager()
    receiver.read_status()
    tv = TvManager()
    tv.read_status()
    devices = {"receiver" : receiver.__dict__, "tv" : tv.__dict__ }
    return render_template("index.html", title = 'Home', devices = devices)

@app.route('test', methods = ['POST'])
def test():
    """Test route for anything"""
    #Used for test purpose
    AndroManager().send_message(request.form['message'])
    return "Done"