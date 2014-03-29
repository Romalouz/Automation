#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: CecSingleton.py
#   Package: Tv
#   Author: Romain Gigault
import cec

class CecSingleton(object):
    class __CecSingleton:
        def __init__(self):
            """Create CEC singleton if it does not exist"""
            self.initiated = False
            self.devices = None
        
        def __str__(self):
            """Print CEC Singleton data"""
            return `self` + self.val
        
        def init_cec(self):
            """Method to init cec adapter. Return True if cec initiated successfully"""
            if (self.initiated): return
            adapter = cec.list_adapters()
            if len(adapter) >= 1:
                try:
                    cec.init()
                    self.adapter = adapter.pop()
                    self.devices = cec.list_devices()
                    self.initiated = True
                except:
                    self.initiated = False

        def get_device(self, osd_string):
            """Return CeC device that matches osd_string"""
            if not(self.initiated): self.init_cec()
            for key, device in self.devices.iteritems():
                if device.osd_string == osd_string:
                     return device
            #if we are here, no device were found
            return None


    instance = None
    def __new__(cls):
        """ Create Singleton if does not exist or call current instance """
        if not CecSingleton.instance:
            CecSingleton.instance = CecSingleton.__CecSingleton()
        return CecSingleton.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
