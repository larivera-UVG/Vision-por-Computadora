#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 11:45:45 2020

18/07/2020: Version 0.0.0 -- Version inicial del archivo
19/07/2020: Version 0.1.0 -- Se agregan funciones para el modulo de toma de datos de la pose de robots.

@author: joseguerra
"""

import cv2 as cv #importando libreria para opencv 
from Robot import vector_robot, Robot
import numpy as np

SQRTDE2 = 1.41421356
MyPI = 3.14159265

anchoMesa = 14.5
largoMesa = 28.0

GlobalCodePixThreshold = 270
GlobalColorDifThreshold = 20


MyGlobalCannyInf = 94
MyGlobalCannySup = 350
#Mat GlobalLambda, GlobalCroppedActualSnap;

def getRobot_Code(calib_snapshot, Canny_inf, Canny_sup, Medida_cod):
    vector = vector_robot()
    blur_size = (3,3)
    height_im, width_im = calib_snapshot.shape[:2]
    
    PixCodeSize = Medida_cod * width_im / anchoMesa
    
    gray_img = cv.cvtColor(calib_snapshot, cv.COLOR_BGR2GRAY)
    gray_blur_img = cv.blur(gray_img, blur_size)
    canny_img = cv.Canny(gray_blur_img, Canny_inf, Canny_sup, apertureSize = 3)

    
    #cv.imshow("Canny", canny_img)
    #cv.waitKey(0)
    
    image, contour, hierarchy = cv.findContours(canny_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #canny_img = cv.blur(canny_img, blur_size)
    #print("PixCodeSize: ", PixCodeSize)
    #a = 0
    LastRecCod = 0
    
    for c in range (0, len(contour) - 1):
        #print(len(contour) - 1)
        #print("Este es el contador",c)
        RecCod = cv.minAreaRect(contour[c])
        #Rx, Ry = RecCod[0] #SingleRecCod.center
        #print("Contornos", RecCod[0])
        #print("Contornos", RecCod[0][0])
        height_rec, width_rec = RecCod[1] #SingleRecCod.size
        #print("GolbalCodePix: ", GlobalCodePixThreshold)
        #print("Resta entre width y PixCode: ",abs(width_rec - PixCodeSize))
        #print("Resta entre heigth: ",abs(height_rec - PixCodeSize))
        a = 0
        
        print("A punto de entrar al primer if")
        if (((abs(width_rec - PixCodeSize) < GlobalCodePixThreshold) and (abs(height_rec - PixCodeSize) < GlobalCodePixThreshold))):
            print("ingresando al pirmer if")
            print("GlobalCodePixThreshold: ", GlobalCodePixThreshold)
            #LastRecCod = RecCod
            #x, y = LastRecCod[0] #LastRecCod.center
            #if a == 1:
                #LastRecCod = RecCod
            #    x, y = LastRecCod[0] #LastRecCod.center
                
            if c == 0 or a == 0:
                a = 1
                print("ingresando al segundo if")
                vector.agregar_robot(getRobot_fromSnapshot(RecCod, calib_snapshot))
                LastRecCod = RecCod
                #x, y = LastRecCod[0] # LastRecCod.center
                #print(RecCod[0][0])
            elif (((abs(RecCod[0][0] - LastRecCod[0][0]) > GlobalCodePixThreshold) or (abs(RecCod[1][0] - LastRecCod[1][0]) > GlobalCodePixThreshold))):
                print("ingresando al segundo if, condicion else")
                vector.agregar_robot(getRobot_fromSnapshot(RecCod, calib_snapshot))
                LastRecCod = RecCod
                #x, y = LastRecCod[0] #LastRecCod.center
            #print("Resta entre centros en x: ", abs(Rx - x))
            #print("Resta entre centros en y: ", abs(Ry - y))
    return vector

def getRobot_fromSnapshot(RecContorno, snap):
    
    # Obtiene el centro, el tama;o y el angulo del contorno.
    center, size, theta = RecContorno

    # Angle correction
    if theta < -45:
        theta += 90

    # Convert to int 
    center, size = tuple(map(int, center)), tuple(map(int, size))
    #print("Este es el nuevo centro", center)

    
    GlobalWidth = snap.shape[1]
    GlobalHeigth = snap.shape[0]
    
    #---------------------------------------------
    #GlobalHeigth,GlobalWidth = snap.shape[:2]

    print("Ingresando a getRobot_fromSnapshot")
    robot = Robot()
    #print("Primer valor del contorno: ", RecContorno[1] )
    
    #Para obtener el snap recortado.
    height_cont,width_cont = RecContorno[1] #height_cont
    tempWiMitad = SQRTDE2 * width_cont / 2
    tempHeMitad = SQRTDE2 * height_cont / 2
    
    
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
    
    cv.imshow("Init", SemiCropCod) 
    cv.imshow("Rotated", dst) 
    #cv.waitKey(0)
    height_Final_Rotated, width_Final_Rotated = Final_Crop_rotated.shape[:2]
    
    #int EscalaColores[3]; //[2] blaco, [1] gris, [0] negro
    ColorSupIzq = Final_Crop_rotated[int(height_Final_Rotated * 1 / 4), int(width_Final_Rotated * 1 / 4)]
    ColorSupDer = Final_Crop_rotated[int(height_Final_Rotated * 1 / 4), int(width_Final_Rotated * 3 / 4)]
    ColorInfDer = Final_Crop_rotated[int(height_Final_Rotated * 3 / 4), int(width_Final_Rotated * 3 / 4)]
    ColorInfIzq = Final_Crop_rotated[int(height_Final_Rotated * 3 / 4), int(width_Final_Rotated * 1 / 4)]
    
    
    for i in range(0,3):
        EscalaColores.append(ColorSupIzq)

    tempFloatTheta = theta
    
    #print(ColorSupDer)
    #print(ColorSupIzq)
    #print(ColorInfDer)
    #print(ColorInfIzq)
    
    #print(Final_Crop_rotated)
    if ((ColorSupDer.any() > ColorSupIzq.any()) and (ColorSupDer.any() > ColorInfDer.any()) and (ColorSupDer.any() > ColorInfIzq.any())):
        print("90 en contra del reloj")
        Final_Crop_rotated = cv.rotate(Final_Crop_rotated, cv.ROTATE_90_COUNTERCLOCKWISE)
        tempFloatTheta = tempFloatTheta + 90
        EscalaColores[2] = ColorSupDer
    elif ((ColorInfDer.any() > ColorSupIzq.any()) and (ColorInfDer/any() > ColorSupDer.any()) and (ColorInfDer.any() > ColorInfIzq.any())):
        print("rotado 180")
        Final_Crop_rotated = cv.rotate(Final_Crop_rotated,cv.ROTATE_180);
        tempFloatTheta = tempFloatTheta + 180;
        EscalaColores[2] = ColorInfDer
        
    elif ((ColorInfIzq.any() > ColorSupIzq.any()) and (ColorInfIzq.any() > ColorInfDer.any()) and (ColorInfIzq.any() > ColorSupDer.any())):
        print("90 a favor del reloj")
        Final_Crop_rotated = cv.rotate(Final_Crop_rotated, cv.ROTATE_90_CLOCKWISE)
        tempFloatTheta = tempFloatTheta - 90
        EscalaColores[2] = ColorInfIzq
        
    if ((ColorSupIzq.any() <= ColorSupDer.any()) and (ColorSupIzq .any() <= ColorInfDer.any()) and (ColorSupIzq.any() <= ColorInfIzq.any())):
        EscalaColores[0] = ColorSupIzq
    elif ((ColorSupDer.any() <= ColorSupIzq.any()) and (ColorSupDer.any() <= ColorInfDer.any()) and (ColorSupDer.any() <= ColorInfIzq.any())):
        EscalaColores[0] = ColorSupDer
    elif ((ColorInfDer.any() <= ColorSupDer.any()) and (ColorInfDer.any() <= ColorSupIzq.any()) and (ColorInfDer.any() <= ColorInfIzq.any())):
        EscalaColores[0] = ColorInfDer
    else:
        EscalaColores[0] = ColorInfIzq

    cv.imshow("Codigo", Final_Crop_rotated)
    cv.waitKey(0)
    
    Matriz_color = np.zeros(shape=(3,3))


    for u in range (1,4):
        for v in range (1,4):
            #print("Esto va antes del val_color",Final_Crop_rotated[int(height_Final_Rotated * u / 4), int(width_Final_Rotated * v / 4)])
            Val_Color_temp = Final_Crop_rotated[int(height_Final_Rotated * u / 4), int(width_Final_Rotated * v / 4)]
            print("Val_Color_temp: ",Val_Color_temp)
            Matriz_color[u - 1][v - 1] = Val_Color_temp[0]
            #print(Val_Color_temp)
            if ((Val_Color_temp.any() < EscalaColores[2].any() - GlobalColorDifThreshold) and (Val_Color_temp.any() > EscalaColores[0].any() + GlobalColorDifThreshold)):
                EscalaColores[1] = Val_Color_temp
    print(Matriz_color)
    #Extraemos el codigo binario
    CodigoBinString = ""
    for  u in range (0, 3):
        for v in range(0,3):
            if ((u == 0) and (v == 0)):
                CodigoBinString = CodigoBinString;
                print(EscalaColores[1] - GlobalColorDifThreshold)
            elif ((Matriz_color[u][v] > EscalaColores[1].any() - GlobalColorDifThreshold) and (Matriz_color[u][v] < EscalaColores[1].any() + GlobalColorDifThreshold)):
                CodigoBinString = CodigoBinString + "1"
            else:
                CodigoBinString = CodigoBinString + "0"


    #Guardamos los valores
    print("Codibo binario: ",CodigoBinString)
    tempID =int(CodigoBinString, 2)
    tempFloatX = (anchoMesa / GlobalWidth) * Cx;
    tempFloatY = (largoMesa / GlobalHeigth) * Cy;
    tempX = int(tempFloatX)
    tempY = int(tempFloatY)
    tempTheta = int(tempFloatTheta)
    pos = [tempX, tempY, tempTheta]
    print("ID temporal",tempID)
    print(pos)
    print(" ")


    return robot.set_robot(tempID,"", pos) #averiguar como se hace para pasar este argumento al objeto.


Snapshot = cv.imread("opencv_CalibSnapshot_0.png")
getRobot_Code(Snapshot, MyGlobalCannyInf, MyGlobalCannySup, 2.99)

    