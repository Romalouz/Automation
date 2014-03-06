#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: manager.py
#   Package: Tv
#   Author: Romain Gigault
import cec
import time
from media import media
from media.tv.model import TvModel

class TvManager(TvModel):
    """Called every time we need to access Tv Device"""

    def __init__(self):
        super(TvManager, self).__init__(host=media.config.get("TV_IP"))

    def init_cec(self):
        """Used before each call to cec librairy"""
        cec_initiated = False
        adapter = cec.list_adapters()
        if adapter.count(media.config.get("CEC_ADAPTER")) >= 1:
            cec.init()
            cec_initiated = True
        return cec_initiated

    def power(self, power):
        """Use to power on or standby tv and receiver at once
        Requires power = on or power = standby | off"""
        command_success = False
        if self.init_cec():
            tv = cec.Device(media.config.get("CEC_TV_ADDRESS"))
            receiver = cec.Device(media.config.get("CEC_RECEIVER_ADDRESS"))
            if power == "on":
                tv.power_on()
                receiver.power_on()
                if tv.is_on() and receiver.is_on():
                   command_success = True
            elif power == "off" or power == "standby":
                tv.standby()
                receiver.standby()
                command_success = True
            else:
                 "not good" 
        return command_success

    def get_power_status(self):
        """Return TV power status True -> on and False -> Standby """
        if self.init_cec():
            return cec.Device(media.config.get("CEC_TV_ADDRESS")).is_on()