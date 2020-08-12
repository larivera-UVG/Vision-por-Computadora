#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 11:25:03 2020

Un ejemplo mas complejo sobre threading en Python. 
Se toma como ejemplo del laboratorio 6 del curso Electronica Digital 3, de la 
Universidad del Valle de Guatemala, impartido por Luis Rivera para el año 2018

El objetivo principal de este programa es reconstruir el himno nacional de Guatemala.
El himno se divide en 2 archivos "Lab6_primero.txt" y "Lab6_segundo.txt"

Mediante hilos, se pide acceder a estos archivos, colocarlos en un buffer y reconstruir,
en un archivo nuevo, el himno completo. 

Este archivo utiliza la libreria multiprocessing.

@author: Jose P. Guerra

Version:
    
    * Fecha ----- Version   ----       Descripcion
    
    10/08/2020 --  0.0.0    ---- Creacion inicial del archivo
    10/08/2020 --  1.0.0    ---- Version final del archivo
"""

"""
Anotacion inicial:
    
"""

from multiprocessing import Process, Lock

lock = Lock() #Funciona como el semaphore en C. Aunque python tiene una funcion 'semaphore' se tiene un 
                        #mejor control en cuanto a sincronizacion usando este recurso de Lock()

buffer = [] #buffer comun para tener una sola via de escritura. 
cont = 0 #variable que indica que hilo esta trabajando, visualmente ayuda a ver el orden de escritura. 


def read_1():
    
    """
    Las variables globales se definen de esta manera en Python: global x
    Esto sirve para que varias funciones, hilos o tareas, puedan acceder a la misma variable.
    Si esto no se hace, la variable, aunque con el mismo nombre, se toma como local.
    """
    global buffer #buffer general para ambos hilos. Se define global en la funcion, no en la declaracion inicial
    global cont #bandera para ver que hilo funciona. Se define como global para usar solo una y que ambos hilos
                #cambien su valor.
    f = open ('Lab6_primero.txt','r') #Abriendo el primer archivo de texto.
    while(True):
        linea = f.readline() #obteniendo las lineas totales del documento
        
        lock.acquire() #Analogo a semaphore. Bloquea el recurso hasta que se envie la orden de liberarlo.
        cont = 1
        buffer = linea
        f2 = open ('Lab6_reconstruido_multiprocessing.txt','a') #abriendo el archivo donde se va a construir el nuevo texto.
        f2.write(buffer) #escribiendo linea por linea
        f2.close() #al finalizar, se cierra el archivo, para evitar corrupciones
        print(cont)
        lock.release() #libera el recurso para alguien mas 
        #print(buffer)
        if not linea: 
            break #si ya no hay mas lineas, rompe el ciclo. break siempre debe ir en una ciclo
    f.close() #cierra el archivo 1. 
    
def read_2():
    global buffer #buffer general para ambos hilos. Se define global en la funcion, no en la declaracion inicial
    global cont#bandera para ver que hilo funciona. Se define como global para usar solo una y que ambos hilos
                #cambien su valor.
                
    f = open ('Lab6_segundo.txt','r') #Abriendo el segundo archivo de texto.
    while(True):
        linea = f.readline() #obteniendo las lineas totales del documento
        #lock.release()
        lock.acquire()#Analogo a semaphore. Bloquea el recurso hasta que se envie la orden de liberarlo.
        cont = 2
        buffer = linea
        f2 = open ('Lab6_reconstruido.txt','a') #abriendo el archivo donde se va a construir el nuevo texto.
        f2.write(buffer) #escribiendo linea por linea
        f2.close() #al finalizar, se cierra el archivo, para evitar corrupciones
        print(cont)
        lock.release() #libera el recurso para alguien mas 
        
        if not linea:
            break #si ya no hay mas lineas, rompe el ciclo. break siempre debe ir en una ciclo
    f.close() #cierra el archivo 2. 
    
"""

Creacion de un thread o hilo:
Se llama a la librearia de multiprocessing.
Se usa la funcion Process(), esta es la encargada de crear los hilos. En general, puede llevar varios 
parametros pero en este caso se puede usar solamente uno que es el 'target'. Los hilos en python se definen
como funciones normales (como cualquier funcion) pero son llamadas como un target en la funcion Process. Esto
permite que sea usado como un hilo al momento de ejecutar el programa. 

Para inicializar los threads se recurre a la funcion start().

Es posible tener un hilo 'demonio' o daemon, esto es un tipo de hilo que nunca muere hasta que se le indica.
Al inicializar este hilo como se hace en este programa, una vez finalice su proceso, 'mata' al hilo tambien. 

"""

"""___main___"""
    
read1 = Process(target = read_1) #asignacion de los hilos a una variable
read2 = Process(target = read_2) #asignacion de los hilos a una variable
#escribiendo = threading.Thread(target = Escritura) #asignacion de los hilos a una variable
read1.start() #inicializa el hilo.
read2.start() #inicializa el hilo.
#escribiendo.start() #inicializa el hilo.

read1.join()
read2.join()
#escribiendo.join()

    
    




