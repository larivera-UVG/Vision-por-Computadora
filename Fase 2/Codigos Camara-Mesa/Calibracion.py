#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jose Pablo Guerra 
Programa de calibracion para la camara utilizando OpenCV
 
***********************
Versionado:
***********************
4/07/2020: Creacion inicial del archivo

***********************
Anotaciones iniciales:
***********************

De preferencia utilizar la suite de anaconda, esto permite instalar los paquetes 
de manera mas adecuada y evitar errores entre versionres o que las librerias 
no esten correctamente linkeadas al compilador. 

Basado en el codigo realizado por Andre Rodas 
"""


import cv2 as cv #importando libreria para opencv 
import ctypes
import pathlib

#cap = cv.VideoCapture(0) #VideoCapture(n) n = 0 para otras que no sean la camara principal.
#cap.close()

if __name__ == "__main__":
    # Load the shared library into ctypes
    libname = pathlib.Path().absolute() / "calibracam.h"
    c_lib = ctypes.CDLL(libname)