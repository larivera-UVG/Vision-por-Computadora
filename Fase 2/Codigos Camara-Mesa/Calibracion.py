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


Canny_Factor = 2.5
Calib_param = 18
Treshold = 1


""" 
**********
FUNCIONES
**********

Aqui se agregan las funciones que van a ser usadas dentro de los diferentes metodos. 

"""
def distancia2puntos(punto1, punto2):
    """
    

    Parameters
    ----------
    punto1 : TYPE
        DESCRIPTION.
    punto2 : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    distanciax = (punto1[0] - punto2[0])**2
    distanciay = (punto1[1] - punto2[1])**2
    return mt.sqrt(distanciax + distanciay) + 0.5

def mayor2float(X1, X2):
    """
    

    Parameters
    ----------
    X1 : TYPE
        DESCRIPTION.
    X2 : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if (X1 > X2):
        return X1
    else:
        return X2;
    
    
def getWiHe(esquina):
    """
    

    Parameters
    ----------
    esquina : TYPE
        DESCRIPTION.

    Returns
    -------
    WiHeMax : TYPE
        DESCRIPTION.

    """

    WiHeMax= []
    W1 = distancia2puntos(esquina[0], esquina[2])
    W2 = distancia2puntos(esquina[1], esquina[3])
    WiMax = mayor2float(W1, W2)
    H1 = distancia2puntos(esquina[0], esquina[1])
    H2 = distancia2puntos(esquina[2], esquina[3])
    HeMax = mayor2float(H1, H2)
    WiHeMax.append(int(WiMax))
    WiHeMax.append(int(HeMax))
    return WiHeMax


def get_esquinas(frame, canny_value, pixelTreshold):
    """
    

    Parameters
    ----------
    frame : TYPE
        DESCRIPTION.
    canny_value : TYPE
        DESCRIPTION.
    pixelTreshold : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    PixCircleValue = 2
    bandera = 1
    esquinas = []
    esquinas_final = []
    img_counter = 0 #contador de imagenes guardadas

    ksize = (3,3) #para el metodo de Canny
    frame_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY) #a blanco y negro para una matriz bidimensional
                                                #es mas facil procesar blanco y negro que color.
    frame_gray = cv.blur(frame_gray, ksize) #difuminado, para quitar detalles extras
    edge = cv.Canny(frame_gray, canny_value, canny_value*Canny_Factor) #Con canny busca los bordes.
        
        #obtiene los contornos de la imagen
    image, contour, hierarchy = cv.findContours(edge, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    #print(contour)
    height_im, width_im = edge.shape[:2]
    boardMax = ([0,0], [0,height_im], [width_im, 0], [width_im, height_im]) #define el borde maximo de la mesa

    #print(len(contour) - 1)       
    for i in range (0, len(contour)-1):
        #print(i)
        rect = cv.minAreaRect(contour[i])
        contour_list = []
        for i in contour:
            approx = cv.approxPolyDP(i,0.01*cv.arcLength(i,True),True)
            area = cv.contourArea(i)
            if ((len(approx) > 8) & (area > 5) ):
                contour_list.append(i)
        cv.drawContours(frame, contour_list,  -1, (255,0,0), 2)
        cv.imshow('Objects Detected',frame)
        #cv.circle(img,center,radius,(0,255,0),2)
        #cv.circle(img,center,radius,(0,255,0),2)
        (x, y), (width, height), angle = rect
        #print("este es el width", width)
        #print("este es el height", height)           
        #print("esta es la diferencia ", (width - height))
        Cx = 0
        Cy = 0
        
        for c in contour_list:
            # compute the center of the contour
            M = cv.moments(c)
            old_Cx = Cx
            old_Cy = Cy
            Cx = int(M["m10"] / M["m00"])
            Cy = int(M["m01"] / M["m00"])
            for i in range (0,4):
                if (distancia2puntos(boardMax[i], (Cx,Cy))<distancia2puntos(boardMax[i], (old_Cx,old_Cy))):
                    esquinas_final.append([Cx,Cy])
            
        """    
        if (abs(width - height)< 2
            and height > PixCircleValue-pixelTreshold 
            and height < PixCircleValue+pixelTreshold
            and width > PixCircleValue-pixelTreshold 
            and width < PixCircleValue+pixelTreshold):
            print("se cumple la condicion")
            #print(bandera)
            if(bandera == 1):
                print("Primera tirada")
                for i in range(0,4):
                    esquinas.append([x,y])
                bandera = 2
                    #print("Estas son las esquinas al inicio: ", esquinas)
            #else:
                #for i in range(0,4):
                    if (distancia2puntos(boardMax[i], (x,y))<distancia2puntos(boardMax[i], esquinas[i])):
                        esquinas_final.append([x,y])
          """              
    print("Estas son las esquinas al final: ", esquinas_final)
    #print("Esquina 1", esquinas_final[1])
    edge_img = "opencv_Cannyframe_{}.png".format(img_counter) #Formato del nombre de la imagen.
                                                    #Guarda el numero de frame (foto) que se tomo.
    cv.imwrite(edge_img, edge) #Guarda la foro
    print("{} Canny Guardado!".format(edge_img)) #mensaje de Ok para el save de la foto.
    img_counter += 1 #aumenta el contador. 
    cv.imshow("prueba", edge)
    return esquinas_final

def getHomogenea(esquina):
    WH = getWiHe(esquina)
    #box0 = np.array([[0, 0], [width, 0], [width, height], [0, height], ], np.float32)
    esquinaFloat= np.array([esquina[0],esquina[2],esquina[1] ,esquina[3],], np.float32)
    print(esquinaFloat)
    esquinasFinales = np.array([[ 0, 0],[float(WH[0]), 0 ],[ 0,float(WH[1])],[float(WH[0]),float(WH[1])],],np.float32)
    M = cv.getPerspectiveTransform(esquinaFloat, esquinasFinales)
    #lambda = getPerspectiveTransform(esquinaFloat, esquinasFinales);
    return M

    
#metodo -> que es capaz de hacer nuestra clase, comportamiento
    
    
class camara():
    def set_camera(self,WIDTH,HEIGHT):
        cam = cv.VideoCapture(0) #abre la camara web
        cam.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
        cam.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        cv.namedWindow("test") #crea la ventana
        return cam
        
    def tomar_foto(self,cam):
        #self.set_camera(WIDTH, HEIGHT)
        """
        
        Returns
        -------
        frame : Foto capturada.

        """

        
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
    
    def Calibrar(self,Snapshot,Calib_param, Treshold):
        Esqui = get_esquinas(Snapshot, Calib_param, Treshold)
        Matrix = getHomogenea(Esqui)
        MyWiHe = getWiHe(Esqui)
        CaliSnapshot = cv.warpPerspective(Snapshot, Matrix, (MyWiHe[0],  MyWiHe[1]))
        cv.imshow("Output Image", CaliSnapshot)
    #imwrite("calisnap.jpg",CaliSnapshot
    #imshow("Output Image", CaliSnapshot);

        
   
        
        
"""
Objeto = mi clase() -> instancia de una clase. 

Tengo un objeto, ahora, vamos a acceder a las propiedades del objeto.

Objeto.metodo
"""      

print("-------Inicializacion del objeto camara ----------")
Camara = camara()
print("-------Seteo de la camara ----------")
cam = Camara.set_camera(960,720)
print("-------Toma de foto ----------")
foto =  Camara.tomar_foto(cam)
print("-------Calibracion ----------")
Camara.Calibrar(foto,Calib_param,Treshold)

