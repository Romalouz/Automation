#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: WebIO.py
#   Author: Romain Gigault
#   Date: 21-Fev-2014
#   Info: Communicate with devices via HTTP GET / POST requests 
import TXNR509
import TVRemote

from flask import Flask, jsonify

app = Flask(__name__)
# myonkyo = TXNR509.Txnr509()
mysamsung = TVRemote.BSeriesSender(host="192.168.1.12")

@app.route("/")
def index():
    return "Hello Max!"

@app.route('/SMS/<string:date>/<string:time>/<string:rnumber>/<string:rname>/<string:snumber>/<string:sname>/<string:message>', methods = ['GET'])
def sms_to_tv(date, time, rnumber, rname, snumber, sname, message):
	test = mysamsung.post_sms(date, time, rnumber, rname, snumber, sname, message)
	return test


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
