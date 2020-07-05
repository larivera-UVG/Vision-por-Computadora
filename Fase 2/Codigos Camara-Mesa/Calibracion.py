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
import numpy as np
import math as mt
""" 
**********
FUNCIONES
**********

Aqui se agregan las funciones que van a ser usadas dentro de los diferentes metodos. 

"""
def distancia2puntos(punto1, punto2):
    distanciax = (punto1[0] - punto2[0])**2
    distanciay = (punto1[1] - punto2[1])**2
    return mt.sqrt(distanciax + distanciay) + 0.5

def mayor2float(X1, X2):
    if (X1 > X2):
        return X1
    else:
        return X2;
    
    
def getWiHe(esquina):

    WiHeMax= []
    W1 = distancia2puntos(esquina[0], esquina[2])
    W2 = distancia2puntos(esquina[1], esquina[3])
    WiMax = mayor2float(W1, W2)
    H1 = distancia2puntos(esquina[0], esquina[1])
    H2 = distancia2puntos(esquina[2], esquina[3])
    HeMax = mayor2float(H1, H2)
    WiHeMax[0].append(WiMax)
    WiHeMax[1].append(HeMax)
    return WiHeMax

"""
#cap = cv.VideoCapture(0) #VideoCapture(n) n = 0 para otras que no sean la camara principal.
#cap.close()

def Capturar2():
    cam = cv.VideoCapture(0)
    
    cv.namedWindow("test")
    
    img_counter = 0
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error, frame no encontrado")
            break
        cv.imshow("test", frame)
    
        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC presionado
            print("Escape presionado, cerrando...")
            break
        elif k%256 == 32:
            # SPACE presionado
            img_name = "opencv_frame_{}.png".format(img_counter) #Formato del nombre de la imagen.
                                                #Guarda el numero de frame (foto) que se tomo.
            cv.imwrite(img_name, frame) #Guarda la foro
            print("{} Guardado!".format(img_name)) #mensaje de Ok para el save de la foto.
            img_counter += 1 #aumenta el contador. 
        
    return frame
    cam.release()
    cv.destroyAllWindows()
"""
    
#metodo -> que es capaz de hacer nuestra clase, comportamiento
    
    
class camara():
    def tomar_foto(self):
        """
        
        Returns
        -------
        frame : Foto capturada.

        """
        cam = cv.VideoCapture(0) #abre la camara web
        cam.set(cv.CAP_PROP_FRAME_WIDTH, 960)
        cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
            
        cv.namedWindow("test") #crea la ventana
        
        img_counter = 0 #contador para las imagenes capturadas (opcional)
        
        while True: #bucle infinito
            ret, frame = cam.read() #obtiene la informacion de la lectura de la camara
            if not ret:
                print("Error, frame no encontrado") #No hay frame, camara no encontrada
                break
            cv.imshow("test", frame) #muestra el video. 
        
            k = cv.waitKey(1) #k = 1 es para espacio
            if k%256 == 27:
                # ESC presionado para cerrar
                print("Escape presionado, cerrando...")
                break
            elif k%256 == 32:
                # SPACE presionado para capturar foto
                img_name = "opencv_frame_{}.png".format(img_counter) #Formato del nombre de la imagen.
                                                    #Guarda el numero de frame (foto) que se tomo.
                cv.imwrite(img_name, frame) #Guarda la foro
                print("{} Guardado!".format(img_name)) #mensaje de Ok para el save de la foto.
                img_counter += 1 #aumenta el contador. 

        #cam.release()
        #cv.destroyAllWindows()            
        return frame #retorna el frame que se va a utilizar

        
    def get_esquinas(self,frame, canny_value, pixelTreshold):
        PixCircleValue = 8
        bandera = 1
        esquinas = []
        img_counter = 0 #contador de imagenes guardadas
        """
        Metodo que obtiene la imagen capturada y obtiene las esquinas de la mesa.
        Utiliza el metodo de Canny como detector de los bordes

        Parameters
        ----------
        frame : frame fotografico (foto a la que se le aplica el procesamiento)
        canny_value : Threshold para el metodo de Canny.

        Returns
        -------
        None.

        """
        ksize = (3,3) #para el metodo de Canny
        frame_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY) #a blanco y negro para una matriz bidimensional
                                                #es mas facil procesar blanco y negro que color.
        frame_gray = cv.blur(frame_gray, ksize) #difuminado, para quitar detalles extras
        edge = cv.Canny(frame_gray, canny_value, canny_value*1.1) #Con canny busca los bordes.
        
        #obtiene los contornos de la imagen
        image, contour, hierarchy = cv.findContours(edge, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
        #print(contour)
        height_im, width_im = edge.shape[:2]
        boardMax = ([0,0], [0,height_im], [width_im, 0], [width_im, height_im]) #define el borde maximo de la mesa

        #print(len(contour) - 1)       
        for i in range (0, len(contour)-1):
            #print(i)
            rect = cv.minAreaRect(contour[i])
            (x, y), (width, height), angle = rect
            #print("este es el width", width)
            #print("este es el height", height)           
            #print("este es el centro: ", (x,y))
            
            
            
            if (abs(width - height)< (pixelTreshold - 1)
                or height > PixCircleValue-pixelTreshold 
                or height < PixCircleValue+pixelTreshold
                or width > PixCircleValue-pixelTreshold 
                or width < PixCircleValue+pixelTreshold):
                #print("se cumple la condicion")
                #print(bandera)
                if(bandera == 1):
                    #print("Primera tirada")
                    for i in range(0,4):
                        esquinas.append([x,y])
                    bandera = 2
                    #print("Estas son las esquinas al inicio: ", esquinas)
                else:
                    for i in range(0,4):
                        if (distancia2puntos(boardMax[i], (x,y))<distancia2puntos(boardMax[i], esquinas[i])):
                            esquinas[i].append([x,y]);
        #print("Estas son las esquinas al final: ", esquinas)
        print(esquinas[1])
        
        edge_img = "opencv_Cannyframe_{}.png".format(img_counter) #Formato del nombre de la imagen.
                                                    #Guarda el numero de frame (foto) que se tomo.
        cv.imwrite(edge_img, edge) #Guarda la foro
        print("{} Canny Guardado!".format(edge_img)) #mensaje de Ok para el save de la foto.
        img_counter += 1 #aumenta el contador. 
        cv.imshow("prueba", edge)
        
        
"""
Objeto = mi clase() -> instancia de una clase. 

Tengo un objeto, ahora, vamos a acceder a las propiedades del objeto.

Objeto.metodo
"""      
Camara = camara()
foto =  Camara.tomar_foto()
Camara.get_esquinas(foto,60,3)