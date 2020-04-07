# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 14:25:30 2020

@author: Hp
"""

import paho.mqtt.client as mqtt
import socket
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
import time

#Callback para gestión de mensajes
def on_message(myClient, userdata, message):
    msg = str(message.payload.decode("utf-8")).split(' ')
    if message.topic == 'state':
        if len(msg) == 2:
            info.loc[int(msg[0]),'Infractor'] = msg[1]
            if msg[1] == 'NO':#Si no es un infractor
                client.publish('checked',msg[0])
                info.loc[int(msg[0]),'DropTime'] = time.asctime()
    if message.topic == 'places':
        msLen = len(msg)
        i = 1
        while i < msLen:
            info.loc[int(msg[0]), 'Places'] += (msg[i] + ' ')
            i+=1
        if info.loc[int(msg[0]),'Infractor'] == '':
            info.loc[int(msg[0]),'Infractor'] = "SI"
        client.publish('checked',msg[0])
        app.newCheater(int(msg[0]))
        info.loc[int(msg[0]),'DropTime'] = time.asctime()
            
        

class Application(Frame):
    def save_toEXCEL(self):
        writer = pd.ExcelWriter('TriTruthOutput.xlsx', engine='xlsxwriter')
        info.to_excel(writer, sheet_name='Results')
        writer.save()
        
    def newCheater(self, dorsal):
        self.toCheck.append(dorsal)
        self.WATCH["bg"] = "red"
        self.WATCH["text"] = "Nº " + str(dorsal)
        
    def cheat(self):
        if len(self.toCheck) > 0:
            if len(self.toCheck) == 1:
                self.WATCH["bg"] = "white"
                self.WATCH["fg"] = "black"
            dorsal = self.toCheck[0]
            self.toCheck.remove(self.toCheck[0])
            info.loc[dorsal,'Check Time'] = time.asctime()
            self.showPlaces(dorsal)
    
    def showPlaces(self, dorsal):
        BOX = (-6.1898, -5.9724, 37.3748, 37.5829)
        
        pos = pd.DataFrame()
        pos["longitude"] = 0        
        pos["latitude"] = 0
        #Interpreto los lugares del excel
        strPlaces = info.loc[dorsal,"Places"]
        listPlaces = strPlaces.split(' ')
        index=0
        for place in listPlaces:
            if len(place.split('#')) == 3:
                waste, lon, lat = place.split('#')
                pos.loc[index,"longitude"] = float(lon)
                pos.loc[index,"latitude"] = float(lat)  
                index+=1                  
        #Muestro resultados en la imagen   
        image = plt.imread('C:/GitHub/TFG-TriTruth/src_W10/base.png')                           
        fig, axis = plt.subplots(figsize = (20,20)) 
        title = "Lugares tramapa del usuario " + str(dorsal) 
        axis.set_title(title)
        axis.scatter(pos.longitude, pos.latitude, zorder=1, alpha= 0.9, c='r', s=100)        
        axis.set_xlim(BOX[0],BOX[1])        
        axis.set_ylim(BOX[2],BOX[3])        
        axis.imshow(image, zorder=0, extent = BOX, aspect= 'equal')
        imgName = str(dorsal) + "map.png"
        fig.savefig(imgName)
    
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "left"})

        self.EXCEL = Button(self)
        self.EXCEL["text"] = "TO EXCEL",
        self.EXCEL["bg"]   = "white"
        self.EXCEL["command"] = self.save_toEXCEL
        self.EXCEL.pack({"side": "right"})
        
        self.WATCH = Button(self)
        self.WATCH["text"] = "",
        self.WATCH["bg"]   = "white"
        self.WATCH["fg"]   = "white"
        self.WATCH["command"] = self.cheat
        self.WATCH.pack(fill=X)
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.toCheck = []


    
#Iniciar proceso Mqtt
try:
    IP = socket.gethostbyname(socket.gethostname())
    client = mqtt.Client()
    client.on_message = on_message #Attach callback 4 subscribed topics
    info = pd.read_excel(r'infoTriathletes.xlsx').set_index('Dorsal')
    info['Infractor']=''
    info['Places']=''
    info['DropTime']=''
    info['Check Time']=''
    client.connect(IP)
    client.loop_start()
    client.subscribe('state')
    client.subscribe('places')
except:
	raise Exception('mqtt error')

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()