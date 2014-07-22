#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: views.py
#	Package: Receiver
#   Author: Romain Gigault
#   Date: 21-Fev-2014
#   Info: Communicate with receiver devices via HTTP GET / POST requests
from media import media
from flask import render_template, request, Blueprint, jsonify
import datetime
from media.tv.manager import TvManager

# Define the blueprint: 'tv', set its url prefix: app.url/tv
tv = Blueprint('tv', __name__, url_prefix='/tv')

@tv.route('/sms/', methods = ['GET','POST'])
def sms_to_tv():
	"""Method GET present a test form to send SMS
	Method POST will display SMS on TV from form data"""
	if request.method == 'GET':
		return render_template("sms.html", title = 'SMS')
	elif request.method == 'POST':
		#format date and time
		rdate = datetime.datetime.strptime(request.form['rdate'], "%m-%d-%Y")
		rtime = datetime.datetime.strptime(request.form['rtime'], "%H.%M")
		error_found = TvManager().post_sms(rdate.strftime("%Y-%m-%d"), \
			                             rtime.strftime("%H:%M:%S"), \
			                             request.form['rnumber'], \
			                             request.form['rname'], \
			                             request.form['snumber'], \
			                             request.form['sname'], \
			                             request.form['mbody'])
		return 'Not OK' if error_found else 'OK'

#@tv.route('/power/<string:power_data>', methods = ['GET'])
#def power(power_data):

@tv.route('/call/', methods = ['POST'])
def call_to_tv():
	"""Method POST will display Call on TV from form data"""
	#format date and time post_call(self, date='2014-02-12', time='22:20:33', rnumber='0674767730', rname='Romain', snumber='0617382221', sname='Lolo')
	date = datetime.datetime.strptime(request.form['date'], "%m-%d-%Y")
	time = datetime.datetime.strptime(request.form['time'], "%H.%M")
	error_found = TvManager().post_call(date.strftime("%Y-%m-%d"), \
			                            time.strftime("%H:%M:%S"), \
			                            request.form['rnumber'], \
			                            request.form['rname'], \
			                            request.form['snumber'], \
			                            request.form['sname'])
	return 'Not OK' if error_found else 'OK'

@tv.route('/power/', methods = ['GET', 'POST'])
def power():
    """Method GET will return the current power status of TV
    Method POST will activate or deactivate the TV"""
    resp_data = 'unknown'
    if request.method == 'GET':
        if TvManager().is_on():
            resp_data = 'on'
        else:
            resp_data = 'standby'
    elif request.method == 'POST':
        print(request.form)
        if TvManager().power(request.form['powerdata']):
            resp_data = request.form['powerdata']
    return jsonify(power = resp_data)

@tv.route('/channel/', methods = ['GET', 'POST'])
def channel():
    """Method POST will change TV channel"""
    TvManager().set_channel(request.form['channeldata'])
    return 'ok'

@tv.route('/key/<string:key_val>', methods = ['GET'])
def key(key_val):
    """Method GET will send remote key """
    TvManager().send_key(key_val)
    return jsonify(status = 'ok')