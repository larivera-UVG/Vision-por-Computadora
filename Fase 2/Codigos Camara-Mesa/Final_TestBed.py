#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:26:33 2020

@author: joseguerra
"""

import sys  
from Calibracion import camara
import PySide2.QtWidgets as pyside




Canny_Factor = 2.5 #factor de multiplicacion para el limite superior de Canny
Calib_param = 40 #Factor de calibracion para Canny, este factor se puede variar
               #para una mejor deteccion de los bordes circulares.
Treshold = 1

WIDTH = 960
HEIGTH = 720


"""
# Create the Qt Application                                                                         
app = pyside.QApplication(sys.argv)                                                                        
# Create a button, connect it and show it                                                           
button = pyside.QPushButton("Iniciar")                                                                    
#button.clicked.connect()                                                                    
button.show()                                                                                       
# Run the main Qt loop                                                                              
app.exec_()
"""

"""
app = pyside.QApplication([])
window = pyside.QWidget()
layout = pyside.QVBoxLayout()
layout.addWidget(pyside.QPushButton('Top'))
foto = pyside.QPushButton.pressed(Camara.tomar_foto(cam))
layout.addWidget(pyside.QPushButton('Bottom'))
layout.event
window.setLayout(layout)
window.show()
app.exec_()

"""

print("-------Inicializacion del objeto camara ----------")
camara = camara(0)
print("-------Seteo de la camara ----------")
camara.initialize(WIDTH, HEIGTH) 
#cam = Camara.set_camera(960,720)
print("-------Toma de foto ----------")
foto = camara.get_frame()
#foto =  camara.tomar_foto()
print("-------Calibracion ----------")
camara.Calibrar(foto,Calib_param,Treshold)
print("-------Generacion de codigo ----------")
camara.Generar_codigo(10)
