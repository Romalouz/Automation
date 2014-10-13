#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: model.py
#   Author: Romain Gigault
#   Date: 17-Sept-2014
#   Info: Interface for light
import serial, time, threading, select
from media.andro.manager import AndroManager

class ArduinoModel():
    """Create a Arduino object for remote control."""

    def __init__(self,port):
        self.port = port
        self.iface = serial.Serial(port, 9600, timeout=0.1)
        time.sleep(1)

    def __exit__(self):
        self.iface.close()

    def switch_status(self,device, on_off):
        error = False
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

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""
    def __init__(self, iface_address):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()
        self.setDaemon = True
        self.anybody_home = False
        self.iface_address = iface_address
        self.start()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        arduino_serial = serial.Serial(self.iface_address, 9600, timeout=0.1)
        as_read,_,_ = select.select([arduino_serial],[],[],7)
        while 1:
            try:
                data = as_read[0].readline()
            except:
                #if programs falls here, it means that did not return the serial link, try to bound it again
                data = ''
                as_read,_,_ = select.select([arduino_serial],[],[],7)
                print("Trying to bound again with Serial")
                pass
            if data != '':
                self.anybody_home = True
                print(data)
            if self.anybody_home:
                print("Sending message to Andro...")
                AndroManager().send_message('SomeoneHome')
                self.anybody_home = False
                
            #Exit the loop if thread was asked to stop
            if(self.stopped()):
                return