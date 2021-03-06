DEBUG = True
DEBUG_SECRET = 'romalouz'
DEBUG_PORT = '41220'
#Receiver related configuration
RECEIVER_IP = "TX-NR509.home"
#TV related configuration
TV_IP = "tvsalon.home"
#CEC related configuration
CEC_ADAPTER = "RPI"
CEC_TV_ADDRESS = 0
CEC_RECEIVER_ADDRESS = 5
CEC_PS3_ADDRESS = 4
CEC_TV_OSD = "TV"
CEC_RECEIVER_OSD = "TX-NR509"
CEC_PS3_OSD = "PlayStation 3"
CEC_ADAPTER_OSD = "python-cec"
CEC_RECEIVER_AI_DVD = 1
CEC_RECEIVER_AI_VCR = 2
CEC_RECEIVER_AI_SAT = 3
CEC_RECEIVER_AI_GAM = 4
CEC_RECEIVER_AI_AUX = 5
CEC_RECEIVER_AI_TUN = 6
CEC_RECEIVER_AI_TV = 7
CEC_RECEIVER_AI_POR = 8
CEC_RECEIVER_AI_NET = 9
CEC_RECEIVER_AI_USB = 10
AUTOREMOTE_TV_POWER = "TvPower =:= "
AUTOREMOTE_KEY = ""
AUTOREMOTE_MESSAGE_FILTER = ""
PC_MAC_ADDRESS = ""
AD_PORT_VAL = "/dev/ttyACM0"
DETECTION_TIME = 2 #Time in minutes before we consider that detected person has left
try:
   from secret_settings import *
except ImportError:
   pass