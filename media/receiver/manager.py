#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: manager.py
#   Package: Receiver
#   Author: Romain Gigault 
from media import media
from media.receiver.model import ReceiverModel

class ReceiverManager(ReceiverModel):
    """Called every time we need to access Receiver Device"""

    def __init__(self):
        self.power_status = 'unknown'
        self.name = 'Onkyo TX-NR509'#self.receiver.info

    def current_power_status(self):
        """Return power status of receiver """
        super(ReceiverManager, self).__init__(host=media.config.get("RECEIVER_IP"))
        return self.get_power_status()

    def read_status(self):
        """Return current status of Receiver"""
        self.power_status = self.current_power_status()