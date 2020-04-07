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
from tkinter import ttk
from PIL import ImageTk, Image

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
        app.newCheater(msg[0])
        info.loc[int(msg[0]),'DropTime'] = time.asctime()
            
        

class Application(Frame):
    def save_toEXCEL(self):
        writer = pd.ExcelWriter('TriTruthOutput.xlsx', engine='xlsxwriter')
        info.to_excel(writer, sheet_name='Results')
        writer.save()
 
    def verificar(self):
        dorsal = self.COMBO.get()
        if dorsal != '':
            values = list(self.COMBO["values"])
            values.remove(dorsal)
            self.COMBO["values"] = values
            self.COMBO.set('')
        self.MAP["image"] = self.imBase
        
        
    def newCheater(self, dorsal):
        self.COMBO["values"] = list(self.COMBO["values"]) + [dorsal]
    
    def newSelection(self, posArg):
        dorsal = int(self.COMBO.get())
        
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
        self.imUsr = ImageTk.PhotoImage(Image.open(imgName).resize((800,800)))
        self.MAP["image"] = self.imUsr
    def createWidgets(self):
        self.downFr = Frame()
        self.downFr.config(bg='blue')
        self.downFr.pack(side='bottom', fill = 'x')
        
        self.QUIT = Button(self.downFr, text="SALIR", command=self.quit )
        self.QUIT.config(bg='red', fg='white')
        self.QUIT.pack(side='left', fill='y')
        
        self.EXCEL = Button(self.downFr, text="EXPORTAR EXCEL", command=self.save_toEXCEL )
        self.EXCEL.config(bg='green', fg='white')
        self.EXCEL.pack(side='right', fill='y')
        
        self.leftFr = Frame()
        self.leftFr.config(bg='black')
        self.leftFr.pack(side='top')
        self.leftFr.pack(side='left')
        self.imLogo = ImageTk.PhotoImage(Image.open("logo.jpg").resize((250,250)))
        self.LOGO = Label(self.leftFr, image = self.imLogo)
        self.LOGO.pack(side = "top", fill = "both", expand = "yes")
        self.CHOOSE = Label(self.leftFr, text="Elige tramposo", bg='black', fg='white')
        self.CHOOSE.pack(fill='x')
        self.COMBO = ttk.Combobox(self.leftFr, state="readonly")
        self.COMBO.pack(fill='both', side='top')
        self.COMBO.bind("<<ComboboxSelected>>", self.newSelection)
        self.COMBO["values"] = []
        
        self.rightFr = Frame()
        self.rightFr.config(bg='black')
        self.rightFr.pack(side='left')
        self.CHOOSE = Label(self.rightFr, text="Elige tramposo", bg='black', fg='white')
        self.CHOOSE.pack(fill='x')
        self.imBase = ImageTk.PhotoImage(Image.open("base.png").resize((800,800)))
        self.MAP = Label(self.rightFr, image = self.imBase)
        self.MAP.pack(side = "top", fill = "both", expand = "yes")
        self.verify = Button(self.rightFr, text="VERIFICAR", bg="green", fg="black", command=self.verificar)
        self.verify.pack(side="bottom")
        
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