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

class Application(Frame):
    
    def save_toEXCEL(self):
        print('to excel')
        
    def verificar(self):
        print("Verify")
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
        self.COMBO = ttk.Combobox(self.leftFr)
        self.COMBO.pack(fill='both', side='top')
        self.COMBO["values"] = []
        
        self.rightFr = Frame()
        self.rightFr.config(bg='black')
        self.rightFr.pack(side='left')
        self.CHOOSE = Label(self.rightFr, text="Elige tramposo", bg='black', fg='white')
        self.CHOOSE.pack(fill='x')
        self.imUsr = ImageTk.PhotoImage(Image.open("base.png"))
        self.MAP = Label(self.rightFr, image = self.imUsr)
        self.MAP.pack(side = "top", fill = "both", expand = "yes")
        self.verify = Button(self.rightFr, text="VERIFICAR", bg="green", fg="black", command=self.verificar)
        self.verify.pack(side="bottom")
        
    
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()