#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: views.py
#	Package: Receiver
#   Author: Romain Gigault
#   Date: 21-Fev-2014
#   Info: Communicate with receiver devices via HTTP GET / POST requests
from media import media
from flask import render_template, request, Blueprint
import datetime
from media.tv.model import BSeriesSender
import media.tv.manager

mysamsung = BSeriesSender(host="192.168.1.15")

# Define the blueprint: 'tv', set its url prefix: app.url/tv
tv = Blueprint('tv', __name__, url_prefix='/tv')

@tv.route('/sms', methods = ['GET','POST'])
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