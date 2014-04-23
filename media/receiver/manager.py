#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: manager.py
#   Package: Receiver
#   Author: Romain Gigault 
from media import media
from media.receiver.model import ReceiverModel
from media.cec import CecSingleton
from media.andro.manager import AndroManager


class ReceiverManager(ReceiverModel):
    """Called every time we need to access Receiver Device"""

    def __init__(self):
        super(ReceiverManager, self).__init__(host=media.config.get("RECEIVER_IP"))
        self.power_status = 'unknown'
        self.volume = '0'
        self.name = 'Onkyo TX-NR509'#self.receiver.info

    def is_on(self):
        """Return power status of receiver """
        #super(ReceiverManager, self).__init__(host=media.config.get("RECEIVER_IP"))
        return CecSingleton.CecSingleton().get_device(media.config.get("CEC_RECEIVER_OSD")).is_on()

    def read_status(self):
        """Return current status of Receiver"""
        self.power_status = self.get_power_status()
        self.volume = self.get_volume()

    # Device control method
    def set_audio(self, audio_input):
        """Use CecSingleton to set audio-input on Receiver.
        Check config for list of available audio input"""
        command_success = False
        receiver = CecSingleton.CecSingleton().get_device(media.config.get("CEC_RECEIVER_OSD"))
        command = dict(dvd = "CEC_RECEIVER_AI_DVD", \
                       vcr = "CEC_RECEIVER_AI_VCR", \
                       satellite = "CEC_RECEIVER_AI_SAT", \
                       game = "CEC_RECEIVER_AI_GAM", \
                       aux = "CEC_RECEIVER_AI_AUX", \
                       tuner = "CEC_RECEIVER_AI_TUN", \
                       tv = "CEC_RECEIVER_AI_TV" , \
                       port = "CEC_RECEIVER_AI_POR", \
                       net = "CEC_RECEIVER_AI_NET", \
                       usb = "CEC_RECEIVER_AI_USB")
        if command.has_key(audio_input):
            command_success  = receiver.set_audio_input(media.config.get(command[audio_input]))
        return command_success


