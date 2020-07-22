#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:26:33 2020

@author: Jose Pablo Guerra

Codigo que implementa Calibracion y generacion de codigos para la mesa de pruebas
Proximamente: detectar la pose de los robots.

7/07/2020: Version 0.1.0 -- Se incluye la GUI con el boton de calibrar y generacion de codigos
                            Se agrega el boton de limpiar pantallas generadas por OpenCV
7/07/2020: Vesion 0.1.1 -- Se agrega un textbox para el numero del generador de codigo, 
                           ademas de corregir su posicion en la GUI
12/07/2020: Version 0.2.0 -- Se agrega el boton para la toma de pose de datos, ademas de las funciones 
                            para reconocer la posicion de los robots. Fallas aun en la deteccion del codigo.
12/07/2020: Version 0.2.1 -- Pruebas preeliminares de rotacion del codigo correctas. Se realizaran mas pruebas
                            para verificar que funcione. Proximo pasos: mejorar la deteccion del codigo.                          
"""


from Calibracion import camara, vector_robot, Robot

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox,QVBoxLayout, QTextEdit,QLineEdit,QInputDialog
import sys
from PySide2.QtGui import QIcon

n = 50 #para el boton1 de capturar
n2 = 50 #para el boton3 del codigo

Canny_Factor = 2.5 #factor de multiplicacion para el limite superior de Canny
Calib_param = 80 #Factor de calibracion para Canny, este factor se puede variar
               #para una mejor deteccion de los bordes circulares.
Treshold = 1

#Tama;o del frame de la camara, de preferencia ajustarlo para que no capture cosas innecesarias
WIDTH = 960
HEIGTH = 720

#Inicializacion del objeto de la camara para el uso en la GUI
camara = camara(0)

#-------------------------------------------------------
#Para la generacion de los codigos y la tome de poses

import cv2 as cv #importando libreria para opencv 
#from Robot import vector_robot, Robot
import numpy as np

SQRTDE2 = 1.41421356
MyPI = 3.14159265

anchoMesa = 14.5
largoMesa = 28.0

GlobalCodePixThreshold = 80
GlobalColorDifThreshold = 10


MyGlobalCannyInf = 185
MyGlobalCannySup = 330
Code_size = 7.0
#Mat GlobalLambda, GlobalCroppedActualSnap;

"""
Definiendo las funciones para la toma de poses. 
"""

def getRobot_Code(calib_snapshot, Canny_inf, Canny_sup, Medida_cod):
    vector = vector_robot()
    blur_size = (3,3)
    height_im, width_im = calib_snapshot.shape[:2]
    
    PixCodeSize = Medida_cod * width_im / anchoMesa
    
    gray_img = cv.cvtColor(calib_snapshot, cv.COLOR_BGR2GRAY)
    gray_blur_img = cv.blur(gray_img, blur_size)
    canny_img = cv.Canny(gray_blur_img, Canny_inf, Canny_sup, apertureSize = 3)

    
    cv.imshow("Canny", canny_img)
    #cv.waitKey(0)
    
    image, contour, hierarchy = cv.findContours(canny_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #cv.drawContours(calib_snapshot, contour,  -1, (255,0,0), 2) #dibuja los contornos
    #canny_img = cv.blur(canny_img, blur_size)
    #print("PixCodeSize: ", PixCodeSize)
    #a = 0
    LastRecCod = 0
    
    a = 0
    print("Este es el maximo del contador",len(contour) - 1)
    for c in contour:
        print(" ")
        print("-----------------")
        #print("Este es el contador",a)
        RecCod = cv.minAreaRect(c)
        #cv.drawContours(calib_snapshot, contour[c],  -1, (10*c + 100,15*c,20*c + 20), 2) #dibuja los contornos
        #cv.waitKey(0)
        #Rx, Ry = RecCod[0] #SingleRecCod.center
        #print("Contornos", RecCod[0])
        #print("Contornos", RecCod[0][0])
        center, size, theta = RecCod #SingleRecCod.size
        center, size = tuple(map(int, center)), tuple(map(int, size))
        #print(center)
        #print("GlobalCodePixThreshold: ", GlobalCodePixThreshold)
        #print("size[0]: ", size[0])
        #print("size[1]: ", size[1])
        #print("Resta entre width y PixCode: ",abs(size[0] - PixCodeSize))
        #print("Resta entre heigth: ",abs(size[1] - PixCodeSize))
        print("-----------------")
        print(" ")
        
        #print("A punto de entrar al primer if")
        #if LastRecCod  != 0:
            #print("abs(center[0] - LastRecCod[0][0])", abs(center[0] - LastRecCod[0][0]))
            #print("abs(center[1] - LastRecCod[1][0])", abs(center[1] - LastRecCod[1][0]))
            
        if (size[0] > 35 and size[1] > 35):
            #cv.drawContours(calib_snapshot, c,  -1, (10,200,20), 2) #dibuja los contornos
            #cv.waitKey(0)
            if a == 0:
                a = 1
                vector.agregar_robot(getRobot_fromSnapshot(RecCod, gray_img))
                LastRecCod = RecCod
                
            elif (((abs(center[0] - LastRecCod[0][0]) > GlobalCodePixThreshold) or (abs(center[1] - LastRecCod[1][0]) > GlobalCodePixThreshold))):
                print("ingresando al segundo if, condicion else")
                print("-----------------")
                print(" ")
                vector.agregar_robot(getRobot_fromSnapshot(RecCod, gray_img))
                LastRecCod = RecCod
                
        """
        if (((abs(size[1] - PixCodeSize) < GlobalCodePixThreshold) and (abs(size[0] - PixCodeSize) < GlobalCodePixThreshold))):
            print(" ")
            print("-----------------")
            print("ingresando al primer if")

                
            if a == 0:
                print("Entre la primera vez de a")
            elif a == 1:
                print("entre la segunda vez de a")
    
            #print("GlobalCodePixThreshold: ", GlobalCodePixThreshold)
            #LastRecCod = RecCod
            #x, y = LastRecCod[0] #LastRecCod.center
            #if a == 1:
                #LastRecCod = RecCod
            #    x, y = LastRecCod[0] #LastRecCod.center

            #if a == 0:
                #a = 1
             #   print("ingresando al segundo if")
             #   print("-----------------")
             #   print(" ")
        
             #   vector.agregar_robot(getRobot_fromSnapshot(RecCod, calib_snapshot))
             #   LastRecCod = RecCod
                #x, y = LastRecCod[0] # LastRecCod.center
                #print(RecCod[0][0])
            if LastRecCod  != 0:
                print("abs(center[0] - LastRecCod[0][0])", abs(center[0] - LastRecCod[0][0]))
                print("abs(center[1] - LastRecCod[1][0])", abs(center[1] - LastRecCod[1][0]))
                
            if LastRecCod == 0:
                print("El LastRecCod esta vacio")
                LastRecCod = RecCod
                
            elif (((abs(center[0] - LastRecCod[0][0]) > GlobalCodePixThreshold) or (abs(center[1] - LastRecCod[1][0]) > GlobalCodePixThreshold))):
                print("ingresando al segundo if, condicion else")
                print("-----------------")
                print(" ")
                vector.agregar_robot(getRobot_fromSnapshot(RecCod, calib_snapshot))
                LastRecCod = RecCod
        a+=1
                #x, y = LastRecCod[0] #LastRecCod.center
            #print("Resta entre centros en x: ", abs(Rx - x))
            #print("Resta entre centros en y: ", abs(Ry - y))
            
        #elif a == 0:
         #   a = 1
          #  print("ingresando al if con a bandera")
           # vector.agregar_robot(getRobot_fromSnapshot(RecCod, calib_snapshot))
            #LastRecCod = RecCod
        """
            
    return vector

def getRobot_fromSnapshot(RecContorno, snap):
    
    # Obtiene el centro, el tama;o y el angulo del contorno.
    center, size, theta = RecContorno

    # Angle correction
    #if theta < -45:
     #   theta += 90

    # Convert to int 
    center, size = tuple(map(int, center)), tuple(map(int, size))
    #print("Este es el nuevo centro", center)

    
    GlobalWidth = snap.shape[1]
    GlobalHeigth = snap.shape[0]
    
    #---------------------------------------------
    #GlobalHeigth,GlobalWidth = snap.shape[:2]
    print(" ")
    print("-----------------")
    print("Ingresando a getRobot_fromSnapshot")
    robot = Robot()
    #print("Primer valor del contorno: ", RecContorno[1] )
    
    #Para obtener el snap recortado.
    height_cont,width_cont = RecContorno[1] #height_cont
    tempWiMitad = SQRTDE2 * size[1] / 2
    tempHeMitad = SQRTDE2 * size[0] / 2
    
    
    Cx = center[0]
    Cy = center[1]


    EscalaColores = []
    
    rows = [int(Cy - tempHeMitad), int(Cy + tempHeMitad)]
    cols = [int(Cx - tempWiMitad), int(Cx + tempWiMitad)]
    #rows_1 = np.array([int(Cy - tempHeMitad), int(Cy + tempHeMitad)])
    #cols_1 = np.array([int(Cx - tempWiMitad), int(Cx + tempWiMitad)])


    #print(RecContorno)
    
    SemiCropCod = snap[rows[0]:rows[1], cols[0]:cols[1]] #hasta aqui todo bien al 19 de julio del 2020.
    #GlobalWidth = SemiCropCod.shape[1]
    #GlobalHeigth = SemiCropCod.shape[0]
    #SemiCropCod_Heigth,SemiCropCod_Width = SemiCropCod.shape[:2]
    #Center_rotate_x = len(rows)
    #Center_rotate_y = len(cols)

    #Obtener matriz de rotacion de la imagen
    M = cv.getRotationMatrix2D(center, theta, 1)
    
    dst = cv.warpAffine(snap, M, (GlobalWidth, GlobalHeigth))
    #image_rotated = cv.warpAffine(SemiCropCod, temp_matRotated, (SemiCropCod_Heigth, SemiCropCod_Width), flags = cv.INTER_CUBIC)
    
    #Final_Crop_rotated = cv.getRectSubPix(image_rotated, (int(height_cont),int(width_cont)), (np.size(rows_1)/2.0, np.size(cols_1)/2.0))
    
    
    Final_Crop_rotated = cv.getRectSubPix(dst, size, center)
    
    #cv.imshow("Init", SemiCropCod) 
    cv.imshow("Rotated", dst) 
    cv.imshow("Final_crop",Final_Crop_rotated)
    #cv.waitKey(0)
    height_Final_Rotated, width_Final_Rotated = Final_Crop_rotated.shape[:2]
    #print("la forma del crop", Final_Crop_rotated.shape)
    #print("El crop", Final_Crop_rotated)
    #print("height_Final_Rotated: ",height_Final_Rotated)
    #print("width_Final_Rotated: ",width_Final_Rotated)
    
    #int EscalaColores[3]; //[2] blaco, [1] gris, [0] negr
    #print("Final_Crop_rotated.shape[1]", Final_Crop_rotated.shape[1])
    #print("Final_Crop_rotated.shape[0]", Final_Crop_rotated.shape[0])
    
    a = 0
    
    if height_Final_Rotated < 40 and width_Final_Rotated < 40:
        a = 1
        ColorSupIzq = 0
        ColorSupDer = 0
        ColorInfDer = 0
        ColorInfIzq = 0
    
    if a == 0:
        temp_ColorSupIzq = Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:40]
        temp_ColorInfIzq = Final_Crop_rotated[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)]
        temp_ColorSupDer = Final_Crop_rotated[int(height_Final_Rotated*1/8):40, 65:100]
        temp_ColorInfDer = Final_Crop_rotated[62:90, 70:90]
        
        ColorSupIzq = temp_ColorSupIzq[int(temp_ColorSupIzq.shape[0]/2),int(temp_ColorSupIzq.shape[1]/2)]
        ColorSupDer = temp_ColorSupDer[int(temp_ColorSupDer.shape[0]/2),int(temp_ColorSupDer.shape[1]/2)]
        ColorInfDer = temp_ColorInfDer[int(temp_ColorInfDer.shape[0]/2),int(temp_ColorInfDer.shape[1]/2)]
        ColorInfIzq = temp_ColorInfIzq[int(temp_ColorInfIzq.shape[0]/2),int(temp_ColorInfIzq.shape[1]/2)]
        #print("temp_ColorSupIzq.shape", temp_ColorSupIzq.shape)
        #print("Midle array image gray sup izq: ", temp_ColorSupIzq[int(temp_ColorSupIzq.shape[0]/2),int(temp_ColorSupIzq.shape[1]/2)])
        #print("Midle array image gray inf izq: ", temp_ColorInfIzq[int(temp_ColorInfIzq.shape[0]/2),int(temp_ColorInfIzq.shape[1]/2)])
        #print("Midle array image gray sup der: ", temp_ColorSupDer[int(temp_ColorSupDer.shape[0]/2),int(temp_ColorSupDer.shape[1]/2)])
        #print("Midle array image gray inf der: ", temp_ColorInfDer[int(temp_ColorInfDer.shape[0]/2),int(temp_ColorInfDer.shape[1]/2)])
        
        #if Final_Crop_rotated.shape[0] > 14 and Final_Crop_rotated.shape[1] > 44:
        #print("int(height_Final_Rotated*1/8)", int(height_Final_Rotated*1/8 + 2))
        #print("Final_Crop_rotated: ", Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:35])
        #cv.imshow("Prueba gris", Final_Crop_rotated[10:20])
        #ColorSupIzq = sum(sum(Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:40]))
            #print(Final_Crop_rotated[15:45, 15:42])
            #ColorSupIzq = (ColorSupIzq_1[0] + ColorSupIzq_1[1] + ColorSupIzq_1[2])/3
        #print("Superior izquierdo")
        #print(ColorSupIzq)
        #print(" ") 
        #cv.imshow("ColorSupIzq_1",Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:35])
            
        #ColorSupDer = sum(sum(Final_Crop_rotated[15:45, 70:105]))
            #ColorSupDer = (ColorSupDer1[0] + ColorSupDer1[1] + ColorSupDer1[2])/3
        #print("Superior derecho")
        #print(ColorSupDer)
        #print(" ") 
        #cv.imshow("supderecho",Final_Crop_rotated[int(height_Final_Rotated*1/8):40, 65:100])
            
        #ColorInfDer = sum(sum(Final_Crop_rotated[62:90, 70:90]))
            #ColorInfDer = (ColorInfDer1[0] + ColorInfDer1[1] + ColorInfDer1[2])/3
        #print("inferior derecho")
        #print(ColorInfDer)
        #print(" ") 
        #cv.imshow("ColorInfDer1",Final_Crop_rotated[62:90, 70:90])
            
        #print("int(height_Final_Rotated*1/4 + 2))",int(height_Final_Rotated*1/4 + 2))
        #ColorInfIzq = sum(sum(Final_Crop_rotated[int(height_Final_Rotated*1/4 + 50):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 25)]))
            #ColorInfIzq = (ColorInfIzq1[0] + ColorInfIzq1[1] + ColorInfIzq1[2])/3
        #print("inferior izquierdo")
        #print(ColorInfIzq)
        #print(" ") 
        #cv.imshow("ColorInfIzq1",Final_Crop_rotated[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)])
        #cv.imshow("ColorMiddleIzq",Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2)+30:int(height_Final_Rotated*1/8 + 30)+30, 10:35])
        #cv.imshow("ColorMiddle",Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2)+30:int(height_Final_Rotated*1/8 + 30)+30, 10+30:35+25])
        #cv.imshow("Color_a0",Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10+30:35+30])
        #cv.imshow("Color_a4",Final_Crop_rotated[int(height_Final_Rotated*1/8)+30:40+30, 65:100])
        #cv.imshow("Color_a6",Final_Crop_rotated[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8)+30:int(height_Final_Rotated*1/8 + 23)+30])
    

        
    for i in range(0,3):
        EscalaColores.append(ColorSupIzq)
        

        #cv.imshow("El crop por partes", Final_Crop_rotated[15:45,70:105])
        
        #cuadro superior izquierdo: 15:45, 15:42
                                        #30 x 25
                                        
       #cuadro inferior izquierda: 70:105, 15:42                                        
       
       #cuadro superior derecho: 15:45, 70:105
       #cuadro inferior derecho: 70:105, 70:105
    tempFloatTheta = theta
    
    #print(ColorSupDer)
    #print(ColorSupIzq)
    #print(ColorInfDer)
    #print(ColorInfIzq)
   # if Final_Crop_rotated.shape[0] > 14 and Final_Crop_rotated.shape[1] > 40:
    #a = 0
    if ((ColorSupDer > ColorSupIzq) and (ColorSupDer > ColorInfDer) and (ColorSupDer > ColorInfIzq)):
        print("90 en contra del reloj")
        print(" ")
        Final_Crop_rotated = cv.rotate(Final_Crop_rotated, cv.ROTATE_90_COUNTERCLOCKWISE)
        tempFloatTheta = tempFloatTheta + 90
        EscalaColores[2] = ColorSupDer
    elif ((ColorInfDer > ColorSupIzq) and (ColorInfDer > ColorSupDer) and (ColorInfDer > ColorInfIzq)):
        print("rotado 180")
        print(" ")
        Final_Crop_rotated = cv.rotate(Final_Crop_rotated,cv.ROTATE_180);
        tempFloatTheta = tempFloatTheta + 180;
        EscalaColores[2] = ColorInfDer
            
    elif ((ColorInfIzq > ColorSupIzq) and (ColorInfIzq > ColorInfDer) and (ColorInfIzq > ColorSupDer)):
        print("90 a favor del reloj")
        print(" ")
        Final_Crop_rotated = cv.rotate(Final_Crop_rotated, cv.ROTATE_90_CLOCKWISE)
        tempFloatTheta = tempFloatTheta - 90
        EscalaColores[2] = ColorInfIzq

    #temp_ColorSupIzq = Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:40]
    #temp_a5 = Final_Crop_rotated[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)]
    #temp_a1 = Final_Crop_rotated[int(height_Final_Rotated*1/8):40, 65:100]
    #temp_a7 = Final_Crop_rotated[62:90, 70:90]
        
    #ColorSupIzq = temp_ColorSupIzq[int(temp_ColorSupIzq.shape[0]/2),int(temp_ColorSupIzq.shape[1]/2)]
    #ColorSupDer = temp_ColorSupDer[int(temp_ColorSupDer.shape[0]/2),int(temp_ColorSupDer.shape[1]/2)]
    #ColorInfDer = temp_ColorInfDer[int(temp_ColorInfDer.shape[0]/2),int(temp_ColorInfDer.shape[1]/2)]
    #ColorInfIzq = temp_ColorInfIzq[int(temp_ColorInfIzq.shape[0]/2),int(temp_ColorInfIzq.shape[1]/2)]
    
    #temp_ColorSupIzq = Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:40]
    temp_a1 = Final_Crop_rotated[int(height_Final_Rotated*1/8):40, 65:100]
    temp_a5 = Final_Crop_rotated[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)]
    temp_a7 = Final_Crop_rotated[int(height_Final_Rotated*1/2) + 15:int(height_Final_Rotated*1/2) + 45, int(height_Final_Rotated*1/2) :int(height_Final_Rotated*1/2) + 26]
        

    a1 = temp_a1[int(temp_a1.shape[0]/2),int(temp_a1.shape[1]/2)]
    a7 = temp_a7[int(temp_a7.shape[0]/2),int(temp_a7.shape[1]/2)]
    a5 = temp_a5[int(temp_a5.shape[0]/2),int(temp_a5.shape[1]/2)]
        #print("temp_ColorSupIzq.shape", temp_ColorSupIzq.shape)
        #print("Midle array image gray sup izq: ", temp_ColorSupIzq[int(temp_ColorSupIzq.shape[0]/2),int(temp_ColorSupIzq.shape[1]/2)])
        #print("Midle array image gray inf izq: ", temp_ColorInfIzq[int(temp_ColorInfIzq.shape[0]/2),int(temp_ColorInfIzq.shape[1]/2)])
        #print("Midle array image gray sup der: ", temp_ColorSupDer[int(temp_ColorSupDer.shape[0]/2),int(temp_ColorSupDer.shape[1]/2)])
        #print("Midle array image gray inf der: ", temp_ColorInfDer[int(temp_ColorInfDer.shape[0]/2),int(temp_ColorInfDer.shape[1]/2)])
        
        #if Final_Crop_rotated.shape[0] > 14 and Final_Crop_rotated.shape[1] > 44:
        #print("int(height_Final_Rotated*1/8)", int(height_Final_Rotated*1/8 + 2))
        #print("Final_Crop_rotated: ", Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:35])
        #cv.imshow("Prueba gris", Final_Crop_rotated[10:20])
        #ColorSupIzq = sum(sum(Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:40]))
            #print(Final_Crop_rotated[15:45, 15:42])
            #ColorSupIzq = (ColorSupIzq_1[0] + ColorSupIzq_1[1] + ColorSupIzq_1[2])/3
        #print("Superior izquierdo")
    #print(ColorSupIzq)
    #print(" ") 
    #cv.imshow("Pivote",Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:35])
            
        #ColorSupDer = sum(sum(Final_Crop_rotated[15:45, 70:105]))
            #ColorSupDer = (ColorSupDer1[0] + ColorSupDer1[1] + ColorSupDer1[2])/3
    #print("Superior derecho")
    #print(ColorSupDer)
    #print(" ") 
    #cv.imshow("Color_a1",Final_Crop_rotated[int(height_Final_Rotated*1/8):40, 65:100])
            
        #ColorInfDer = sum(sum(Final_Crop_rotated[62:90, 70:90]))
            #ColorInfDer = (ColorInfDer1[0] + ColorInfDer1[1] + ColorInfDer1[2])/3
    #print("inferior derecho")
    #print(ColorInfDer)
    #print(" ") 
    
    #cv.imshow("Color_a7",Final_Crop_rotated[int(height_Final_Rotated*1/2) + 15:int(height_Final_Rotated*1/2) + 45, int(height_Final_Rotated*1/2) :int(height_Final_Rotated*1/2) + 26])
            
    #print("int(height_Final_Rotated*1/4 + 2))",int(height_Final_Rotated*1/4 + 2))
        #ColorInfIzq = sum(sum(Final_Crop_rotated[int(height_Final_Rotated*1/4 + 50):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 25)]))
            #ColorInfIzq = (ColorInfIzq1[0] + ColorInfIzq1[1] + ColorInfIzq1[2])/3
    #print("inferior izquierdo")
    #print(ColorInfIzq)
    #print(" ")
    
    #cv.imshow("Color_a5",Final_Crop_rotated[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)])
    #cv.imshow("Color_a2",Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2)+30:int(height_Final_Rotated*1/8 + 30)+30, 10:35])
    #cv.imshow("Color_a3",Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2)+30:int(height_Final_Rotated*1/8 + 30)+30, 10+30:35+25])
    #cv.imshow("Color_a0",Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), int(height_Final_Rotated*1/8)+35:int(height_Final_Rotated*1/8)+65])
    #cv.imshow("Color_a4",Final_Crop_rotated[int(height_Final_Rotated*1/8)+30:40+30, 65:100])
    #cv.imshow("Color_a6",Final_Crop_rotated[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8)+30:int(height_Final_Rotated*1/8 + 23)+30])
    
        #Generando los valores para detectar el codigo.
    temp_a3 = Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2)+30:int(height_Final_Rotated*1/8 + 30)+30, 10+30:35+30]
    a3 = temp_a3[int(temp_a3.shape[0]/2),int(temp_a3.shape[1]/2)]
        
    #print("a3: ", a3)
        
    temp_a2 = Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2)+30:int(height_Final_Rotated*1/8 + 30)+30, 10:35]
    a2 = temp_a2[int(temp_a2.shape[0]/2),int(temp_a2.shape[1]/2)]
    #print("a2: ", a2)
    
    #print("height_Final_Rotated*1/8: ",height_Final_Rotated*1/8)
    temp_a0 = Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), int(height_Final_Rotated*1/8)+35:int(height_Final_Rotated*1/8)+65]
    a0 = temp_a0[int(temp_a0.shape[0]/2),int(temp_a0.shape[1]/2)]
    #print("a0: ", a0)
        
        
    temp_a4 = Final_Crop_rotated[int(height_Final_Rotated*1/8)+30:40+30, 65:100]
    a4 = temp_a4[int(temp_a4.shape[0]/2),int(temp_a4.shape[1]/2)]
    #print("a4: ", a4)
        
    temp_a6 = Final_Crop_rotated[int(height_Final_Rotated*1/4 + 50):int(height_Final_Rotated*1/2 + 60), int(height_Final_Rotated*1/8)+20:int(height_Final_Rotated*1/8+30 + 23)+40]
    a6 = temp_a6[int(temp_a6.shape[0]/2),int(temp_a6.shape[1]/2)]
    #print("a6: ", a6)

        
    code = [a7,a6,a5,a4,a3,a2,a1,a0]
    cv.imshow("Codigo", Final_Crop_rotated)
    cv.waitKey(0)        
    if ((ColorSupIzq <= ColorSupDer) and (ColorSupIzq <= ColorInfDer) and (ColorSupIzq <= ColorInfIzq)):
        EscalaColores[0] = ColorSupIzq
    elif ((ColorSupDer <= ColorSupIzq) and (ColorSupDer <= ColorInfDer) and (ColorSupDer <= ColorInfIzq)):
        EscalaColores[0] = ColorSupDer
    elif ((ColorInfDer <= ColorSupDer) and (ColorInfDer <= ColorSupIzq) and (ColorInfDer <= ColorInfIzq)):
        EscalaColores[0] = ColorInfDer
    else:
        EscalaColores[0] = ColorInfIzq
    

                    
    #print(Matriz_color)
    #Extraemos el codigo binario
    CodigoBinString = ""
    print(code)
    
    for i in range (0, len(code)):
        if code[i] <60:
            CodigoBinString = CodigoBinString + "0"
        elif code[i] >60 and code[i]<80:
            CodigoBinString = CodigoBinString + "1"
            
#    print("CodigoBinString: ",CodigoBinString)
#    temporal_ID = int(CodigoBinString, 2)
#    print("temporal_ID: ", temporal_ID)


    #Guardamos los valores
    if a == 0:
        print("Codibo binario: ",CodigoBinString)
        tempID =int(CodigoBinString, 2)
        tempFloatX = (anchoMesa / GlobalWidth) * Cx;
        tempFloatY = (largoMesa / GlobalHeigth) * Cy;
        tempX = int(tempFloatX)
        tempY = int(tempFloatY)
        tempTheta = int(tempFloatTheta)
        pos = [tempX, tempY, tempTheta]
        print("ID temporal",tempID)
        print("-------------------")
        print(" ")
    else:
        tempID = 0
        tempFloatX = (anchoMesa / GlobalWidth) * Cx;
        tempFloatY = (largoMesa / GlobalHeigth) * Cy;
        tempX = int(tempFloatX)
        tempY = int(tempFloatY)
        tempTheta = int(tempFloatTheta)
        pos = [0, 0, 0]
        

    return robot.set_robot(tempID,"", pos) #averiguar como se hace para pasar este argumento al objeto.

"""
Definiendo a la interfaz grafica. 
"""

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prueba de GUI")
        self.setGeometry(500,400,500,400)
        #self.setIcon()
        self.capturar_button()
        self.limpiar_button()
        self.TxtBox()
        self.codigo_button()
        self.Toma_pose()

    def capturar_button(self):
        btn1 = QPushButton("Capturar", self)
        btn1.move(n,50)
        self.Init_Cam
        btn1.clicked.connect(self.capturar)
    
    def limpiar_button(self):
        btn2 = QPushButton("Limpiar", self)
        btn2.move(n+90,50)
        btn2.clicked.connect(self.limpiar_pantalla)
        
    def codigo_button(self):
        btn3 = QPushButton("Codigo", self)
        btn3.move(n2,90)
        btn3.clicked.connect(self.codigo)
        
    def Toma_pose(self):
        btn4 = QPushButton("Tomar Pose", self)
        btn4.move(n2,140)
        btn4.clicked.connect(self.pose)
        
    def pose(self):
        Snapshot = cv.imread("opencv_CalibSnapshot_0.png")
        getRobot_Code(Snapshot, MyGlobalCannyInf, MyGlobalCannySup, Code_size)
    
    def TxtBox(self):
        self.lineEdit = QLineEdit(self,placeholderText="Ingrese número")
        self.lineEdit.setFixedWidth(120)
        self.lineEdit.move(n2+92,93)
        #vbox = QVBoxLayout(self)
        #vbox.addWidget(self.lineEdit)
        
    def limpiar_pantalla(self):
        camara.destroy_window()
        
    def codigo(self):
        text = self.lineEdit.text()
        if text == '':
            text = '0'
        num = int(text)
        camara.Generar_codigo(num)
        
    def Init_Cam(self):
        camara.initialize(WIDTH, HEIGTH)
        
    def capturar(self):
        foto = camara.get_frame()
        camara.Calibrar(foto,Calib_param,Treshold)
        

            
myapp = QApplication.instance()
if myapp is None: 
    myapp = QApplication(sys.argv)
#myapp = QApplication(sys.argv)
window = Window()
window.show() 
sys.exit(myapp.exec_())
myapp.quit()







