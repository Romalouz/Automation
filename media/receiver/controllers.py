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
from media.receiver.manager import ReceiverManager

# Define the blueprint: 'receiver', set its url prefix: app.url/receiver
receiver = Blueprint('receiver', __name__, url_prefix='/receiver')

@receiver.route('/radio/<string:freq>', methods = ['GET'])
def power_radio(freq):
    ReceiverManager().set_fm(freq)
    return 'Ok'

@receiver.route('/set_input/<string:input_data>', methods = ['GET'])
def set_onkyo_input(input_data):
    ReceiverManager().command('input-selector {inp}'.format(inp=input_data))
    return 'Ok'

@receiver.route('/power/<string:power_data>', methods = ['GET'])
def power(power_data):
    data = ReceiverManager().power(power_data)
    if data == power_data:
        return data
    else:
        return "Not Ok"

@receiver.route('/power/', methods = ['GET'])
def get_power():
    receiver = ReceiverManager()
    receiver.read_status()
    return receiver.power_status

@receiver.route('/volume/<int:vol>', methods = ['GET'])
def volume(vol):
    ReceiverManager().set_volume(vol)
    return 'Ok'

@receiver.route('/ps3/<string:pow>', methods = ['GET'])
def set_onkyo_ps3(pow):
    ReceiverManager().power_ps3(pow)
    return 'PS3 Ok'