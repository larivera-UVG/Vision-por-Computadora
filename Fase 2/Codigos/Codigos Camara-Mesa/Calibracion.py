#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jose Pablo Guerra 
Programa de calibracion para la camara utilizando OpenCV
 
***********************
Versionado:
***********************
4/07/2020: Creacion inicial del archivo
5/07/2020: Version 0.1.0 -- falta agregar dos funciones mas de la version origninal en c++
Detecta bordes circulares en las esquinas de la mesa y calibra basados en esos puntos.
Version con Programacion Orientada a Objetos. 

7/07/2020: Version 0.2.0 -- Se ajustan algunos metodos, se agrega un init mejorado 
                            y una captura de fotograma mejor para incluirlo en la GUI.
                            Se agrega el metodo de la generacion de codigos.

***********************
Anotaciones iniciales:
***********************
De preferencia utilizar la suite de anaconda, esto permite instalar los paquetes 
de manera mas adecuada y evitar errores entre versionres o que las librerias 
no esten correctamente linkeadas al compilador. 

Que la mesa no tenga objetos sobre ella y que tenga bordes circulares 
de alto contraste para mejores resultados.

Basado en el codigo realizado por Andre Rodas 
"""


#Importando las librerias necesarias
import cv2 as cv #importando libreria para opencv 
import numpy as np #para la creacion de arrays
import math as mt #para el uso de herramientas matematicas como raiz cuadrada


Canny_Factor = 2.5 #factor de multiplicacion para el limite superior de Canny
Calib_param = 40 #Factor de calibracion para Canny, este factor se puede variar
               #para una mejor deteccion de los bordes circulares.
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
    punto1 : Primer punto.
    punto2 : Segundo punto.
    Returns
    -------
    TYPE
        Obtiene dos puntos y calcula su distancia
    """
    distanciax = (punto1[0] - punto2[0])**2
    distanciay = (punto1[1] - punto2[1])**2
    return mt.sqrt(distanciax + distanciay) + 0.5

def mayor2float(X1, X2):
    """
    
    Parameters
    ----------
    X1 : Numero 1.
    X2 : Numero 2
    Returns
    -------
    TYPE
        obtiene el mayor de los numeros
    """
    if (X1 > X2):
        return X1
    else:
        return X2;
    
    
def getWiHe(esquina):
    """
    
    Parameters
    ----------
    esquina : Recibe una coordenada (x,y) de la ubicacion de la esquina (4 esquinas, 4 parejas)
    Returns
    -------
    WiHeMax : El punto mayor entre las diferentes esquinas.
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

def pipe(frame):
    return frame

def get_esquinas(frame, canny_value, pixelTreshold):
    """
    
    Parameters
    ----------
    frame : La foto o frame de la mesa.
    canny_value : El valor de Canny para el metodo.
    pixelTreshold : NO USADO.
    Returns
    -------
    esquinas_final : Retorna un array con las coordenadas finales de cada esquina, basado en el 
                    borde circular.
    """

    esquinas_final = [] #array de las esquinas, ubica los puntos circulares para la calibracion
    img_counter = 0 #contador de imagenes guardadas

    ksize = (3,3) #para el metodo de Canny
    frame_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY) #a blanco y negro para una matriz bidimensional
                                                #es mas facil procesar blanco y negro que color.
    frame_gray = cv.blur(frame_gray, ksize) #difuminado, para quitar detalles extras
    edge = cv.Canny(frame_gray, canny_value, canny_value*Canny_Factor) #Con canny busca los bordes.
        
        #obtiene los contornos de la imagen
    image, contour, hierarchy = cv.findContours(edge, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    #print(contour) #para debug
    height_im, width_im = edge.shape[:2] #obtiene el tama;o maximo de la imagen
    boardMax = ([0,0], [0,height_im], [width_im, 0], [width_im, height_im]) #define el borde maximo de la mesa, esquinas maximas

    #print(len(contour) - 1) #para debug   
    for i in range (0, len(contour)-1):
        #print(i) #para debug
        #rect = cv.minAreaRect(contour[i]) #obtiene el area minima del contorno, no usado
        contour_list = [] #array que guarda los contornos circulares encontrados
        for i in contour:
            approx = cv.approxPolyDP(i,0.01*cv.arcLength(i,True),True) #utiliza el metodo de aproximacion
                            #approxPolyDP para encontrar los contornos circulares.
            area = cv.contourArea(i) #calcula el area de este contorno.
            
            if ((len(approx) > 8) & (area > 3) ): #Treshold aproximado, puede variar si se desea para detectar circulos 
                                                #diferentes tama;os
                contour_list.append(i) #si esta dentro del rango, lo agrega a la lista
                
        #PARA DEBUG:
            
        #cv.drawContours(frame, contour_list,  -1, (255,0,0), 2) #dibuja los contornos
        #print(frame.shape)
        #cv.imshow('Objects Detected',frame) #muestra en la imagen original donde estas los circulos encontrados
        #cv.waitKey(1)
        #cv.circle(img,center,radius,(0,255,0),2)
        #cv.circle(img,center,radius,(0,255,0),2)
        #(x, y), (width, height), angle = rect
        #print("este es el width", width)
        #print("este es el height", height)           
        #print("esta es la diferencia ", (width - height))
        
        Cx = 0 #coordenada en x
        Cy = 0 #coordenada en y
        
        esquinas_final = [[1,1], [1,2], [2,1], [2,2]] #un valor inicial para la comparativa
        a = True
        for c in contour_list: #recorre la lista de contornos para buscar el centro
            # calcula el centro
            M = cv.moments(c)
            
            #ver documentacion para obtener mas informacion de como se calcula la coordenada (x,y)
            Cx = int(M["m10"] / M["m00"])
            Cy = int(M["m01"] / M["m00"])
            
            #esquinas_final[0] = [Cx,Cy] #agrega la primera esquina en la posicion inicial.
            
            if (a):
                esquinas_final[0] = [Cx,Cy]
                a = False
                
            for i in range (0,4):
                if (distancia2puntos(boardMax[i], (Cx,Cy))<distancia2puntos(boardMax[i], esquinas_final[i])):
                    esquinas_final[i] = [Cx,Cy]

                
                """
                Posterior a eso, recorre las 4 esquinas maximas de la imagen y las 4 esquinas iniciales.
                Calcula la distancia entre esos puntos y el centro del borde para ver cual es mas peque;o
                si el centro del borde es mas peque;o, esta mas cerca del borde maximo, por lo tanto es 
                un circulo en la esquina de la mesa. Sino, no lo toca. 
                
                Finalmente crea el array con las esquinas de cada borde circular.
                """
                       
    print("Estas son las esquinas al final: ", esquinas_final) #para debug
    #print("Esquina 1", esquinas_final[1])
    
    #guarda la imagen de Canny solamente como referencia, se puede comentar. 
    edge_img = "opencv_Cannyframe_{}.png".format(img_counter) #Formato del nombre de la imagen.
                                                    #Guarda el numero de frame (foto) que se tomo.
    cv.imwrite(edge_img, edge) #Guarda la foro
    print("{} Canny Guardado!".format(edge_img)) #mensaje de Ok para el save de la foto.
    img_counter += 1 #aumenta el contador. 
    cv.imshow("prueba", edge)
    cv.waitKey(1)
    return esquinas_final 

def getHomogenea(esquina):
    """
    
    Parameters
    ----------
    esquina : array de esquinas.
    Returns
    -------
    M : la matriz de la transformada de la perspectiva
    """
    WH = getWiHe(esquina) #Obtiene el valor del W y el H

    esquinaFloat= np.array([esquina[0],esquina[2],esquina[1] ,esquina[3],], np.float32) #se hace
                    #este arreglo con numpy para que OpenCV reconozca las esquinas como un tipo de dato correcto.
    
    #print(esquinaFloat) #para debug
    esquinasFinales = np.array([[ 0, 0],[float(WH[0]), 0 ],[ 0,float(WH[1])],[float(WH[0]),float(WH[1])],],np.float32)
    
    M = cv.getPerspectiveTransform(esquinaFloat, esquinasFinales) #obtiene la matriz de la perspectiva.
    #lambda = getPerspectiveTransform(esquinaFloat, esquinasFinales);
    return M

    
def saveMat(name, src):
    cv.FileStorage(name,src)

#metodo -> que es capaz de hacer nuestra clase, comportamiento
    
    
class camara():
    """
    Definicion de la clase de camara, incluye los siguientes metodos:
        set_camara(): para setear configuracion inicial de la camara
        tomar_foto(): para capturar el frame.
        Calibrar(): Calibracion de la camara.
    """
    
    def __init__(self,cam_num):
        """
        

        Parameters
        ----------
        cam_num : El numero del dispositivo que se quiere abrir, normalmente es 0.

        Returns
        -------
        None.

        """
        self.cap = cv.VideoCapture(cam_num)
        self.cam_num = cam_num
        
    def initialize(self,WIDTH,HEIGHT):
        """
        

        Parameters
        ----------
        WIDTH : Ancho del frame.
        HEIGHT : Largo del frame.

        Returns
        -------
        None.

        """
        self.cap = cv.VideoCapture(self.cam_num)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        
    def get_frame(self):
        """
        

        Returns
        -------
        Retorna el frame capturado al momento de presionar la tecla ESC.

        """
        while True:
            ret, self.last_frame = self.cap.read()
            cv.imshow("test", self.last_frame) #muestra el video. 
            k = cv.waitKey(1) #k = 1 es para espacio
            if k%256 == 27:
                    # ESC presionado para cerrar
                cv.destroyWindow("test")
                cv.waitKey(1)
                print("Escape presionado, cerrando...")
                break
            
        return self.last_frame
    
    def update_frame(self):
        """
        

        Returns
        -------
        Modelo, de momento no se usa.
        Sirve para actualizar el frame capturado.

        """
        ret, self.last_frame = self.cap.read()
        return self.last_frame
                                 
    def destroy_window(self):
        """
        

        Returns
        -------
        Destruye las ventanas abiertas por OpenCV.

        """
        cv.destroyAllWindows()
        cv.waitKey(1)
        
    def set_camera(self,WIDTH,HEIGHT):
        """
        
        Parameters
        ----------
        WIDTH : Width del frame
        HEIGHT : Height del frame.
        Returns
        -------
        cam : variable de tipo VideoCapture, para ser usado en la toma de foto..
        """
        #cam = cv.VideoCapture(0) #abre la camara web
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        #print("saliendo")
        #cv.namedWindow("test") #crea la ventana
    """
    def tomar_foto(self,cam):
        #
        
        Parameters
        ----------
        cam : Objeto de tipo VideoCapture, configuracion inicial de la camara.
        Returns
        -------
        frame: fotograma tomado con la camara.
        #
        
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

        cam.release()
        cv.destroyAllWindows()            
        return frame #retorna el frame que se va a utilizar  
     """    
    def Calibrar(self,Snapshot,Calib_param, Treshold):
        """
        

        Parameters
        ----------
        Snapshot : Fotografia para la calibracion.
        Calib_param : Parametro de calibracion para Canny.
        Treshold : NO USADO.

        Returns
        -------
        None.

        """
        img_counter = 0
        Esqui = get_esquinas(Snapshot, Calib_param, Treshold)
        Matrix = getHomogenea(Esqui)
        MyWiHe = getWiHe(Esqui)
        CaliSnapshot = cv.warpPerspective(Snapshot, Matrix, (MyWiHe[0],  MyWiHe[1]))
        
        
        edge_img = "opencv_CalibSnapshot_{}.png".format(img_counter) #Formato del nombre de la imagen.
                                                    #Guarda el numero de frame (foto) que se tomo.
        cv.imwrite(edge_img, CaliSnapshot) #Guarda la foro
        print("{} Canny Guardado!".format(edge_img)) #mensaje de Ok para el save de la foto.
        img_counter += 1 #aumenta el contador. 
        #cv.imshow("prueba", edge)
        cv.imshow("Output Image", CaliSnapshot)
        cv.waitKey(1)
        
    def Generar_codigo(self,val):
        img_counter = 0
        """
        

        Parameters
        ----------
        val : Un valor entre 0 y 255 para generar los codigos de deteccion de los robots.

        Returns
        -------
        Cod : El codigo luego de la construccion de la matriz.

        """
        
        #Si el valor no esta en el rango, retorna una matriz vacia
        if val < 0 or val > 255:
            print("Ingrese un numero valido entre 0 y 255")
            Cod = np.zeros([200,200], dtype = np.uint8)
            return Cod #matriz de 0 para evitar errores.
        
        num = '{0:08b}'.format(val) #toma el valor y lo convierte en un string binario
                                #el formato es '0bxxx' por lo que se elimina el '0b' 
                                #y se garantiza que siempre sean 8 bits.
    #print(num)
        k = -1 #parametro de control
        
        Cod = np.zeros([200,200], dtype = np.uint8) #crea un array de zeros que sera la 
                            #matriz donde se genera el codigo. Debe ser de tipo int de 8 bits
                            #para que pueda reconocer los tonos de grises
    #print(Cod)
        for u in range (0,3):
            for v in range (0,3):
                
                #para generar el pivote (ver la tesis de Andre)
                #El pivote sirve para saber que cuadro debe estar alineado.
                if k == -1:
                    for i in range(u*50+25, u*50+75):
                        for i2 in range(v*50+25,v*50+75):
                            Cod[i,i2] = 255 #llena el pivote, 255 = blanco
                else:
                    #genera los otros cuadros en escala de grises, 125 = gris
                    t = num[7-k]
                    n = int(t)
                    for i3 in range(u*50+25, u*50+75):
                        for i4 in range(v*50+25,v*50+75):
                            Cod[i3,i4] = n * 125
                k = k + 1
                cv.imshow('cod', Cod)
                cv.waitKey(1)
                edge_img = "opencv_CodGenerator_{}.png".format(img_counter) #Formato del nombre de la imagen.
                                                    #Guarda el numero de frame (foto) que se tomo.
                cv.imwrite(edge_img, Cod) #Guarda la foro
                print("{} Canny Guardado!".format(edge_img)) #mensaje de Ok para el save de la foto.
                img_counter += 1 #aumenta el contador. 
        return Cod #retorna la matriz que luego puede ser mostrada como una foto del codigo.
        