#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Un ejemplo mas complejo sobre threading en Python. 
Se toma como ejemplo del laboratorio 6 del curso Electronica Digital 3, de la 
Universidad del Valle de Guatemala, impartido por Luis Rivera para el año 2018

El objetivo principal de este programa es reconstruir el himno nacional de Guatemala.
El himno se divide en 2 archivos "Lab6_primero.txt" y "Lab6_segundo.txt"

Mediante hilos, se pide acceder a estos archivos, colocarlos en un buffer y reconstruir,
en un archivo nuevo, el himno completo. 

@author: Jose P. Guerra

Version:
    
    * Fecha ----- Version   ----       Descripcion
    
    10/05/2020 --  0.0.0    ---- Creacion inicial del archivo
    12/05/2020 --  1.0.0    ---- Cargando librerias iniciales
    21/05/2020 --  1.1.0    ---- Lectura de archivos de texto en hilos distintos
    21/05/2020 --  1.2.0    ---- Lectura linea por linea del archivo de texto
    21/05/2020 --  1.3.0    ---- Escritura linea por linea en un archivo nuevo, aun no hay orden
    
    
    
"""


import threading #importando la libreria de multi-hilos
import time as t #para los delay

sem = threading.Semaphore()

def read_1():
    f = open ('Lab6_primero.txt','r')
    while(True):
        sem.acquire()
        linea = f.readline()
        f2 = open ('Lab6_reconstruido.txt','a')
        f2.write(linea)
        f2.close()
        sem.release()
        if not linea:
            break
    f.close()
    
def read_2():
    f = open ('Lab6_segundo.txt','r')
    while(True):
        sem.acquire()
        linea = f.readline()
        f2 = open ('Lab6_reconstruido.txt','a')
        f2.write(linea)
        f2.close()
        sem.release()
        if not linea:
            break
    f.close()
    
    
    
read1 = threading.Thread(target = read_1) #asignacion de los hilos a una variable
read2 = threading.Thread(target = read_2) #asignacion de los hilos a una variable
read1.start() #inicializa el hilo.
read2.start() #inicializa el hilo.

    
    
"""___main___"""



