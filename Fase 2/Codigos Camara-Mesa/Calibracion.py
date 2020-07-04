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

    
#metodo -> que es capaz de hacer nuestra clase, comportamiento
    
    
class camara():
    def tomar_foto(self):
        """
        
        Returns
        -------
        frame : Foto capturada.

        """
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

        #cam.release()
        #cv.destroyAllWindows()            
        return frame

        
    def get_esquinas(self,frame, canny_value):
        img_counter = 0
        """
        

        Parameters
        ----------
        frame : frame fotografico (foto a la que se le aplica el procesamiento)
        canny_value : Threshold para el metodo de Canny.

        Returns
        -------
        None.

        """
        ksize = (3,3)
        frame_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        frame_gray = cv.blur(frame_gray, ksize)
        edge = cv.Canny(frame_gray, canny_value, canny_value*1.4)
        contour = cv.findContours(edge, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
        cv.imshow("prueba", edge)
        img_name = "opencv_Cannyframe_{}.png".format(img_counter) #Formato del nombre de la imagen.
                                                    #Guarda el numero de frame (foto) que se tomo.
        cv.imwrite(img_name, frame) #Guarda la foro
        print("{} Canny Guardado!".format(img_name)) #mensaje de Ok para el save de la foto.
        img_counter += 1 #aumenta el contador. 
        
"""
Objeto = mi clase() -> instancia de una clase. 

Tengo un objeto, ahora, vamos a acceder a las propiedades del objeto.

Objeto.metodo
"""      
Camara = camara()
foto =  Camara.tomar_foto()
Camara.get_esquinas(foto,3)