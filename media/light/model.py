#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: model.py
#   Author: Romain Gigault
#   Date: 17-Sept-2014
#   Info: Interface for light
import serial, time

class LightModel():
    """Create a light object for remote control."""

    def __init__(self,port):
        self.port = port
        self.iface = serial.Serial(port, 9600, timeout=0.1)
        time.sleep(1)

    def __exit__(self):
        self.iface.close()

    def switch_status(self,device, on_off):
        error = False
        print device
        print on_off
        if device != 'bedRoom' and device != 'livingRoom':
            return 'bad device'
        if on_off == 'on':
            if device == 'bedRoom':
                self.iface.write('1')
            elif device == 'livingRoom':
                self.iface.write('3')
        elif on_off == 'off':
            if device == 'bedRoom':
                self.iface.write('0')
            elif device == 'livingRoom':
                self.iface.write('2')
        else:
            error = True
        if error:
            return "NOK"
        else:
            return "OK"

        

