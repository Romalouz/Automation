#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: manager.py
#   Package: Tv
#   Author: Romain Gigault
import time
from media import media
from media.tv.model import TvModel
from media.cec import CecSingleton

class TvManager(TvModel):
    """Called every time we need to access Tv Device"""

    def __init__(self):
        self.power_status = 'unknown'
        super(TvManager, self).__init__(host=media.config.get("TV_IP"))

    # Device control method
    def power(self, power):
        """Use to power on or standby tv and receiver at once
        Requires power = on or power = standby"""
        command_success = False
        tv = CecSingleton.CecSingleton().get_device(media.config.get("CEC_TV_OSD"))
        if power == "on":
            tv.power_on()
            if tv.is_on():
                command_success = True
        elif power == "standby":
            tv.standby()
            if not(tv.is_on()):
                command_success = True
        else:
            command_success = False
        if command_success: return power

    def get_power_status(self):
        """Return TV power status True -> on and False -> Standby """
        if CecSingleton.CecSingleton().get_device(media.config.get("CEC_TV_OSD")).is_on():
            power = 'on'
        else:
            power = 'standby'
        return power


    def current_power_status(self):
        """Return power status of TV """
        #super(TvManager, self).__init__(host=media.config.get("TV_IP"))
        return self.get_power_status()

    def read_status(self):
        """Return current status of TV"""
        self.power_status = self.current_power_status()