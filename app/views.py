#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: __init__.py
#   Author: Romain Gigault
#   Date: 21-Fev-2014
#   Info: Communicate with devices via HTTP GET / POST requests
from app import app
from flask import render_template
import datetime
from .helper import TXNR509
from .helper import TVRemote

myonkyo = TXNR509.Txnr509(host="192.168.1.11")
mysamsung = TVRemote.BSeriesSender(host="192.168.1.15")


@app.route('/index')
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

@app.route('/SMS/<string:datestr>/<string:timestr>/<string:rnumber>/<string:rname>/<string:snumber>/<string:sname>/<string:message>', methods = ['GET'])
def sms_to_tv(datestr, timestr, rnumber, rname, snumber, sname, message):
	#format date and time
	datestr = datetime.datetime.strptime(datestr, "%d-%m-%Y")
	timestr = datetime.datetime.strptime(timestr, "%H.%M")
	error_found = mysamsung.post_sms(datestr.strftime("%Y-%m-%d"), timestr.strftime("%H:%M:%S"), rnumber, rname, snumber, sname, message)
	return error_found

@app.route('/ONKYO/radio/<string:freq>', methods = ['GET'])
def power_radio(freq):
	myonkyo.set_fm(freq)
	return 'Ok'

@app.route('/ONKYO/set_input/<string:input_data>', methods = ['GET'])
def set_input(input_data):
	myonkyo.command('input-selector {inp}'.format(inp=input_data))
	return 'Ok'