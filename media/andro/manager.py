#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: androCommunication.py
#   Package: andro
#   Author: Romain Gigault 
from media import media
from urllib import urlopen

class AndroManager(object):
    """Allows to send message and notification using AutoRemote application on android device"""
    def __init__(self):
        self.message_base_url = "https://autoremotejoaomgcd.appspot.com/sendmessage?key="+media.config.get("AUTOREMOTE_KEY")
        self.notification_base_url = "https://autoremotejoaomgcd.appspot.com/sendnotification?key="+media.config.get("AUTOREMOTE_KEY")
        
    def send_message(self, message, target="", sender="", password="", ttl="", collapseKey=""):
        """Send a message to Android Device"""
        full_url = self.message_base_url + "&message=" + media.config.get("AUTOREMOTE_MESSAGE_FILTER") + " " + message
        if target != "":
            full_url += "&target=" + target
        if sender != "":
            full_url += "&sender=" + sender
        if password != "":
            full_url += "&password=" + password
        if ttl != "":
            full_url += "&ttl=" + ttl
        if collapseKey != "":
            full_url += "&collapseKey=" + collapseKey
        try:
            urlopen(full_url)
        except:
            raise "ARGGGGGGGGHHHHHHHHHHH"

    def send_notification(self, title="",text="",id="",led_color="",led_on="",led_off=""):
        """Send a notification to Android Device"""
        #TODO parser to clear spaces !
        full_url = self.notification_base_url
        if title != "":
            full_url += "&title=" + title
        if text != "":
            full_url += "&text=" + text
        if id != "":
            full_url += "&id=" + id
        if led_color != "":
            full_url += "&led=" + led_color
        if led_on != "":
            full_url += "&ledon=" + led_on
        if led_off != "":
            full_url += "&ledoff=" + led_off
        try:
            urlopen(full_url)
        except:
            raise "ARGGGGGGGGHHHHHHHHHHH2"
     