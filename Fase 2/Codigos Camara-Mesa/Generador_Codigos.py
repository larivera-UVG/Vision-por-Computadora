#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 22:12:29 2020

@author: joseguerra
"""
import numpy as np
import cv2 as cv

def CodeGenerator(val):
    if val < 0 or val > 255:
        print("Ingrese un numero valido entre 0 y 255")
        Cod = np.zeros([200,200], dtype = np.uint8)
        return Cod
    num = '{0:08b}'.format(val)
    print(num)
    k = -1
    Cod = np.zeros([200,200], dtype = np.uint8)
    print(Cod)
    for u in range (0,3):
        #print(u)
        for v in range (0,3):
            if k == -1:
                for i in range(u*50+25, u*50+75):
                    for i2 in range(v*50+25,v*50+75):
                        Cod[i,i2] = 255
            else:
                t = num[7-k]
                n = int(t)
                print(n)
                for i3 in range(u*50+25, u*50+75):
                    for i4 in range(v*50+25,v*50+75):
                        #print("escala de grises")
                        Cod[i3,i4] = n * 125
                        #print("grises: ", Cod[i3,i4])
            k = k + 1
            #print("blanco: ", Cod[i,i2])

    return Cod
            
    
M = CodeGenerator(-1)
#print(M.shape)
cam = cv.VideoCapture(0) #abre la camara web
#ret, frame = cam.read() #obtiene la informacion de la lectura de la camar
cv.namedWindow("Cod")
cv.imshow("Cod",M)
cv.imwrite("Cod.jpg",M) 
cv.waitKey(0)  
"""
while True:
    ret, frame = cam.read() #obtiene la informacion de la lectura de la camar
    if not ret:
        print("Error, frame no encontrado")
        break
    cv.imshow("Frame",frame)   
    #cv.imshow("Cod",M)   
"""