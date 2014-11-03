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

class ArduinoThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""
    def __init__(self, iface_address, timer):
        super(ArduinoThread, self).__init__()
        self._stop = threading.Event()
        self.setDaemon = True
        self.anybody_home = False
        self.iface_address = iface_address
        self.timer = timer
        self.last_detected = 0 #Initialize last_detected
        self.last_message_sent = 0 
        day_str = time.strftime("%d-%b-%Y",time.localtime())
        self.sunrise = time.strptime(day_str + " 08:00", "%d-%b-%Y %H:%M")
        self.sunset = time.strptime(day_str + " 20:00", "%d-%b-%Y %H:%M")
        self.start()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        arduino_serial = serial.Serial(self.iface_address, 9600, timeout=0.1)
        time.sleep(1)
        as_read,_,_ = select.select([arduino_serial],[],[],7)
        light_triggered = False
        while 1:
            try:
                data = as_read[0].readline()
            except:
                #if programs falls here, it means that did not return the serial link, try to bound it again
                data = ''
                as_read,_,_ = select.select([arduino_serial],[],[],7)
                #print("Trying to bound again with Serial")
                pass
            if data != '':
                self.anybody_home = True
                self.last_detected = time.time()
                #print("Someone detected at " + time.strftime("%d-%b-%Y %H:%M",time.localtime(self.last_detected)))
            if self.anybody_home:
                if (time.time() - self.last_message_sent > self.timer*60):#TODO correct this, it should send a signal when someone is detected and not wait the timer
                    #print("Sending message to Andro...")
                    AndroManager().send_notification(title='Someone%20at%20home', text = "Detected%20at%20" + time.strftime("%d-%b-%Y---%H:%M",time.localtime(self.last_detected)),id="sbdy_detected",led_color="red",led_on="5000",led_off="2000")
                    self.anybody_home = False
                    self.last_message_sent = time.time()
                    self.last_detected = 0
                #if self.check_sunrise_sunset():
                #    if not light_triggered:
                #        #Trigger light and remember command
                #        print ("Triggering light...")
                #        ArduinoModel(self.iface_address).switch_status("livingRoom","on")
                #        light_triggered = True
                #if light_triggered and (time.time() - self.last_detected > 1*60):
                #    print ("Killing light...")
                #    ArduinoModel(self.iface_address).switch_status("livingRoom","off")
                #    light_triggered = False
                #    self.anybody_home = False
                #TODO create a switch to avoid lightening up if it is not required

            #Exit the loop if thread was asked to stop
            if(self.stopped()):
                del(arduino_serial)
                return

    def update_timer(self):
        self.timer = time.time() #Get actual time

    def check_sunrise_sunset(self):
        now = time.localtime()
        #print("Sunrise : " + time.strftime("%d-%b-%Y %H:%M", self.sunrise))
        #print("Now : " + time.strftime("%d-%b-%Y %H:%M", now))
        #print("Sunset : " + time.strftime("%d-%b-%Y %H:%M", self.sunset))
        if(self.sunrise < now and now < self.sunset):
            return False
        else:
            return True

    def update_sun_times(self):
        #TODO write a parser to get sun time via a webservic
        return False