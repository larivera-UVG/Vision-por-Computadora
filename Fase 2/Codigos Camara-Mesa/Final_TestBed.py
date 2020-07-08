#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:26:33 2020

@author: Jose Pablo Guerra

Codigo que implementa Calibracion y generacion de codigos para la mesa de pruebas
Proximamente: detectar la pose de los robots.

7/07/2020: Version 0.1.0 -- Se incluye la GUI con el boton de calibrar y generacion de codigos
                            Se agrega el boton de limpiar pantallas generadas por OpenCV
7/07/2020: Vesion 0.1.1 -- Se agrega un textbox para el numero del generador de codigo, 
                           ademas de corregir su posicion en la GUI
"""


from Calibracion import camara

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox,QVBoxLayout, QTextEdit,QLineEdit,QInputDialog
import sys
from PySide2.QtGui import QIcon

Canny_Factor = 2.5 #factor de multiplicacion para el limite superior de Canny
Calib_param = 40 #Factor de calibracion para Canny, este factor se puede variar
               #para una mejor deteccion de los bordes circulares.
Treshold = 1

#Tama;o del frame de la camara, de preferencia ajustarlo para que no capture cosas innecesarias
WIDTH = 960
HEIGTH = 720

#Inicializacion del objeto de la camara para el uso en la GUI
camara = camara(0)



class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prueba de GUI")
        self.setGeometry(500,400,500,400)
        #self.setIcon()
        self.capturar_button()
        self.limpiar_button()
        self.TxtBox()
        self.codigo_button()

    def capturar_button(self):
        btn1 = QPushButton("Capturar", self)
        btn1.move(50,50)
        self.Init_Cam
        btn1.clicked.connect(self.capturar)
    
    def limpiar_button(self):
        btn2 = QPushButton("Limpiar", self)
        btn2.move(50,70)
        btn2.clicked.connect(self.limpiar_pantalla)
        
    def codigo_button(self):
        btn3 = QPushButton("Codigo", self)
        btn3.move(50,90)
        btn3.clicked.connect(self.codigo)
    
    def TxtBox(self):
        self.lineEdit = QLineEdit(self,placeholderText="Ingrese número")
        self.lineEdit.setFixedWidth(120)
        self.lineEdit.move(142,93)
        #vbox = QVBoxLayout(self)
        #vbox.addWidget(self.lineEdit)
        
    def limpiar_pantalla(self):
        camara.destroy_window()
        
    def codigo(self):
        text = self.lineEdit.text()
        if text == '':
            text = '0'
        num = int(text)
        camara.Generar_codigo(num)
        
    def Init_Cam(self):
        camara.initialize(WIDTH, HEIGTH)
        
    def capturar(self):
        foto = camara.get_frame()
        camara.Calibrar(foto,Calib_param,Treshold)
    

myapp = QApplication(sys.argv)
window = Window()
window.show()
 
myapp.exec_()
sys.exit()







