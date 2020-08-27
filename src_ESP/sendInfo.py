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
topics = ['checked']

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

with open('user.conf','r') as idFile:
	id = idFile.read()

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
	if msg == id:
		#open('cheat.log','w').close()#Limpio el archivo
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

def publishContent(msgState, msgPlaces):
	mqtt.publish('state',msgState)
	time.sleep(0.5)
	if msgPlaces != '':
		mqtt.publish('places',msgPlaces)
	startTime = time.time()
	waitTime = 300 #5 minutos para esperar una respuesta de checked.
	while(waitTime > time.time()-startTime):
		mqtt.check_msg()
		
def run(cheatInfo):
	wifi = connectWifi()
	if wifi == 'Error':
		raise Exception('Wifi Error')
	mqtt = connectMQTT()
	if mqtt == 'Error':
		raise Exception('mqtt Error')
	
	if cheatInfo == '':
		msgState = '{} NO'.format(id)
		msgPlaces = ''
	else:
		msgState = '{} SI'.format(id)
		msgPlaces = '{} {}'.format(id, cheatInfo) 
			
	while wifi.isconnected():
		publishContent(msgState,msgPlaces)
	return('Unchecked')
