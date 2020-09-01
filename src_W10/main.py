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
import tkinter.messagebox as warning
import os

#Callback para gestión de mensajes
def on_message(myClient, userdata, message):
    global client
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
        if self.configured == True:
            try:
                writer = pd.ExcelWriter('TriTruthOutput.xlsx', engine='xlsxwriter')
                info.to_excel(writer, sheet_name='Results')
                writer.save()
                return ('Ok')
            except Exception:
                warning.showwarning(title='Error guardado de info', message='Error al guardar el excel de datos')
                return ('Error')
        else:
            return ('Ok')
 
    def verificar(self):
        dorsal = self.COMBO.get()
        if dorsal != '':
            values = list(self.COMBO["values"])
            values.remove(dorsal)
            self.COMBO["values"] = values
            self.COMBO.set('')
            info.loc[int(dorsal),'CheckTime'] = time.asctime()
        self.MAP["image"] = self.imBase
  
    def configurar(self):
        try:
            connMqtt()
            getData()
            getMapConfig()
            self.imBase = ImageTk.PhotoImage(Image.open(mapName).resize((800,800)))
            self.MAP["image"] = self.imBase
            self.configured = True
            self.reconn.destroy()
            self.verify['state'] = 'normal'
            self.discard['state'] = 'normal'
            self.EXCEL['state'] = 'normal'
            self.COMBO['state'] = 'normal'
        except Exception as e:
            if e.args[0] == 'mqtt error':
                warning.showwarning(title='Error de mensajería', message='Error al conectar con el broker MQTT')
            elif e.args[0] == 'data error':
                warning.showwarning(title='Error de informacion', message='Error en el archivo de datos excel InfoTriathletes.xlsx')
            elif e.args[0] == 'map error':
                 warning.showwarning(title='Error de archivo', message='Error en el archivo de configuración map.conf')
            elif e.args[1] == 'No such file or directory':
                warning.showwarning(title='Error de archivo', message='Error en el nombre del archivo del mapa en map.conf')
            else:
                warning.showwarning(title='Error', message='Error desconocido \n {}'.format(e.args))
    def descartar(self):
        dorsal = self.COMBO.get()
        if dorsal != '':
            values = list(self.COMBO["values"])
            values.remove(dorsal)
            self.COMBO["values"] = values
            self.COMBO.set('')
            info.loc[int(dorsal),'Places'] = ''
            info.loc[int(dorsal),'Infractor'] = 'NO'
        self.MAP["image"] = self.imBase
        
        
    def newCheater(self, dorsal):
        self.COMBO["values"] = list(self.COMBO["values"]) + [dorsal]
        
    def salida(self):
        if self.save_toEXCEL() == 'Ok':
            self.quit()
        
    def newSelection(self, posArg):
        global BOX, mapName
        dorsal = int(self.COMBO.get())
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
        image = plt.imread(mapName)                           
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
        
        self.QUIT = Button(self.downFr, text="SALIR", command=self.salida )
        self.QUIT.config(bg='red', fg='white')
        self.QUIT.pack(side='left', fill='y')
        
        self.EXCEL = Button(self.downFr, text="EXPORTAR EXCEL", command=self.save_toEXCEL )
        self.EXCEL.config(bg='green', fg='white', state='disabled')
        self.EXCEL.pack(side='right', fill='y')
        
        self.leftFr = Frame()
        self.leftFr.config(bg='black')
        self.leftFr.pack(side='top')
        self.leftFr.pack(side='left')
        self.imLogo = ImageTk.PhotoImage(Image.open("logo.png").resize((250,350)))
        self.LOGO = Label(self.leftFr, image = self.imLogo)
        self.LOGO.pack(side = "top", fill = "both", expand = "yes")
        self.CHOOSE = Label(self.leftFr, text="Elige deportista", bg='black', fg='white')
        self.CHOOSE.pack(fill='x')
        self.COMBO = ttk.Combobox(self.leftFr, state="readonly")
        self.COMBO.pack(fill='both', side='top')
        self.COMBO['state'] = 'disabled'
        self.COMBO.bind("<<ComboboxSelected>>", self.newSelection)
        self.COMBO["values"] = []
        self.reconn = Button(self.leftFr, text="CONFIGURAR", bg="RED", fg="white", command=self.configurar, height=10, width=35)
        self.reconn.pack(side="top")
        
        self.rightFr = Frame()
        self.rightFr.config(bg='black')
        self.rightFr.pack(side='left')
        self.IMAGEN = Label(self.rightFr, text="MAPA BASE", bg='black', fg='white')
        self.IMAGEN.pack(fill='x')
        self.imBase = ImageTk.PhotoImage(Image.open("logo.png").resize((800,800)))
        self.MAP = Label(self.rightFr, image = self.imBase)
        self.MAP.pack(side = "top", fill = "both", expand = "yes")
        self.verify = Button(self.rightFr, text="VERIFICAR", bg="green", fg="black", command=self.verificar, state='disabled')
        self.verify.pack(side="left")
        self.discard = Button(self.rightFr, text="DESCARTAR", bg="blue", fg="white", command=self.descartar, state='disabled')
        self.discard.pack(side="right")
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.toCheck = []
        self.configured = False
        self.configurar()


    
#Iniciar proceso Mqtt
def connMqtt():
    try:
        global client
        os.system('cmd /k ubuntu run sudo service mosquitto start')
        IP = socket.gethostbyname(socket.gethostname())
        client = mqtt.Client()
        client.on_message = on_message #Attach callback 4 subscribed topics
        client.connect(IP)
        client.loop_start()
        client.subscribe('state')
        client.subscribe('places')
    except:
    	raise Exception('mqtt error')
def getData():
    try:
        global info
        info = pd.read_excel(r'infoTriathletes.xlsx').set_index('Dorsal')
        info['Infractor']=''
        info['Places']=''
        info['DropTime']=''
        info['CheckTime']=''
    except:
        raise Exception('data error')
        
def getMapConfig():
    global mapName, BOX
    try:
        with open('map.conf','r') as mapInfo:
            lineNumber = 0
            for line in mapInfo:
                if line[0] != '#':
                    if lineNumber == 0:
                        mapName = line.rstrip()
                        lineNumber += 1
                    elif lineNumber == 1:
                        long1 = float(line)
                        lineNumber += 1
                    elif lineNumber == 2:
                        long2 = float(line)
                        lineNumber += 1
                    elif lineNumber == 3:
                        lat1 = float(line)
                        lineNumber += 1
                    elif lineNumber == 4:
                        lat2 = float(line)
                        lineNumber += 1
        BOX = (long1, long2, lat1, lat2)
    except:
        raise Exception('map error')
        
mapName = ''
BOX = None     
info = None
client = None
root = Tk()
root.title("12 meters. Detection")
app = Application(master=root)
app.mainloop()
root.destroy()