import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import time
import esp
esp.osdebug(None)
import gc
gc.collect()
client_id = ubinascii.hexlify(machine.unique_id())
topics = ['userAns']

#Previous global config load
with open('wireless.conf','r') as configFile:
	lineNumber=0			#As in python, line beginning with '#' is a comment very
	for line in configFile:	#important adding the symbol as first character and
		if line[0] != '#': 	#all comments at the top of file whithout empty lines
			if lineNumber==0:
				ssid = line.replace('\n','')
				lineNumber+=1
			elif lineNumber==1:
				password=line.replace('\n','')
				lineNumber+=1
			elif lineNumber ==2:
				mqtt_server=line.replace('\n','')
				
#Here user config should be loaded
dorsal=100
tramposo = 'NO'
#Wireless connection
def connectWifi():
	global ssid, password
	wifi = network.WLAN(network.STA_IF)
	wifi.active(True)
	wifi.connect(ssid,password)
	waitTime=30
	startTime = time.time()
	while wifi.isconnected()==False and waitTime > time.time()-startTime:
		pass
	if wifi.isconnected()==False:
		return 'Error'
	else:
		return wifi

#Callback for topic subscribing
def sub_cb(topic,msg):
	print('Received my topic, we go')
	machine.deepsleep()

#MQTT connection and topics subscribing
def connectMQTT():
	global client_id, mqtt_server, topics
	client = MQTTClient(client_id, mqtt_server)
	client.set_callback(sub_cb)
	try:
		client.connect()
	except:
		return 'Error'
	for topic in topics:
		client.subscribe(topic)
	return client

def run():
	wifi = connectWifi()
	if wifi == 'Error':
		raise Exception('Wifi Error')
	mqtt = connectMQTT()
	if mqtt == 'Error':
		raise Exception('mqtt Error')
	msg = b'Dorsal #{} Estado #{} tramposo'.format(dorsal, tramposo)
	mqtt.publish('userSays',msg)
	startTime = time.time()
	waitTime = 60
	while(waitTime > time.time()-startTime):
		mqtt.check_msg()

