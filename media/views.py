#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: __init__.py
#   Author: Romain Gigault
#   Date: 21-Fev-2014
#   Info: Communicate with devices via HTTP GET / POST requests
from media import media
from flask import render_template, request
import datetime
from .helper import *

myonkyo = TXNR509.Txnr509(host="192.168.1.11")
mysamsung = TVRemote.BSeriesSender(host="192.168.1.15")


@media.route('/media/index')
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

# @media.route('/SMS/<string:datestr>/<string:timestr>/<string:rnumber>/<string:rname>/<string:snumber>/<string:sname>/<string:message>', methods = ['GET'])
# def sms_to_tv(datestr, timestr, rnumber, rname, snumber, sname, message):
@media.route('/tv/sms', methods = ['GET','POST'])
def sms_to_tv():
	if request.method == 'GET':
		return render_template("sms.html", title = 'SMS')
	elif request.method == 'POST':
		#format date and time
		rdate = datetime.datetime.strptime(request.form['rdate'], "%d-%m-%Y")
		rtime = datetime.datetime.strptime(request.form['rtime'], "%H.%M")
		error_found = mysamsung.post_sms(rdate.strftime("%Y-%m-%d"), \
			                             rtime.strftime("%H:%M:%S"), \
			                             request.form['rnumber'], \
			                             request.form['rname'], \
			                             request.form['snumber'], \
			                             request.form['sname'], \
			                             request.form['mbody'])
		return 'Not OK' if error_found else 'OK'

@media.route('/onkyo/radio/<string:freq>', methods = ['GET'])
def power_radio(freq):
	myonkyo.set_fm(freq)
	return 'Ok'

@media.route('/onkyo/set_input/<string:input_data>', methods = ['GET'])
def set_onkyo_input(input_data):
	myonkyo.command('input-selector {inp}'.format(inp=input_data))
	return 'Ok'

@media.route('/onkyo/power/<string:power_data>', methods = ['GET'])
def set_onkyo_power(power_data):
	myonkyo.power(power_data)
	return 'Ok'

@media.route('/onkyo/volume/<int:vol>', methods = ['GET'])
def set_onkyo_volume(vol):
	myonkyo.set_volume(vol)
	return 'Ok'