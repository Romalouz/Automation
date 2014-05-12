#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: __init__.py
#   Author: Romain Gigault
#   Date: 21-Fev-2014
#   Info: Communicate with devices via HTTP GET / POST requests  
from flask import Flask, jsonify,render_template, url_for
from flask_bootstrap import Bootstrap

media = Flask(__name__)
Bootstrap(media)

# Configurations
media.config.from_object('media.config')

# Import a module / component using its blueprint handler variable
from media.receiver.controllers import receiver as receiver_module
from media.tv.controllers import tv as tv_module
from media.app.controllers import app as app_module
from media.pc.controllers import pc as pc_module

# Register blueprint(s)
media.register_blueprint(receiver_module)
media.register_blueprint(tv_module)
media.register_blueprint(app_module)
media.register_blueprint(pc_module)

#initiate CEC
#from media.cec import CecSingleton
@media.route('/api/', methods = ['GET'])
def this_func():
    """This is a function. It does nothing."""
    return jsonify({ 'result': '' })

@media.route('/api/help/', methods = ['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in media.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = media.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)
