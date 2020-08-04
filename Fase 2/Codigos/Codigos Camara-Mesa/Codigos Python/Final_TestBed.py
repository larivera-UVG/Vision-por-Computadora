#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:26:33 2020
@author: Jose Pablo Guerra
Codigo que implementa Calibracion y generacion de codigos para la mesa de pruebas y la deteccion de pose de robots
asi como la identifacion de sus codigos o marcadores.

7/07/2020: Version 0.1.0 -- Se incluye la GUI con el boton de calibrar y generacion de codigos
                            Se agrega el boton de limpiar pantallas generadas por OpenCV.
                            
7/07/2020: Vesion 0.1.1 -- Se agrega un textbox para el numero del generador de codigo, 
                           ademas de corregir su posicion en la GUI.
                           
12/07/2020: Version 0.2.0 -- Se agrega el boton para la toma de pose de datos, ademas de las funciones 
                            para reconocer la posicion de los robots. Fallas aun en la deteccion del codigo.
                            
12/07/2020: Version 0.2.1 -- Pruebas preeliminares de rotacion del codigo correctas. Se realizaran mas pruebas
                            para verificar que funcione. Proximo pasos: mejorar la deteccion del codigo.   
                            
21/07/2020: Version 0.3.0 -- Se arregla la parte del pivote, gira exitosamente siempre para dejar al pivote en la esquina superior izquierda.
                            Se arregla la identificacion de codigo.
                            
                            Para un mejor resultado, iluminar bien los codigos para que pueda detectar el pixel correctamente, sino, puede fallar.
26/07/2020: Version 0.4.0 -- Se arregla la identifcacion de codigo, ahora detecta codigos entre 3x3 y hasta 7x7 (pruebas realizadas)
                             Se agrega en la GUI el boton de toma de pose para unificar los 3 programas en uno solo.
                             
30/07/2020: Version 0.4.1 -- Se agrega un cuadro de texto para el tama;o de los marcadores o codigos, esto con el fin de
                            facilitar al usuario ingresar el tama;o del codigo desde la GUI y no tener que compilar el 
                            programa nuevamente cada vez que se desea cambiar de tama;o.
                            Detecta tama;os desde 3x3 hasta 10x10 (siempre cuidando la ilumacion)
                            Se agrega un if para evitar que otros objetos sean detectados, este if se maneja con las
                            variables gloables MIN_IMAGE_SIZE  y TRESHOLD_IMAGE_SIZE. La primera controla el tama;o 
                            de la imagen (en promedio es una imagen de 115x115) y el segundo controla el treshold
                            de tama;o porque puede variar minimamente.
                            
31/07/2020: Version 0.4.2 -- Arreglos menores a la deteccion de tama;o de imagen, se agrega las siguientes variables:
                            TRESHOLD_DETECT_MIN y TRESHOLD_DETECT_MAX. Por la forma en como se identifican los IDs se 
                            necesita detectar los cuadros grises, según sea la iluminación, este parametro puede variar
                            entre los 70 (o hasta 65) hasta un maximo de 130 (mas o menos). Con estas variables se 
                            controlan esos tresholds para detectar rangos de gris adecuados. 
                            
02/08/2020: Version 0.5.0 -- Se elimina la funcion reescalar por tama;o de codigo o marcador, ahora, reescala 
                            por tama;o de de imagen (lo lleva una imagen de 116x116)
                            Se agregan mas funciones a la GUI, en este caso una funcion de seteo de camara de la clase
                            robot (que hace lo mismo que la clase camara), y abre una nueva ventana para tomar una nueva
                            foto pero se calibra utilizando los parametros ya encontrados. 
                            Esta version esta lista para los multi-hilos.
                            
03/08/2020: Version 0.5.0 -- Se agregan comentarios para enteder el codigo y su funcionamiento, esto no sube el conteo del versionado.

03/08/2020: Version 0.6.0 -- Se eliminan funciones de toma de pose y se agregan a la libreria Swarm_robotic.py

03/08/2020: Version 0.6.1 -- Se agrega el metodo get_code de la clase Robot
"""


from Swarm_robotic import camara, Robot #libreria swarm para la deteccion de la pose de agentes
import cv2 as cv #importando libreria para opencv 

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
NUM_CAM = 0

camara = camara(NUM_CAM) #Inicializa el objeto camara para sus funciones respectivas
robot = Robot(NUM_CAM) #Inicializa el objeto robot para la toma de poses y captura de imagen.

#----------------------------------
#Para la toma de poses de los robots

MyGlobalCannyInf = 185
MyGlobalCannySup = 330


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
        self.TxtBox2()
        self.codigo_button()
        self.Toma_pose()

    def capturar_button(self):
        btn1 = QPushButton("Calibrar", self)
        btn1.move(n,50)
        self.Init_Cam
        btn1.clicked.connect(self.capturar)
    
    def limpiar_button(self):
        btn2 = QPushButton("Limpiar", self)
        btn2.move(n+90,50)
        btn2.clicked.connect(self.limpiar_pantalla)
        
    def codigo_button(self):
        btn3 = QPushButton("Generar Codigo", self)
        btn3.move(n2,90)
        btn3.clicked.connect(self.codigo)
        
    def Toma_pose(self):
        btn4 = QPushButton("Tomar Pose", self)
        btn4.move(n2,140)
        self.Init_pose()
        btn4.clicked.connect(self.pose)
        
    def pose(self):
        text = self.lineEdit2.text()
        if text == '':
            text = '3'
        numCod = int(text)
        snapshot_robot = robot.Capture_frame()
        cv.imshow("CapturaPoseRobot", snapshot_robot)
        #Snapshot = cv.imread("opencv_CalibSnapshot_0.png")
        robot.get_code(snapshot_robot, MyGlobalCannyInf, MyGlobalCannySup, numCod)
    
    def TxtBox(self):
        self.lineEdit = QLineEdit(self,placeholderText="Ingrese número")
        self.lineEdit.setFixedWidth(120)
        self.lineEdit.move(n2+140,93)
        #vbox = QVBoxLayout(self)
        #vbox.addWidget(self.lineEdit)
    
    def TxtBox2(self):
        self.lineEdit2 = QLineEdit(self,placeholderText="Tamaño del código")
        self.lineEdit2.setFixedWidth(125)
        self.lineEdit2.move(n2+120,143)
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
    
    def Init_pose(self):
        robot.initialize(WIDTH, HEIGTH)
        
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