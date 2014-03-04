#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: controllers.py
#	Package: Receiver
#   Author: Romain Gigault
#   Date: 21-Fev-2014
#   Info: Communicate with receiver devices via HTTP GET / POST requests
from media import media
from flask import render_template, request, Blueprint
import datetime
from media.receiver.model import Txnr509
import media.receiver.manager


myonkyo = Txnr509(host="192.168.1.11")

# Define the blueprint: 'receiver', set its url prefix: app.url/receiver
receiver = Blueprint('receiver', __name__, url_prefix='/receiver')

@receiver.route('/index')
def index():
	user = { 'nickname': 'Miguel' } # fake user
	posts = [ # fake array of posts
	    { 
	        'author': { 'nickname': 'John' }, 
	        'body': 'Beautiful day in Portland!' 
	    },
	    { 
	        'author': { 'nickname': 'Susan' }, 
	        'body': 'The Avengers movie was so cool!' 
	    }
	]
	return render_template("index.html", title = 'Home', user = user, posts = posts)

@receiver.route('/radio/<string:freq>', methods = ['GET'])
def power_radio(freq):
	myonkyo.set_fm(freq)
	return 'Ok'

@receiver.route('/set_input/<string:input_data>', methods = ['GET'])
def set_onkyo_input(input_data):
	myonkyo.command('input-selector {inp}'.format(inp=input_data))
	return 'Ok'

@receiver.route('/power/<string:power_data>', methods = ['GET'])
def set_onkyo_power(power_data):
	myonkyo.power(power_data)
	return 'Ok'

@receiver.route('/volume/<int:vol>', methods = ['GET'])
def set_onkyo_volume(vol):
	myonkyo.set_volume(vol)
	return 'Ok'