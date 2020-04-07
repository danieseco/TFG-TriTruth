import paho.mqtt.client as mqtt
import socket
import pandas as pd

def cbMsg(myClient, userdata, message):
    msg = str(message.payload.decode("utf-8")).split(' ')
    print(msg)
    if message.topic == 'state':
        if len(msg) == 2:
            info.loc[msg[0],'Infractor'] = msg[1]
    if message.topic == 'places':
        msLen = len(msg)
        i = 1
        while i < msLen:
            info.loc[msg[0], 'Places'] += (msg[i] + ' ')
            i+=1
        saveExcel(info)

def startmqtt():
    client.loop_start()
    try:
    	client.connect(IP)
    except:
    	raise Exception('mqtt error')
    client.subscribe('state')
    client.subscribe('places')

def saveExcel(df):
    print('guradamos excel')
    writer = pd.ExcelWriter('infoTriathletes.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Results')
    writer.save()

IP = socket.gethostbyname(socket.gethostname())
client = mqtt.Client()
client.on_message = cbMsg #Attach callback 4 subscribed topics
info = pd.read_excel(r'infoTriathletes.xlsx').set_index('Dorsal')
info['Infractor']=''
info['Places']=''
