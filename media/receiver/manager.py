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
        super(ReceiverManager, self).__init__(host=media.config.get("RECEIVER_IP"))