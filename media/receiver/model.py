#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: model.py
#   Author: Romain Gigault
#   Date: 15-Jan-2014
#   Info: Interface for Onkyo Receiver
import eiscp

class ReceiverModel(eiscp.eISCP):
	"""Create a ReceiverModel object for remote control."""

	def __init__(self,host):
		"""Create ReceiverModel object with host IP provided """
		super(ReceiverModel, self).__init__(host=host)
		self.power_status = 'unknown'
		#TODO add test that receiver exists in network

	@classmethod
	def fromsearch(cls):
		"""Look for all eiscp devices on network.
		Look for TX-NR509 device and affect to receiver attribute """
		# super(Txnr509, cls).__init__(cls, host='none')
		receivers = cls.discover()
		try:
			for receiver in receivers:
				if receiver.info['model_name'] == 'TX-NR509':
					cls.host = receiver.host
					cls.port = receiver.port
					cls.info = receiver.info
					cls.power_status = 'unknown'
					break
			# If receiver is none, raise exception
			if cls.host == 'none' or \
			   cls.port == 'none':
				raise ReceiverError("Device not found on network, aborting", "__init__")

		except ReceiverError, e:
			print(e)

	def __exit__(self):
		"""Disconnect from device when exiting"""
		self.disconnect()

	def set_message(self, timeout=0.1):
		self.message = self.get(timeout=timeout)

	def assert_status(self, result, command, status):
		if result[0] == command and result[1] == status:
			self.set_message()
		else:
			raise ReceiverError('Device was not set {stat} via {cmd}' \
				   .format(stat=status,cmd=command), 'assert_status') 
		
	def get_message(self):
		print(self.message)

	def power(self, pwr):
		"""Used to set device on or off"""
		self.power_status = pwr
		if pwr == 'on':
			result = self.command('system-power on')
			self.assert_status(result, 'system-power', 'on')
		elif pwr == 'off' or pwr == 'standby':
			result = self.command('system-power standby')
			self.assert_status(result, 'system-power', 'standby')
		else:
			raise ReceiverError("Value {val} is not a valid power argument".format(val=pwr), 'power')

	def set_volume(self, value=30):
		"""Set device volume to value """
		try:
			assert(15<value<75)
		except AssertionError:
			raise ReceiverError("Value {val} is not in volume range".format(val=value), 'set_volume')
		except:
			raise ReceiverError("Unexpected error !", 'set_volume')
		result = self.command('volume {}'.format(str(value)))
		if result[0][1] == 'volume' and '0x'+ result[1].lower() == hex(value).lower() :
			self.set_message()
		else:
			raise ReceiverError('Device volume was not set to {val}' \
				   .format(val=value), 'set_volume') 

	def power_ps3(self, power=''):
		""" Start or stop PS3 based on power (pwron or pwroff) """
		if power == 'pwron' or power == 'pwroff':
			self.command('dvd-player={}'.format(power))
			self.set_message(5)
		else:
			raise ReceiverError("Value '{pwr}' is not a valid command".format(pwr=power), 'power_ps3')

	def set_fm(self, frequency='10230'):
		""" Set input on FM and send the FM frequency"""
		error_message = "Value '{freq}' is not ".format(freq=frequency)
		if(len(frequency) != 5):
			raise ReceiverError(error_message + "a valid FM frequency", 'set_fm')
		#Check that frequency is a valid integer and is in FM range 
		try:
			freq = int(frequency)
			assert(8750<=freq<=10800)
		except AssertionError:
			raise ReceiverError(error_message + "in the FM range", 'set_fm')
		except ValueError:
			raise ReceiverError(error_message + "an integer", 'set_fm')
		except:
			raise ReceiverError("Unexpected error !", 'set_fm')
		#switch input to tuner FM
		result = self.command('input-selector fm')
		self.assert_status(result, 'input-selector', 'fm')
		#Send command for FM frequency
		result = self.raw('TUN' + frequency)
		if result == 'TUN' + frequency:
			self.set_message()
		else:
			raise ReceiverError('FM frequency was not set to {val}' \
				   .format(val=frequency), 'set_fm') 




class ReceiverError(Exception):
	"""ReceiverError is raised when an error occurs while controlling Onkyo device"""
	def __init__(self, message, method=''):
		"""Constructor of Exception:
		message: message to display
		method: method where exception is raised"""
		self.message = message
		self.method = method
	def __str__(self):
		"""Display exception"""
		if self.method != '':
			return "Method {method} raised: {message}" \
				   .format(method=self.method, message=self.message)
		else:
			return "{message}".format(message=self.message)