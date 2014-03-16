#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: manager.py
#   Package: Tv
#   Author: Romain Gigault
import time
from media import media
from media.tv.model import TvModel

class TvManager(TvModel):
    """Called every time we need to access Tv Device"""

    def __init__(self):
        self.power_status = 'unknown'
        #super(TvManager, self).__init__(host=media.config.get("TV_IP"))

    def current_power_status(self):
        """Return power status of TV """
        super(TvManager, self).__init__(host=media.config.get("TV_IP"))
        return self.get_power_status()

    def read_status(self):
        """Return current status of TV"""
        self.power_status = self.current_power_status()