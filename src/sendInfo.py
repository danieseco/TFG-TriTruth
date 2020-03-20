import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
client_id = ubinascii.hexlify(machine.unique_id())

#Previous global config load
with open('wireless.conf','r') as configFile:
	lineNumber=0			#As in python, line beginning with '#' is a comment very
	for line in configFile:	#important adding the symbol as first character and
		if line[0] != '#': 	#all comments at the top of file whithout empty lines
			if lineNumber==0:
				ssid = line
				lineNumber+=1
			elif lineNumber==1:
				password=line
				lineNumber+=1
			elif lineNumber ==2:
				mqtt_server=line
				
#Wireless connection
def connectWifi():
	global ssid, password
	wifi = network.WLAN(network.STA_IF)
	wifi.active(True)
	wifi.connect(ssid,password)
	waitTime=0
	while station.isconnected()==False and waitTime<5:
		machine.lightsleep(100)
		waitTime+=0.1
	if station.isconnected()==False:
		return 'Error'
	else:
		return wifi

#Callback for topic subscribing
def sub_cb(topic,msg):
	pass #callback on develop
		
#MQTT connection and topics subscribing
def connectMQTT():
	global client_id, mqtt_server, topics
	client = MQTTClient(client_id, mqtt_server)
	client.set_callback(sub_cb)
	try:
		client.connect()
	except MQTTException:
		return 'Error'
	for topic in topics:
		client.subscribe(topic)
	return client
	
topics = ['userAns']
wifi = connectWifi()
if wifi == 'Error':
	raise wifiError		
mqtt = connectMQTT()
if mqtt == 'Error':
	raise mqttError