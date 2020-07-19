#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 11:45:45 2020

@author: joseguerra
"""

import cv2 as cv #importando libreria para opencv 
from Obtener_pos import vector_robot

SQRTDE2 = 1.41421356
MyPI = 3.14159265

anchoMesa = 128.4
largoMesa = 88.4

GlobalCodePixThreshold = 5
GlobalColorDifThreshold = 20
GlobalWidth = 0 
GlobalHeigth = 0
#Mat GlobalLambda, GlobalCroppedActualSnap;

def getRobot_Code(snapshot, Canny_inf, Canny_sup, Medida_cod):
    vector = vector_robot()
    blur_size = [3,3]
    height_im, width_im = snapshot.shape[:2]
    PixCodeSize = Medida_cod * width_im / anchoMesa
    gray_img = cv.cvtColor(snapshot, cv.COLOR_BGR2GRAY)
    gray_blur_img = cv.blur(gray_img, blur_size)
    canny_img = cv.Canny(gray_blur_img, Canny_inf, Canny_sup)
    image, contour, hierarchy = cv.findContours(canny_img, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    canny_img = cv.blur(canny_img, blur_size)
    
    a = 0
    for i in contour:
        RecCod = cv.minAreaRect(i)
        Rx, Ry = RecCod[0] #SingleRecCod.center
        height_rec, width_rec = RecCod[1] #SingleRecCod.size

        if (((abs(width_rec - PixCodeSize) < GlobalCodePixThreshold) and (abs(height_rec - PixCodeSize) < GlobalCodePixThreshold))):
            if a == 0:
                a = 1
                vector.agregar_robot(getRobot_fromSnapshot(snapshot))
                LastRecCod = RecCod
                x, y = LastRecCod[0] # LastRecCod.center
            elif (((abs(Rx - x) > GlobalCodePixThreshold) or (abs(Ry - y) > GlobalCodePixThreshold))):
                vector.agregar_robot(getRobot_fromSnapshot(snapshot))
                LastRecCod = RecCod
                x, y = LastRecCod[0] #LastRecCod.center
    return vector

def getRobot_fromSnapshot(RecContorno):
    height_cont, width_cont = RecContorno[1]
    tempWiMitad = SQRTDE2 * width_cont / 2
    tempHeMitad = SQRTDE2 * height_cont / 2
    Cx, Cy = RecContorno[0]
    angle = RecContorno[2]

    EscalaColores = []
    rows = [(Cy - tempHeMitad), (Cy + tempHeMitad)]
    cols = [(Cx - tempWiMitad), (Cx + tempWiMitad)]
    
    SemiCropCod = RecContorno[rows[0]:rows[1], cols[0]:cols[1]]
    
    temp_matRotated = cv.getRotationMatrix2D([Cx,Cy], angle, 1.0)
    image_rotated = cv.warpAffine(SemiCropCod, temp_matRotated, (len(rows), len(cols)), flags=cv.INTER_CUBIC)
    
    Final_Crop_rotated = cv.getRectSubPix(image_rotated, len(RecContorno), (len(rows)/2.0, len(cols)/2.0))
    
    
    Final_Crop_rotated = cv.cvtColor(Final_Crop_rotated, cv.COLOR_BGR2GRAY)
    height_Final_Rotated, width_Final_Rotated = Final_Crop_rotated[1]
    
    #int EscalaColores[3]; //[2] blaco, [1] gris, [0] negro
    ColorSupIzq = Final_Crop_rotated(height_Final_Rotated * 1 / 4, width_Final_Rotated * 1 / 4)
    ColorSupDer = Final_Crop_rotated(height_Final_Rotated * 1 / 4, width_Final_Rotated * 3 / 4)
    ColorInfDer = Final_Crop_rotated(height_Final_Rotated * 3 / 4, width_Final_Rotated * 3 / 4)
    ColorInfIzq = Final_Crop_rotated(height_Final_Rotated * 3 / 4, width_Final_Rotated * 1 / 4)
    EscalaColores[0] = EscalaColores[1] = EscalaColores[2] = ColorSupIzq
    tempFloatTheta = angle
    

    
    if ((ColorSupDer > ColorSupIzq) and (ColorSupDer > ColorInfDer) and (ColorSupDer > ColorInfIzq)):
        Final_Crop_rotated = cv.rotate(Final_Crop_rotated, cv.ROTATE_90_COUNTERCLOCKWISE)
        tempFloatTheta = tempFloatTheta + 90
        EscalaColores[2] = ColorSupDer
    elif ((ColorInfDer > ColorSupIzq) and (ColorInfDer > ColorSupDer) and (ColorInfDer > ColorInfIzq)):
        Final_Crop_rotated = cv.rotate(Final_Crop_rotated,cv.ROTATE_180);
        tempFloatTheta = tempFloatTheta + 180;
        EscalaColores[2] = ColorInfDer
        
    elif ((ColorInfIzq > ColorSupIzq) and (ColorInfIzq > ColorInfDer) and (ColorInfIzq > ColorSupDer)):
        Final_Crop_rotated = cv.rotate(Final_Crop_rotated, cv.ROTATE_90_CLOCKWISE)
        tempFloatTheta = tempFloatTheta - 90
        EscalaColores[2] = ColorInfIzq
        
    if ((ColorSupIzq <= ColorSupDer) and (ColorSupIzq <= ColorInfDer) and (ColorSupIzq <= ColorInfIzq)):
        EscalaColores[0] = ColorSupIzq
    elif ((ColorSupDer <= ColorSupIzq) and (ColorSupDer <= ColorInfDer) and (ColorSupDer <= ColorInfIzq)):
        EscalaColores[0] = ColorSupDer
    elif ((ColorInfDer <= ColorSupDer) and (ColorInfDer <= ColorSupIzq) and (ColorInfDer <= ColorInfIzq)):
        EscalaColores[0] = ColorInfDer
    else:
        EscalaColores[0] = ColorInfIzq

    cv.imshow("Codigo", Final_Crop_rotated)
    cv.waitKey(0)
    
    Matriz_color = []
    
    for u in range (0,4):
        for v in range (1,4):
            Val_Color_temp = Final_Crop_rotated((height_Final_Rotated * u / 4), (width_Final_Rotated * v / 4))
            Matriz_color[u - 1][v - 1] = Val_Color_temp
            if ((Val_Color_temp < EscalaColores[2] - GlobalColorDifThreshold) and (Val_Color_temp > EscalaColores[0] + GlobalColorDifThreshold)):
                EscalaColores[1] = Val_Color_temp
    
    #Extraemos el codigo binario
    CodigoBinString = ""
    for  u in range (0, 3):
        for v in range(0,3):
            if ((u == 0) and (v == 0)):
                CodigoBinString = CodigoBinString;
            elif ((Matriz_color[u][v] > EscalaColores[1] - GlobalColorDifThreshold) and (Matriz_color[u][v] < EscalaColores[1] + GlobalColorDifThreshold)):
                CodigoBinString = CodigoBinString + "1"
            else:
                CodigoBinString = CodigoBinString + "0"


    #Guardamos los valores
    tempID =int(CodigoBinString, 2)
    tempFloatX = (anchoMesa / GlobalWidth) * Cx;
    tempFloatY = (largoMesa / GlobalHeigth) * Cy;
    tempX = int(tempFloatX)
    tempY = int(tempFloatY)
    tempTheta = int(tempFloatTheta)
    return robot(tempID,"", tempX, tempY, tempTheta) #averiguar como se hace para pasar este argumento al objeto.

    