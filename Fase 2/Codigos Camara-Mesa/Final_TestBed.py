#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:26:33 2020

@author: joseguerra
"""


from Calibracion import camara


from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import sys
from PySide2.QtGui import QIcon

Canny_Factor = 2.5 #factor de multiplicacion para el limite superior de Canny
Calib_param = 40 #Factor de calibracion para Canny, este factor se puede variar
               #para una mejor deteccion de los bordes circulares.
Treshold = 1

WIDTH = 960
HEIGTH = 720
camara = camara(0)

#camara = camara(0)
#camara.initialize(WIDTH, HEIGTH)


#print("-------Inicializacion del objeto camara ----------")
#camara = camara(0)
#print("-------Seteo de la camara ----------")
#camara.initialize(WIDTH, HEIGTH) 
#cam = Camara.set_camera(960,720)
#print("-------Toma de foto ----------")
#oto = camara.get_frame()
#foto =  camara.tomar_foto()
#print("-------Calibracion ----------")
#camara.Calibrar(foto,Calib_param,Treshold)
#print("-------Generacion de codigo ----------")
#camara.Generar_codigo(10)




class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prueba de GUI")
        self.setGeometry(500,400,500,400)
        #self.setIcon()
        self.capturar_button()
        self.limpiar_button()

    def capturar_button(self):
        btn1 = QPushButton("Capturar", self)
        btn1.move(50,100)
        self.Init_Cam
        btn1.clicked.connect(self.capturar)
    
    def limpiar_button(self):
        btn1 = QPushButton("Limpiar", self)
        btn1.move(20,200)
        btn1.clicked.connect(self.limpiar_pantalla)
        
    def limpiar_pantalla(self):
        camara.destroy_window()
        
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







