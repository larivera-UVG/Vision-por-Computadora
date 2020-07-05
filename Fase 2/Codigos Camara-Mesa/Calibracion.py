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
"""
**********
FUNCIONES
**********

Aqui se agregan las funciones que van a ser usadas dentro de los diferentes metodos. 

"""
def distancia2puntos(punto1, punto2):
    pass

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

        
    def get_esquinas(self,frame, canny_value):
        PixCircleValue = 10
        bandera = True
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
        print(contour)
        
        width, height = edge.shape[:2] #para el ancho y alto de la imagen del contorno.
        
        print("este es el width", width)
        print("este es el height", height)
        boardMax = ([0,0], [0,height], [width, 0], [width, height]) #define el borde maximo de la mesa (aproximado)
        
        for i in (0, len(contour)-1):
            center,areaMin, angle = cv.minAreaRect(contour[i])
            print("este es el centro: ", center)
            if (abs(width - height)<3 
                and(height > PixCircleValue-3 
                and (height < PixCircleValue+3) 
                and (width > PixCircleValue-3 and width < PixCircleValue+3))):
                
                if(bandera):
                    for i in range(0,4):
                        esquinas[i] = center
                        bandera = False
                    print("Estas son las esquinas al inicio: ", esquinas)
                else:
                    for i in range(0,4):
                        if (distancia2puntos(boardMax[i], center)<distancia2puntos(boardMax[i], esquinas[i])):
                            esquinas[i] = center;
                    print("Estas son las esquinas al final: ", esquinas)
        
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
Camara.get_esquinas(foto,50)