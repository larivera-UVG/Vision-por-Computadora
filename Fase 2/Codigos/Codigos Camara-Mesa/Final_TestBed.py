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
"""


from Calibracion import camara, vector_robot, Robot

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox,QVBoxLayout, QTextEdit,QLineEdit,QInputDialog
import sys
from PySide2.QtGui import QIcon

n = 50 #para el boton1 de capturar
n2 = 50 #para el boton3 del codigo

Canny_Factor = 2.5 #factor de multiplicacion para el limite superior de Canny
Calib_param = 40 #Factor de calibracion para Canny, este factor se puede variar
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

GlobalCodePixThreshold = 210
GlobalColorDifThreshold = 1


MyGlobalCannyInf = 97
MyGlobalCannySup = 380
Code_size = 3
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

    
    #cv.imshow("Canny", canny_img)
    #cv.waitKey(0)
    
    image, contour, hierarchy = cv.findContours(canny_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #cv.drawContours(calib_snapshot, contour,  -1, (255,0,0), 2) #dibuja los contornos
    #canny_img = cv.blur(canny_img, blur_size)
    #print("PixCodeSize: ", PixCodeSize)
    #a = 0
    LastRecCod = 0
    
    a = 0
    for c in range (0, len(contour) - 1):
        print(" ")
        print("-----------------")
        print("Este es el maximo del contador",len(contour) - 1)
        print("Este es el contador",c)
        RecCod = cv.minAreaRect(contour[c])
        #cv.drawContours(calib_snapshot, contour[c],  -1, (10*c + 100,15*c,20*c + 20), 2) #dibuja los contornos
        #cv.waitKey(0)
        #Rx, Ry = RecCod[0] #SingleRecCod.center
        #print("Contornos", RecCod[0])
        #print("Contornos", RecCod[0][0])
        center, size, theta = RecCod #SingleRecCod.size
        center, size = tuple(map(int, center)), tuple(map(int, size))
        #print(center)
        print("GolbalCodePix: ", GlobalCodePixThreshold)
        print("Resta entre width y PixCode: ",abs(size[0] - PixCodeSize))
        print("Resta entre heigth: ",abs(size[1] - PixCodeSize))
        print("-----------------")
        print(" ")
        
        #print("A punto de entrar al primer if")
        if (((abs(size[1] - PixCodeSize) < GlobalCodePixThreshold) and (abs(size[0] - PixCodeSize) < GlobalCodePixThreshold))):
            print(" ")
            print("-----------------")
            print("ingresando al pirmer if")
            #print("GlobalCodePixThreshold: ", GlobalCodePixThreshold)
            #LastRecCod = RecCod
            #x, y = LastRecCod[0] #LastRecCod.center
            #if a == 1:
                #LastRecCod = RecCod
            #    x, y = LastRecCod[0] #LastRecCod.center
            if c > 0:
                print(abs(center[0] - LastRecCod[0][0]))
            if c == 0:
                #a = 1
                print("ingresando al segundo if")
                print("-----------------")
                print(" ")
        
                vector.agregar_robot(getRobot_fromSnapshot(RecCod, calib_snapshot))
                LastRecCod = RecCod
                #x, y = LastRecCod[0] # LastRecCod.center
                #print(RecCod[0][0])
            elif (((abs(center[0] - LastRecCod[0][0]) > GlobalCodePixThreshold) or (abs(center[1] - LastRecCod[1][0]) > GlobalCodePixThreshold))):
                print("ingresando al segundo if, condicion else")
                print("-----------------")
                print(" ")
        
                vector.agregar_robot(getRobot_fromSnapshot(RecCod, calib_snapshot))
                LastRecCod = RecCod
                #x, y = LastRecCod[0] #LastRecCod.center
            #print("Resta entre centros en x: ", abs(Rx - x))
            #print("Resta entre centros en y: ", abs(Ry - y))
            
        elif a == 0:
            a = 1
            print("ingresando al if con a bandera")
            vector.agregar_robot(getRobot_fromSnapshot(RecCod, calib_snapshot))
            LastRecCod = RecCod
            
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
    
    cv.imshow("Init", SemiCropCod) 
    cv.imshow("Rotated", dst) 
    cv.imshow("Final_crop",Final_Crop_rotated)
    #cv.waitKey(0)
    height_Final_Rotated, width_Final_Rotated = Final_Crop_rotated.shape[:2]
    #print("la forma del crop", Final_Crop_rotated.shape)
    #print("El crop", Final_Crop_rotated)
    #print("height_Final_Rotated: ",height_Final_Rotated)
    #print("width_Final_Rotated: ",width_Final_Rotated)
    
    #int EscalaColores[3]; //[2] blaco, [1] gris, [0] negr
    print("Final_Crop_rotated.shape[1]", Final_Crop_rotated.shape[1])
    print("Final_Crop_rotated.shape[0]", Final_Crop_rotated.shape[0])
    if Final_Crop_rotated.shape[0] > 14 and Final_Crop_rotated.shape[1] > 44:
    
        print("int(height_Final_Rotated*1/8)", int(height_Final_Rotated*1/8))
        ColorSupIzq = sum(sum(sum(Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 15:50])))
        #print(Final_Crop_rotated[15:45, 15:42])
        #ColorSupIzq = (ColorSupIzq_1[0] + ColorSupIzq_1[1] + ColorSupIzq_1[2])/3
        print("Superior izquierdo")
        print(ColorSupIzq)
        print(" ") 
        cv.imshow("ColorSupIzq_1",Final_Crop_rotated[int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 30), 15:50])
        
        ColorSupDer = sum(sum(sum(Final_Crop_rotated[15:45, 70:105])))
        #ColorSupDer = (ColorSupDer1[0] + ColorSupDer1[1] + ColorSupDer1[2])/3
        print("Superior derecho")
        print(ColorSupDer)
        print(" ") 
        cv.imshow("supderecho",Final_Crop_rotated[15:45, 70:105])
        
        ColorInfDer = sum(sum(sum(Final_Crop_rotated[70:105, 70:105])))
        #ColorInfDer = (ColorInfDer1[0] + ColorInfDer1[1] + ColorInfDer1[2])/3
        print("inferior derecho")
        print(ColorInfDer)
        print(" ") 
        cv.imshow("ColorInfDer1",Final_Crop_rotated[80:110, 70:105])
        print("int(height_Final_Rotated*1/4 + 2))",int(height_Final_Rotated*1/4 + 2))
        ColorInfIzq = sum(sum(sum(Final_Crop_rotated[int(height_Final_Rotated*1/4 + 55):int(height_Final_Rotated*1/2 + 30), int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 40)])))
        #ColorInfIzq = (ColorInfIzq1[0] + ColorInfIzq1[1] + ColorInfIzq1[2])/3
        print("inferior izquierdo")
        print(ColorInfIzq)
        print(" ") 
        cv.imshow("ColorInfIzq1",Final_Crop_rotated[int(height_Final_Rotated*1/4 + 50):int(height_Final_Rotated*1/2 + 45), int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 35)])
    else:
        ColorSupIzq = 0
        ColorInfIzq = 0
        ColorSupDer = ColorSupIzq
        ColorInfDer = ColorInfIzq
    #print(Final_Crop_rotated.shape[0])
    
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
    if Final_Crop_rotated.shape[0] > 14 and Final_Crop_rotated.shape[1] > 40:
        a = 0
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

            
        if ((ColorSupIzq <= ColorSupDer) and (ColorSupIzq <= ColorInfDer) and (ColorSupIzq <= ColorInfIzq)):
            EscalaColores[0] = ColorSupIzq
        elif ((ColorSupDer <= ColorSupIzq) and (ColorSupDer <= ColorInfDer) and (ColorSupDer <= ColorInfIzq)):
            EscalaColores[0] = ColorSupDer
        elif ((ColorInfDer <= ColorSupDer) and (ColorInfDer <= ColorSupIzq) and (ColorInfDer <= ColorInfIzq)):
            EscalaColores[0] = ColorInfDer
        else:
            EscalaColores[0] = ColorInfIzq
    else:
        EscalaColores[0] = 0
        EscalaColores[1] = 0
        EscalaColores[2] = 0
        a = 1
    
    Matriz_color = np.zeros(shape=(3,3))


    for u in range (1,4):
        for v in range (1,4):
            #print("Esto va antes del val_color",Final_Crop_rotated[int(height_Final_Rotated * u / 4), int(width_Final_Rotated * v / 4)])
            #print("Tama;o del recorte",np.shape(Final_Crop_rotated.shape))
            #print("El recorte",Final_Crop_rotated[4,3])
            #print("Indice del recorte height: ", int(height_Final_Rotated * u / 6))
            #print("Indice del recorte width: ",int(width_Final_Rotated * v / 6))
            
            pix1 = int(height_Final_Rotated * u / 4)
            pix2 = int(width_Final_Rotated * v / 4)
            
            if pix2 > 3:
                pix2 = 3
                
            if a == 1:
                pass
            else:
                Val_Color_temp = Final_Crop_rotated[pix1, pix2]
                Val_Color_temp = (Val_Color_temp[0] + Val_Color_temp[1] + Val_Color_temp [2])/3
                #print("Val_Color_temp: ",Val_Color_temp)
                Matriz_color[u - 1][v - 1] = Val_Color_temp
                #print(Val_Color_temp)
                if ((Val_Color_temp < EscalaColores[2] - GlobalColorDifThreshold) and (Val_Color_temp > EscalaColores[0] + GlobalColorDifThreshold)):
                    EscalaColores[1] = Val_Color_temp
                    
    #print(Matriz_color)
    #Extraemos el codigo binario
    CodigoBinString = ""
    
    if a == 1:
        pass
    else:
        for  u in range (0, 3):
            for v in range(0,3):
                print("Matriz_color[u][v]: ",Matriz_color[u][v])
                #print("EscalaColores[1] - GlobalColorDifThreshold: ",EscalaColores[1] - GlobalColorDifThreshold)
                #print("EscalaColores[1] + GlobalColorDifThreshold: ", EscalaColores[1] + GlobalColorDifThreshold)
                if ((u == 0) and (v == 0)):
                    CodigoBinString = CodigoBinString
                    #print("Matriz_color[u][v]: ",Matriz_color[u][v])
                    #print("EscalaColores[1] - GlobalColorDifThreshold: ",EscalaColores[1] - GlobalColorDifThreshold)
                    #print("EscalaColores[1] + GlobalColorDifThreshold: ", EscalaColores[1] + GlobalColorDifThreshold)
                elif ((Matriz_color[u][v] > EscalaColores[1].any() - GlobalColorDifThreshold) and (Matriz_color[u][v] < EscalaColores[1].any() + GlobalColorDifThreshold)):
                    CodigoBinString = CodigoBinString + "1"
                else:
                    CodigoBinString = CodigoBinString + "0"

    if a == 1:
        tempID = 0
        pos = [0,0,0]
    else:
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
        print("-------------------")
        print(" ")
        
        cv.imshow("Codigo", Final_Crop_rotated)
        cv.waitKey(0)

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







