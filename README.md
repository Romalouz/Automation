Automation
==========

Raspberrypi based home automation using Python Flask, python-cec and eicsp 

Requirements:

Before you can run this web based application, you will need the following librairies:
  - libcec:       https://github.com/Pulse-Eight/libcec
  - python-cec:   https://github.com/trainman419/python-cec
  - onkyo-eiscp:  https://github.com/miracle2k/onkyo-eiscp‎
  - flask:        http://flask.pocoo.org/
  
I am running this application on Raspberry Pi with Raspian distribution.

Usage:

Install required librairies on your pi.

Configure IP of your Samsung B serie TV and your Onkyo receiver in file: media/config.py

Start the development server with following command: sudo ./run.py 

This will start the webserver that you can access with: http://your_pi_ip:3000
Note that no index page will be displayed !!

Following route are implemented:
  - /tv/sms   
    Display a form to send sms to tv
  - /tv/power/(on|standby)
    Send on or standby command to tv
  - /tv/get_power
    Display power status of tv

