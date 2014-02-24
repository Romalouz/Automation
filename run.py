#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: __init__.py
#   Author: Romain Gigault
#   Date: 21-Fev-2014
#   Info: Communicate with devices via HTTP GET / POST requests 
from app import app

app.run(host='0.0.0.0', port=80, debug=True)