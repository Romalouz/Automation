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
            if tv.power_on():
                command_success = True
        elif power == "standby":
            if tv.standby():
                command_success = True
        else:
            command_success = False
        return command_success

    def get_power_status(self):
        """Return TV power status True -> on and False -> Standby """
        return CecSingleton.CecSingleton().get_device(media.config.get("CEC_TV_OSD")).is_on()

    def is_on(self):
        """Return power status of TV """
        #super(TvManager, self).__init__(host=media.config.get("TV_IP"))
        return self.get_power_status()

    def read_status(self):
        """Return current status of TV"""
        if self.is_on():
            self.power_status = 'on'
        else:
            self.power_status = 'standby'