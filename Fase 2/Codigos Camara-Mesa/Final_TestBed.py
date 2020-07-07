#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:26:33 2020

@author: joseguerra
"""

from Calibracion import camara
import PyQt5 as qt

Canny_Factor = 2.5 #factor de multiplicacion para el limite superior de Canny
Calib_param = 40 #Factor de calibracion para Canny, este factor se puede variar
               #para una mejor deteccion de los bordes circulares.
Treshold = 1



print("-------Inicializacion del objeto camara ----------")
Camara = camara()
print("-------Seteo de la camara ----------")
cam = Camara.set_camera(960,720)
print("-------Toma de foto ----------")
foto =  Camara.tomar_foto(cam)
print("-------Calibracion ----------")
Camara.Calibrar(foto,Calib_param,Treshold)
print("-------Generacion de codigo ----------")
Camara.Generar_codigo(10)
