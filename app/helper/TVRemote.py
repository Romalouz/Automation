#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: samsungremote.py
#   Author: Romain Gigault
#   Date: 07-Fev-2014
#   Info: To send remote control commands to the Samsung B series tv over LAN
 
import socket
import time
import unicodedata

class BSeriesSender(object): #implements KeyCodeSender {
	"""Create a BSeriesSender object for remote control of TV."""
	def __init__(self, host, port=2345):
		"""Provide TV ip to create remote object """
		self.host = host
		self.port = port
		self.set_command_list()

	def __exit__(self):
		"""Reset host and port number"""
		self.host = 0
		self.port = 0

	def send_key(self, key):
		"""Send a key to TV"""
		# Assert that code exists
		if(key in self.commands):
			try:
				# Open Socket
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect((self.host, self.port))
				command = str(self.commands[key]) + '\n'
				sock.send(command)
				sock.close()
			except socket.error, e:
				raise TVError(e[1], 'send_key')
			finally:
				sock.close()
				sock = None
		else:
			raise TVError('Key received is note a valid code', 'send_key')

	def set_channel(self, channel_value):
		"""Send a channel value command"""
		error_message = "Value '{chan}' is not ".format(chan=channel_value)
		# Make sure channel_value is an int before getting the number of keys to send
		try:
			int(channel_value)
			assert(0<=channel_value<=999)
		except AssertionError:
			raise TVError(error_message + "in the channel range", 'set_channel')
		except ValueError:
			raise TVError(error_message + "an integer", 'set_channel')
		except:
			raise TVError("Unexpected error !", 'set_fm')
		for char in str(channel_value).zfill(3):
			self.send_key('BTN_' + char)
			time.sleep(0.1)
	
	def post_sms(self, date='2014-02-12', time='22:20:33', rnumber='0674767730', rname='Romain', snumber='0617382221', sname='Lolo', message='Bonjour !'):
		"""This routine is used to send a message of type SMS to the TV"""
		xmldata1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + \
		"<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">" + \
		"<s:Body>" + \
		"<u:AddMessage xmlns:u=\"urn:samsung.com:service:MessageBoxService:1\">" + \
		"<MessageType>text/xml</MessageType>" + \
		"<MessageID>can be anything</MessageID>" + \
		"<Message>" + \
		"&lt;Category&gt;SMS&lt;/Category&gt;" + \
		"&lt;DisplayType&gt;Maximum&lt;/DisplayType&gt;" + \
		"&lt;ReceiveTime&gt;" + \
		"&lt;Date&gt;"
		xmldata2 = "&lt;/Date&gt;" + \
		"&lt;Time&gt;"
		xmldata3 = "&lt;/Time&gt;" + \
		"&lt;/ReceiveTime&gt;" + \
		"&lt;Receiver&gt;" + \
		"&lt;Number&gt;"
		xmldata4 = "&lt;/Number&gt;" + \
		"&lt;Name&gt;"
		xmldata5 = "&lt;/Name&gt;" + \
		"&lt;/Receiver&gt;" + \
		"&lt;Sender&gt;" + \
		"&lt;Number&gt;"
		xmldata6 = "&lt;/Number&gt;" + \
		"&lt;Name&gt;"
		xmldata7 = "&lt;/Name&gt;" + \
		"&lt;/Sender&gt;" + \
		"&lt;Body&gt;"
		xmldata8 = "&lt;/Body&gt;" + \
		"</Message>" + \
		"</u:AddMessage>" + \
		"</s:Body>" + \
		"</s:Envelope>"

		#Remove accentuation of message
		message = unicodedata.normalize('NFKD', message).encode('ASCII', 'ignore')
		#Bool to check error
		error_found = False
		#Create Header for Message
		header = "POST /PMR/control/MessageBoxService HTTP/1.0\r\n" + \
		"Content-Type: text/xml; charset=\"utf-8\"\r\n" + \
		"Host: " + self.host + "\r\n" + \
		"Content-Length: " + str(len(xmldata1) + len(date) + \
								len(xmldata2) + len(time) + \
								len(xmldata3) + len(rnumber) + \
								len(xmldata4) + len(rname) + \
								len(xmldata5) + len(snumber) + \
								len(xmldata6) + len(sname) + \
								len(xmldata7) + len(message) + \
								len(xmldata8)) + "\r\n"  + \
		"SOAPACTION: urn:samsung.com:service:MessageBoxService:1#AddMessage\r\n" + \
		"Connection: close\r\n\r\n"
		#Create socket
		full_soap_request = header + \
			xmldata1 + date + \
			xmldata2 + time + \
			xmldata3 + rnumber + \
			xmldata4 + rname + \
			xmldata5 + snumber +\
			xmldata6 + sname +\
			xmldata7 + message + xmldata8
		msg_port = 52235;
		
		try:
			# Open Socket
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.host, msg_port))
			sock.send(full_soap_request.encode('utf-8'))
			read = sock.recv(1024)
		#	print("\n\n Reader \n\n" + read)
 			sock.close()
		except socket.error, e:
			error_found = True
			raise TVError(e[1], 'post_sms')
		finally:
			sock.close()
			sock = None
		return error_found

	def post_call(self, date='2014-02-12', time='22:20:33', rnumber='0674767730', rname='Romain', snumber='0617382221', sname='Lolo'):
		"""This routine is used to send a message of type call to the TV"""
		xmldata1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + \
		"<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">" + \
		"<s:Body>" + \
		"<u:AddMessage xmlns:u=\"urn:samsung.com:service:MessageBoxService:1\">" + \
		"<MessageType>text/xml</MessageType>" + \
		"<MessageID>call</MessageID>" + \
		"<Message>" + \
		"&lt;Category&gt;Incoming Call&lt;/Category&gt;" + \
		"&lt;DisplayType&gt;Maximum&lt;/DisplayType&gt;" + \
		"&lt;CallTime&gt;" + \
		"&lt;Date&gt;"
		xmldata2 = "&lt;/Date&gt;" + \
		"&lt;Time&gt;"
		xmldata3 = "&lt;/Time&gt;" + \
		"&lt;/CallTime&gt;" + \
		"&lt;Callee&gt;" + \
		"&lt;Number&gt;"
		xmldata4 = "&lt;/Number&gt;" + \
		"&lt;Name&gt;"
		xmldata5 = "&lt;/Name&gt;" + \
		"&lt;/Callee&gt;" + \
		"&lt;Caller&gt;" + \
		"&lt;Number&gt;"
		xmldata6 = "&lt;/Number&gt;" + \
		"&lt;Name&gt;"
		xmldata7 = "&lt;/Name&gt;" + \
		"&lt;/Caller&gt;" + \
		"</Message>" + \
		"</u:AddMessage>" + \
		"</s:Body>" + \
		"</s:Envelope>"

		#Remove accentuation of message
		message = unicodedata.normalize('NFKD', message).encode('ASCII', 'ignore')

		#Create Header for Message
		header = "POST /PMR/control/MessageBoxService HTTP/1.0\r\n" + \
		"Content-Type: text/xml; charset=\"utf-8\"\r\n" + \
		"Host: " + self.host + "\r\n" + \
		"Content-Length: " + str(len(xmldata1) + len(date) + \
								len(xmldata2) + len(time) + \
								len(xmldata3) + len(rnumber) + \
								len(xmldata4) + len(rname) + \
								len(xmldata5) + len(snumber) + \
								len(xmldata6) + len(sname) + \
								len(xmldata7)) + "\r\n"  + \
		"SOAPACTION: urn:samsung.com:service:MessageBoxService:1#AddMessage\r\n" + \
		"Connection: close\r\n\r\n"
		#Create socket
		full_soap_request = header + \
			xmldata1 + date + \
			xmldata2 + time + \
			xmldata3 + rnumber + \
			xmldata4 + rname + \
			xmldata5 + snumber +\
			xmldata6 + sname +\
			xmldata7
		msg_port = 52235;

		try:
			# Open Socket
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.host, msg_port))
			sock.send(full_soap_request.encode('utf-8'))
			read = sock.recv(1024)
			print("\n\n Reader \n\n" + read)
 			sock.close()
		except socket.error, e:
			raise TVError(e[1], 'post_call')
		finally:
			sock.close()
			sock = None

	def post_reminder(self, date1='2014-02-12', time1='22:20:33', rnumber='0674767730', rname='Romain', subject='Subject', date2='2014-03-12', time2='23:20:33', location='Paris', body='Description'):
		"""This routine is used to send a message of type reminder to the TV"""
		xmldata1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + \
		"<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">" + \
		"<s:Body>" + \
		"<u:AddMessage xmlns:u=\"urn:samsung.com:service:MessageBoxService:1\">" + \
		"<MessageType>text/xml</MessageType>" + \
		"<MessageID>can be anything</MessageID>" + \
		"<Message>" + \
		"&lt;Category&gt;Schedule Reminder&lt;/Category&gt;" + \
		"&lt;DisplayType&gt;Maximum&lt;/DisplayType&gt;" + \
		"&lt;StartTime&gt;" + \
		"&lt;Date&gt;"
		xmldata2 = "&lt;/Date&gt;" + \
		"&lt;Time&gt;"
		xmldata3 = "&lt;/Time&gt;" + \
		"&lt;/StartTime&gt;" + \
		"&lt;Owner&gt;" + \
		"&lt;Number&gt;"
		xmldata4 = "&lt;/Number&gt;" + \
		"&lt;Name&gt;"
		xmldata5 = "&lt;/Name&gt;" + \
		"&lt;/Owner&gt;" + \
		"&lt;Subject&gt;"
		xmldata6 = "&lt;/Subject&gt;" + \
		"&lt;EndTime&gt;" + \
		"&lt;Date&gt;"
		xmldata7 = "&lt;/Date&gt;" + \
		"&lt;/Time&gt;"
		xmldata8 = "&lt;/Time&gt;" + \
		"&lt;/EndTime&gt;" + \
		"&lt;Location&gt;"
		xmldata9= "&lt;/Location&gt;" + \
		"&lt;Body&gt;"
		xmldata10 = "&lt;/Body&gt;" + \
		"</Message>" + \
		"</u:AddMessage>" + \
		"</s:Body>" + \
		"</s:Envelope>"

		#Create Header for Message
		header = "POST /PMR/control/MessageBoxService HTTP/1.0\r\n" + \
		"Content-Type: text/xml; charset=\"utf-8\"\r\n" + \
		"Host: " + self.host + "\r\n" + \
		"Content-Length: " + str(len(xmldata1) + len(date1) + \
								len(xmldata2) + len(time1) + \
								len(xmldata3) + len(rnumber) + \
								len(xmldata4) + len(rname) + \
								len(xmldata5) + len(subject) + \
								len(xmldata6) + len(date2) + \
								len(xmldata7) + len(time2) + \
								len(xmldata8) + len(location) + \
								len(xmldata9) + len(body) + \
								len(xmldata10)) + "\r\n"  + \
		"SOAPACTION: urn:samsung.com:service:MessageBoxService:1#AddMessage\r\n" + \
		"Connection: close\r\n\r\n"
		#Create socket
		full_soap_request = header + \
			xmldata1 + date1 + \
			xmldata2 + time1 + \
			xmldata3 + rnumber + \
			xmldata4 + rname + \
			xmldata5 + subject +\
			xmldata6 + date2 +\
			xmldata7 + time2 +\
			xmldata8 + location +\
			xmldata9 + body +\
			xmldata10
		msg_port = 52235;

		try:
			# Open Socket
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.host, msg_port))
			sock.send(full_soap_request.encode('utf-8'))
			read = sock.recv(1024)
			print("\n\n Reader \n\n" + read)
 			sock.close()
		except socket.error, e:
			raise TVError(e[1], 'post_reminder')
		finally:
			sock.close()
			sock = None


	def set_command_list(self):
		"""List of available commands for Samsung B series TV"""
		self.commands = dict( \
			BTN_POWER_OFF = 2, \
			BTN_TV = 27, \
			BTN_1 = 4, \
			BTN_2 = 5, \
			BTN_3 = 6, \
			BTN_4 = 8, \
			BTN_5 = 9, \
			BTN_6 = 10, \
			BTN_7 = 12, \
			BTN_8 = 13, \
			BTN_9 = 14, \
			BTN_0 = 17, \
			BTN_FAVOURITE_CHANNEL = 68, \
			BTN_PREVIOUS_CHANNEL = 19, \
			BTN_VOLUME_UP = 7, \
			BTN_VOLUME_DOWN = 11, \
			BTN_CHANNEL_UP = 18, \
			BTN_CHANNEL_DOWN = 16, \
			BTN_MUTE = 15, \
			BTN_SOURCE = 1, \
			BTN_INFO = 31, \
			BTN_TOOLS = 75, \
			BTN_GUIDE = 79, \
			BTN_RETURN = 88, \
			BTN_MENU = 26, \
			BTN_ENTER = 104, \
			BTN_UP = 96, \
			BTN_DOWN = 97, \
			BTN_LEFT = 101, \
			BTN_RIGHT = 98, \
			BTN_INTERNET = 147, \
			BTN_EXIT = 45, \
			BTN_RED = 108, \
			BTN_GREEN = 20, \
			BTN_YELLOW = 21, \
			BTN_BLUE = 22, \
			BTN_TELETEXT = 44, \
			BTN_MEDIA = 140, \
			BTN_CONTENT = 121, \
			BTN_CHANNEL_LIST = 107, \
			BTN_AD = 0, \
			BTN_SUBTITLE = 37, \
			BTN_FORWARD = 69, \
			BTN_PAUSE = 74, \
			BTN_BACKWARD = 72, \
			BTN_RECORD = 73, \
			BTN_PLAY = 71, \
			BTN_STOP = 70, \
			BTN_SLEEP = 3, \
			BTN_PICTURE_IN_PICTURE = 32, \
			BTN_PSIZE = 62, \
			BTN_ENERGY = 119, \
			BTN_SRS = 110, \
			BTN_PMODE = 40, \
			BTN_P_DYNAMIC = 189, \
			BTN_P_STANDARD = 223, \
			BTN_P_MOVIE1 = 222, \
			BTN_P_MOVIE2 = 221, \
			BTN_P_USER1 = 220, \
			BTN_P_USER2 = 219, \
			BTN_P_USER3 = 218, \
			BTN_ASPECT_43 = 227, \
			BTN_ASPECT_169 = 228, \
			BTN_S_SCART1 = 132, \
			BTN_S_SCART2 = 235, \
			BTN_S_MODULE = 134, \
			BTN_S_AV = 236, \
			BTN_S_VGA = 105, \
			BTN_S_HDMI1 = 233, \
			BTN_S_HDMI2 = 190, \
			BTN_S_HDMI3_DVI = 194, \
			BTN_S_HDMI4 = 197)

class TVError(Exception):
	"""TVError is raised when an error occurs while controlling Samsung B serie TV"""
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