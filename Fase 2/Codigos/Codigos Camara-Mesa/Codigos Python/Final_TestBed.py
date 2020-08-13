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

09/08/2020: Version 0.7.0 -- Cambio en los metodos de calibracion y en la deteccion de pose por las modificaciones 
                             realizadas a la clase ***camara** y la clase ***vector_robot*** de la libreria
                             Swarm_robotic.py
                             
09/08/2020: Version 0.8.0 -- Cambio en la tome de pose, se importan las funciones (ya no forma parte de la clase ***vector_robot***)
                             con el objetivo de usarlo en multi-hilos (aunque a esta version funciona normal, sin hilos).

10/08/2020: Version 0.9.0 -- Se agregan funciones multi-hilos utilizando las libreria threading (se probo con 
                             multiprocessing pero por problemas del uso de GLI (consultar) no funciona algunas 
                             funciones de OpenCV).
                             hasta el momento se procesa la imagen, se obtiene el codigo y se actualiza el vector
                             en 3 hilos diferentes con captura manual del usuario. Se planea agregar la funcion de
                             captura continua como un 4 hilo. 
        
12/08/2020: Version 0.10.0 -- Se agregan ciertas ventanas en el hilo principal que muestra las imagenes para debug.
                              Esto depende del modo que se escoja en la funcion. Finalmente, se arreglan ciertos 
                              delay en los hilos para acelerar el procesamiento pero evitar colisiones y ayudar
                              a la sincronizacion.

"""


from Swarm_robotic import camara, vector_robot, Robot #libreria swarm para la deteccion de la pose de agentes
from toma_pose import getRobot_fromSnapshot, process_image
import cv2 as cv #importando libreria para opencv 
import threading
import time
#import numpy as np
#from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox,QVBoxLayout, QTextEdit,QLineEdit,QInputDialog
import sys
#from PySide2.QtGui import QIcon
#from multiprocessing import Process, Lock, Queue
#q = Queue()

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
#robot = Robot(NUM_CAM) #Inicializa el objeto robot para la toma de poses y captura de imagen.
vector_robot = vector_robot()
#----------------------------------
#Para la toma de poses de los robots

MyGlobalCannyInf = 185
MyGlobalCannySup = 330

snapshot_robot = []
RecCod = []
gray_blur_img = []
canny_img = []
parameters = []
activate = 0
a = 0
Final_Crop_rotated = []
resized = []

#MyWiHe = []
# In[Definiendo hilos]:

#read_lock = Lock()
lock = threading.Lock()
    
def worker(q, n):
    q.put(n)
    pass

def image_processing():
    global gray_blur_img, RecCod, canny_img, snapshot_robot
    print("Soy el hilo de procesamiento")
    while(1):
        lock.acquire()
        print("Estoy procesando...")
        #read_lock.acquire()
        """
        while not q.empty():
            snapshot_robot = q.get()
            
        if q.empty():
            pass
        else:
        """
        a = 1
        print(a)
        print("El procesamiento va a empezar")
        """
        #voy a procesar
        blur_size = (3,3) #para la difuminacion, leer documentacion
        #height_im, width_im = calib_snapshot.shape[:2] #obtiene los tama;os de la imagen capturada
        #print(height_im, width_im)
        #PixCodeSize = Medida_cod * width_im / anchoMesa
        print("voy a prrocesar la imagen")
        print("Aplicare filtro de grises")
        gray_img = cv.cvtColor(snapshot_robot, cv.COLOR_BGR2GRAY) #se le aplica filtro de grises
        #print(gray_img)
        print("Aplicare blur")
        gray_blur_img = cv.blur(gray_img, blur_size) #difuminacion para elimiar detalles innecesarios
        print("Obtendre canny")
        canny_img = cv.Canny(gray_blur_img, MyGlobalCannyInf, MyGlobalCannySup, apertureSize = 3) #a esto se le aplica Canny para la deteccion de bordes
        print("Termine de procesar")
        image, RecCod, hierarchy = cv.findContours(canny_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        print("Tengo los contornos")
        """
        RecCod, gray_blur_img, canny_img = process_image(snapshot_robot, MyGlobalCannyInf, MyGlobalCannySup)
        #q.put(contour)
        #q.put(gray_blur_img)
        lock.release()
        print("Libere")
        time.sleep(3)

def getting_robot_code(numCod, MyWiHe):
    global RecCod, gray_blur_img, parameters, activate, resized, Final_Crop_rotated
    #print(RecCod)
    print("Soy el hilo de obtener pose")
    while(1):
        lock.acquire()
        activate = 1
        print("adquiri el recurso")
        """
        n = 0
        while not q.empty():
            if n == 0:
                RecCod = q.get()
                n+=1
            if n == 1:
                gray_blur_img = q.get()
                n+=1
        """
                
        #RecCod = q.get()
        #gray_blur_img = q.get()
        a = 2
        print(a)
        #print(n)
        #if n == 2:
        print("La obtencion de pose va empezar")
        #cv.imshow("CapturaPoseRobot", snapshot_robot)
        #cv.waitKey(0)
        parameters,resized,Final_Crop_rotated, _ = getRobot_fromSnapshot(RecCod, gray_blur_img,MyWiHe,numCod,"DEBUG_ON_CAPTURE")
        #break
        #read_lock.release()

        lock.release()
        time.sleep(2)
        
def actualizar_robots():
    global parameters, activate
    
    lock.acquire()
    
    size = len(parameters)
    print("El tama;o de los parametros: ", size)
    for i in range (0, size):
        temp_param = parameters[i]
        vector = vector_robot.agregar_robot(Robot(temp_param[0],temp_param[1],temp_param[2]))
        #print(np.shape(vector))
    size_vector = len(vector)
    print("Este es el tama;o del vector antes de entrar: ",size_vector)
    for v in range (0, size_vector):
        print("Este es el vector retornado: ",vector[v].id_robot)
    lock.release()
    time.sleep(5)
    if activate == 1:
        n = 0
        print("la bandera de activacion me hizo entrar")
        while(1):
            n+=1
            if n > 0:
                lock.acquire()
            size = len(parameters)
            #print("El tama;o de los parametros: ", size)
            for i in range (0, size):
                temp_param = parameters[i]
                if vector_robot.update_robot_byID(temp_param[0], temp_param[1], temp_param[2]):
                    pass
                else:
                    vector = vector_robot.agregar_robot(Robot(temp_param[0],temp_param[1],temp_param[2]))
                 
                """
                size_vector = len(vector)
                for v in range (0, size_vector):
                    if temp_param[0] == vector[v].id_robot:
                        pass
                    else:
                        vector = vector_robot.agregar_robot(Robot(temp_param[0],temp_param[1],temp_param[2]))
                """
            size_vector = len(vector)
            print("Este es el tama;o del vector en el while: ",size_vector)
            for v in range (0, size_vector):
                print("Este es el vector retornado: ",vector[v].id_robot)
                print("Este es el vector retornado: ",vector[v].get_pos())
            lock.release()
            time.sleep(1)
            


def capturar_foto():
    pass





#escribiendo.join()

# In[Definiendo la interfaz grafica]
"""
Definiendo a la interfaz grafica. 
"""

class Window(QWidget):
    #global q
    #new_thread = 0
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
        self.new_thread = 0
        self.Toma_pose()

    def capturar_button(self):
        btn1 = QPushButton("Calibrar", self)
        btn1.move(n,50)
        #self.Init_Cam
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
        #self.Init_pose()
        btn4.clicked.connect(self.pose)
        
    def pose(self):
        global gray_blur_img, canny_img, snapshot_robot, resized, Final_Crop_rotated
        text = self.lineEdit2.text()
        if text == '':
            text = '3'
        numCod = int(text)
        #read_lock.acquire()
        foto = camara.get_frame()
        snapshot_robot,MyWiHe = vector_robot.calibrar_imagen(foto)
        #q.put(snapshot_robot)
        #read_lock.release()
        cv.imshow("CapturaPoseRobot", snapshot_robot)
        cv.waitKey(0)
        time.sleep(1)
        if self.new_thread == 0:
            #capturar = threading.Thread(target = capturar_foto, args=(numCod,)) #asignacion de los hilos a una variable
            procesar = threading.Thread(target = image_processing) #asignacion de los hilos a una variable
            obtener_pose = threading.Thread(target = getting_robot_code, args=(numCod,MyWiHe,))
            vector_update = threading.Thread(target = actualizar_robots)
            procesar.start() #inicializa el hilo.
            time.sleep(1)
            obtener_pose.start() #inicializa el hilo.
            time.sleep(1)
            vector_update.start()
            self.new_thread = 1
        if resized == [] or Final_Crop_rotated ==[]:
            pass
        else:
            #gray_blur_img
            cv.imshow("gray_blur_img",gray_blur_img)
            cv.imshow("resized",resized)
            cv.imshow("Final_Crop_rotated", Final_Crop_rotated)
            cv.imshow("canny_img",canny_img)
            cv.waitKey(0)
        #cv.waitKey(100)
        #cv.imshow("canny_img", canny_img)
        #cv.waitKey(0)
        #cv.imshow("Imagen blur", gray_blur_img)
        #cv.waitKey(0)
        
        #procesar.join()
        #obtener_pose.join()
        #actualizar = threading.Thread(target = read_2)
        
        """
        #Snapshot = cv.imread("opencv_CalibSnapshot_0.png")
        RecCod, gray_blur_img, canny_img = getRobot_Code(snapshot_robot, MyGlobalCannyInf, MyGlobalCannySup, numCod)
        parameters = getRobot_fromSnapshot(RecCod,gray_blur_img,numCod)
        
        size = len(parameters)
        for i in range (0, size):
            temp_param = parameters[i]
            vector = vector_robot.agregar_robot(Robot(temp_param[0],temp_param[1],temp_param[2]))
        print("Este es el vector retornado: ",vector[0].id_robot)
        print("Este es el vector retornado: ",vector[1].id_robot)
        """
    
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