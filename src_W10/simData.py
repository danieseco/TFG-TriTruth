import paho.mqtt.client as mqtt
import socket
import sys
import time

def connMqtt():
    try:
        global client
        IP = socket.gethostbyname(socket.gethostname())
        client = mqtt.Client()
        client.connect(IP)
        client.loop_start()
    except:
    	raise Exception('mqtt error')
		
client = None
try:
	connMqtt()
except Exception as e:
	print("Error", e)
places = []
with open('simData.log','r') as info:
	lectura = info.read()
	'''lect = lectura.split(' ')
	for place in lect:
		three = place.split('#')
		places.append([three[1],three[2]])'''

if int(sys.argv[1]) == 1:
	client.publish('state', sys.argv[2] + " SI")
	client.publish('places', sys.argv[2] + lectura)
	time.sleep(1)

client.disconnect()
