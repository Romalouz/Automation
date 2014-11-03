#!  /usr/bin/env python
from flup.server.fcgi import WSGIServer
from media import media
from media.arduino.model import ArduinoThread
from time import sleep

if __name__ == '__main__':
    #Start Arduino thread before starting webserver
    arduino_thread = ArduinoThread(iface_address = media.config.get("AD_PORT_VAL"), timer =  media.config.get("DETECTION_TIME"))
    sleep(1)
    if arduino_thread.isAlive():
        print('Thread is running')
    WSGIServer(media).run()
    #Kill thread
    arduino_thread.stop()
    sleep(1)
    if(not arduino_thread.isAlive()):
        print "Exiting web server and Arduino thread"