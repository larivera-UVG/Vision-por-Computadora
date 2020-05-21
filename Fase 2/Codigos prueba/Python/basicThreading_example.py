#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programa basico para demostracion de las funciones de la libreria threading
de Python.

@author: Jose P. Guerra

Version:
    
    * Fecha ------ Version ----       Descripcion
    
    10/05/2020 --  0.0.0   ---- Creacion inicial del archivo
    12/05/2020 -- 1.0.0    ---- Cargando librerias iniciales
    17/05/2020 -- 1.1.0    ---- Primeras pruebas multihilos
    21/05/2020 -- 2.0.0    ---- Version final del programa
    
    
    
"""

import threading #cargando la libreria para usar multihilos

"""
El funcionamiento de multi-hilos en python requiere de funciones para ser llamadas
Esto implica, para este ejemplo, que la funcion work sera llamada como argumento para
crear el hilo. 

La funcion puede ser de cualquier tipo y recibir tantos parametros se desee.
"""

def thread(num):
    """Esta funcion imprimiera el numero de hilo creado"""
    print('Hilo: %s' % num)



for i in range(5):
    t = threading.Thread(target=thread, args=(i,)) #asignacion de los hilos a una variable

    t.start() #inicializa el hilo.



