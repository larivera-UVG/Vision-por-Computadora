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
                            
12/07/2020: Version 0.3.0 -- Se agrega la clase de los robots para la deteccion de sus poses y codigos.

26/07/2020: Version 0.3.1 -- Se elimina unas lineas innecesarias. 
                             Se modifica el metodo get_robot_id de la clase vector_robot
                             
30/07/2020: Version 0.3.2 -- Ajustes menores al codigo para guardar la imagen del marcador generado.

31/07/2020: Version 0.3.3 -- Ajustes menores al codigo, se eliminan unos prints de debug

02/08/2020: Version 0.4.0 -- Se agreaga un nuevo __init__ a la clase de Robot, esto con el fin de tener una funcion
                             de capturar foto. La clase camara calibra, pero ahora, la clase robot tiene su propio 
                             metodo de captura de imagen que se recalibra con los parametros encontrados (mientras
                             las condiciones de luz sean las mismas) 
                             
03/08/2020: Version 0.5.0 -- Se agregan dos funciones para la toma de pose que estaban en el programa de la GUI
                             esto unifica todas las funciones en este archivo, lo cual permite solamente agregar
                             un par de funciones y no se requiere interdepencia de varios archivos. 
                             
03/08/2020: Version 0.6.0 -- Se agrega el metodo get_code de a la clase Robot para unificar las funciones. 

04/08/2020: Version 0.7.0 -- Se hacen modificaciones a la clase de Robot y vector_robot. El objetivo principal de este
                             cambio es poder pasar objetos y crear un vector de objetos de tipo Robot para poder
                             acceder a sus atributos respectivos luego de eso. 

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
Matrix = []
MyWiHe = []

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
    #for i in range (0, len(contour)-1):
        #print(i) #para debug
        #rect = cv.minAreaRect(contour[i]) #obtiene el area minima del contorno, no usado
    contour_list = [] #array que guarda los contornos circulares encontrados
    for con in contour:
        approx = cv.approxPolyDP(con,0.01*cv.arcLength(con,True),True) #utiliza el metodo de aproximacion
                            #approxPolyDP para encontrar los contornos circulares.
        area = cv.contourArea(con) #calcula el area de este contorno.
            
        if ((len(approx) > 8) & (area > 3) ): #Treshold aproximado, puede variar si se desea para detectar circulos 
                                                #diferentes tama;os
            contour_list.append(con) #si esta dentro del rango, lo agrega a la lista
                
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
        #self.cap = cv.VideoCapture(self.cam_num)
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
        global MyWiHe
        global Matrix
        img_counter = 0
        Esqui = get_esquinas(Snapshot, Calib_param, Treshold)
        Matrix = getHomogenea(Esqui)
        MyWiHe = getWiHe(Esqui)
        CaliSnapshot = cv.warpPerspective(Snapshot, Matrix, (MyWiHe[0],  MyWiHe[1]))
        
        #Robot.Get_NewFrame(self,self.Matrix, self.MyWiHe)
        
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
        
class Robot():

    """
    """
    id_robot = 0
    ip = 0
    pos = [0,0,0]
    vel_left = 0
    vel_right = 0
    
    def __init__ (self,_id, _ip, _pos):
        self.id_robot = _id
        self.ip = _ip
        self.pos = _pos
        self.vel_left = 0
        self.vel_right = 0
    """    
    def __init__(self, _id, _ip, _pos):
        self.id_robot = _id
        self.ip = _ip
        self.x = _pos[0]
        self.y = _pos[1]
        self.theta = _pos[2]
        self.vel_left = 0
        self.vel_right = self.vel_left
    """
        
        
    def Get_NewFrame(self,Mat, WiHe):
        self.NewMat = Mat
        self.MyWiHe_new = WiHe
        print("NewMat", self.NewMat)
        print("MyWiHe_new", self.MyWiHe_new)
     
    """
    def set_robot(self, _id, _ip, _pos):
        
        

        Parameters
        ----------
        _id : TYPE
            DESCRIPTION.
        _ip : TYPE
            DESCRIPTION.
        _pos : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        
        Robot.id_robot = _id
        Robot.ip = _ip
        self.x = _pos[0]
        self.y = _pos[1]
        self.theta = _pos[2]
        self.vel_left = 0
        Robot.vel_right = Robit.vel_left
        self.robot = [self.id_robot,self.ip,self.x,self.y,self.theta,self.vel_right,self.vel_left]
        return self.robot
    """    
    
    def set_IP(self,_ip):
        """
        

        Parameters
        ----------
        ip : TYPE
            DESCRIPTION.

        Returns
        -------
        ip : TYPE
            DESCRIPTION.

        """
        self.ip = _ip
        return Robot.ip
    
    def set_pos(self, _pos):
        """
        

        Parameters
        ----------
        pos : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.pos[0] = _pos[0]
        self.pos[1] = _pos[1]
        self.pos[2] = _pos[2]
        
    def get_pos(self):
        """
        

        Returns
        -------
        Pos : TYPE
            DESCRIPTION.

        """
        """
        Pos = []
        Pos.append(self.x)
        Pos.append(self.y)
        Pos.append(self.theta)
        """
        return self.pos
        
    def get_IP (self):
        """
        

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self.ip
    
    def set_speed(self, vel):
        """
        

        Parameters
        ----------
        vel : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.vel_right = vel[0]
        self.vel_left = vel[1]
        
    def get_speed(self):
        """
        

        Returns
        -------
        speed : TYPE
            DESCRIPTION.

        """
        speed = []
        speed.append(self.vel_right)
        speed.append(self.vel_left)
        return speed
    
#_robot = Robot()
    
class vector_robot():
    """
    """
    Robot_vector = []
    #robot_vector_u = Robot()
    def __init__(self):
        self.Robot_vector = []
        
    def init_cam_robot(self, cam_num):
        self.cap = cv.VideoCapture(cam_num)
        
    def get_code(self,snapshot_robot, MyGlobalCannyInf, MyGlobalCannySup, numCod):
        return getRobot_Code(snapshot_robot, MyGlobalCannyInf, MyGlobalCannySup, numCod)
        
    def Capture_frame(self):
        """
        

        Returns
        -------
        Retorna el frame capturado al momento de presionar la tecla ESC.

        """
        global MyWiHe
        global Matrix
        while True:
            ret, self.last_frame_robot = self.cap.read()
            cv.imshow("Captura de pose", self.last_frame_robot) #muestra el video. 
            k = cv.waitKey(1) #k = 1 es para espacio
            if k%256 == 27:
                    # ESC presionado para cerrar
                cv.destroyWindow("Captura de pose")
                cv.waitKey(1)
                print("Escape presionado, cerrando...")
                break
        #print("NewMat", self.NewMat)
        #print("MyWiHe_new", self.MyWiHe_new)
        #MyWiHe = self.MyWiHe_new
        self.last_frame_robot = cv.warpPerspective(self.last_frame_robot, Matrix, (MyWiHe[0],  MyWiHe[1]))
        return self.last_frame_robot
        
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
        #self.cap = cv.VideoCapture(self.cam_num)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        
    
    def agregar_robot(self,Robot):
        """
        

        Parameters
        ----------
        vector_robot : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        #self.class_robot = class_robot
        #class_robot.id_robot = self
        #global _Robot

        self.Robot_vector.append(Robot)
        print("vector en la posicion 0")
        print(self.Robot_vector[0])
        print("prueba de acceso a los atributos.")
        print(self.Robot_vector[0].id_robot)
        print("vamos a cambiar un atributo, la velocidad quiza")
        print(self.Robot_vector[0].set_speed([1,1]))
        print("vamos a ver la velocidad")
        print(self.Robot_vector[0].get_speed())
        return self.Robot_vector
    
    def search_id_robot(self, _id):
        """
        

        Parameters
        ----------
        _id : TYPE
            DESCRIPTION.

        Returns
        -------
        final_ID : TYPE
            DESCRIPTION.

        """
        final_ID = -1
        for i in range (0, len(self.Robot_vector)):
            temp_Robot = self.Robot_vector[i]
            if (temp_Robot[0] == _id):
                final_ID = i 
                break
        return final_ID
    
    def get_robot_id(self, _id):
        """
        

        Parameters
        ----------
        _id : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        size_robot = len(self.Robot_vector)
        #print(size_robot)
        #print("Este es mi id", _id)
        #print("Soy un robot en esta poiscion: ",self.Robot_vector[2][0])
        a = ''
        for i in range (0,size_robot):
            #print("entre al for")
            temp_ID = self.Robot_vector[i][0]
            #print("Este es el ID que buscas: ", self.Robot_vector[i][0])
            if _id == temp_ID:
                return self.Robot_vector[i]
            else: 
                a = ''
        return a
        #if _id == 0:
        #    return print("No hay robot")
        #else:
        #    return self.Robot_vector[_id]
        
#-------------------------------------------------------
#Para la generacion de los codigos y la tome de poses
#robot = Robot(0) #Inicializa el objeto robot para la toma de poses y captura de imagen.


#from Robot import vector_robot, Robot

#de momento no se usan
SQRTDE2 = 1.41421356
MyPI = 3.14159265

#revisar si es que se usan
anchoMesa = 14.5
largoMesa = 28.0

#de momento no se usan
#GlobalCodePixThreshold = 80
#GlobalColorDifThreshold = 10

#si se usan
MyGlobalCannyInf = 185
MyGlobalCannySup = 330
#Code_size = 1.0 #no se usa

#si se usan
MAX_IMAGE_SIZE = 75

#Para detectar los cuadros grises, normalmente con buena iluminacion pueden llegar a tener un valor de 130 (o mas)
#pero para condiciones de poca luz, el valor MIN puede variar. 
TRESHOLD_DETECT_MIN = 65
TRESHOLD_DETECT_MAX = 130


"""
Definiendo las funciones para la toma de poses. 
"""

def getRobot_Code(calib_snapshot, Canny_inf, Canny_sup, Medida_cod):
    """
    

    Parameters
    ----------
    calib_snapshot : TYPE
        DESCRIPTION.
    Canny_inf : TYPE
        DESCRIPTION.
    Canny_sup : TYPE
        DESCRIPTION.
    Medida_cod : TYPE
        DESCRIPTION.

    Returns
    -------
    vector : TYPE
        DESCRIPTION.

    """
    vector = vector_robot() #inicializa el objeto vector_robot para agregar los diferentes parametros de cada robot como vector
    blur_size = (3,3) #para la difuminacion, leer documentacion
    height_im, width_im = calib_snapshot.shape[:2] #obtiene los tama;os de la imagen capturada
    
    #PixCodeSize = Medida_cod * width_im / anchoMesa
    
    gray_img = cv.cvtColor(calib_snapshot, cv.COLOR_BGR2GRAY) #se le aplica filtro de grises
    gray_blur_img = cv.blur(gray_img, blur_size) #difuminacion para elimiar detalles innecesarios
    canny_img = cv.Canny(gray_blur_img, Canny_inf, Canny_sup, apertureSize = 3) #a esto se le aplica Canny para la deteccion de bordes

    
    #para debug
    #muestra la imagen de canny para ver que contornos va a detectar.
    cv.imshow("Canny", canny_img)
    cv.waitKey(0)
    
    #obtiene los contornos de la imagen de Canny
    image, contour, hierarchy = cv.findContours(canny_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    #para debug
    #dibuja los contornos detectados, descomentar estas lineas:
        
    #cv.drawContours(calib_snapshot, contour,  -1, (255,0,0), 2) #dibuja los contornos
    #cv.imshow("Contornos", calib_snapshot)
    #cv.waitKey(0)

    for c in contour:

        #para debug, imprimi separadores de lo que se va realizando.
        
        print(" ")
        print("-----------------")
        #print("Este es el contador",a)
        RecCod = cv.minAreaRect(c)
        #cv.drawContours(calib_snapshot, c,  -1, (10*i + 100,15*i,20*i + 20), 2) #dibuja los contornos
        #cv.waitKey(0)
        #Rx, Ry = RecCod[0] #SingleRecCod.center
        #print("Contornos", RecCod[0])
        #print("Contornos", RecCod[0][0])
        
        center, size, theta = RecCod #SingleRecCod.size, del codigo de C++, obtiene el angulo, centro y tama;o del contorno
        center, size = tuple(map(int, center)), tuple(map(int, size)) #lo vuelve un int.
        
        #para debug, imprimi el valor del centro.
        #print(center)

        
        #separador
        print("-----------------")
        print(" ")
        

        """
        A continuacion se detalla el procedimiento:
            Se obtiene un factor de escala entre la medida real del marcador o identificador y el tama;o estandar
            con el cual se hizo este codigo, es decir, 3. Este rescale_factor sirve para evitar que contornos muy peque;os
            pasen, aunque igual, mas adelante, hay otro filtro que elimina eso. 
        """
        rescale_factor_size = Medida_cod/3 #factor de escala
        
        #para debug, imprime el tama;o del contorno, se puede descomentar
        print("Size[0] y size[1]: ", size[0], size[1])

        #Compara si ambos tama;os estan por arriba del minimo para no tener imagenes o contornos muy peque;os
        #y nada relevantes para este programa.
        if (size[0] > (40 * rescale_factor_size) and size[1] > (40*rescale_factor_size)): #):
            #cv.drawContours(calib_snapshot, c,  -1, (10,200,20), 2) #dibuja los contornos
            #cv.waitKey(0)
           new_vector_robot =  vector.agregar_robot(getRobot_fromSnapshot(RecCod, gray_blur_img, Medida_cod))
            
    print("Este es el vector que se agrego")
    print(new_vector_robot[0].id_robot)
    #print(vector.Robot.id_robot)
    #para debug, imprime el ID del robot que se identifico y lo  busca en la base de vector_robot()
    #print("Yo soy el robot con 40 y tengo los siguientes atributos: ", vector.get_robot_id(40))
    #print("Yo soy el robot con 30 y tengo los siguientes atributos: ", vector.get_robot_id(30))
    #print("Yo soy el robot con 50 y tengo los siguientes atributos: ", vector.get_robot_id(50))
    return new_vector_robot

def getRobot_fromSnapshot(RecContorno, snap, codeSize):
    """
    

    Parameters
    ----------
    RecContorno : TYPE
        DESCRIPTION.
    snap : TYPE
        DESCRIPTION.
    codeSize : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    # Obtiene el centro, el tama;o y el angulo del contorno.
    center, size, theta = RecContorno

    # Angle correction, no usado, no crea ninguna diferencia en este codigo
    #if theta < -45:
     #   theta += 90

    # Convert to int 
    center, size = tuple(map(int, center)), tuple(map(int, size))
    #print("Este es el nuevo centro", center)

    #obtiene las medidas del contorno o recorte
    GlobalWidth = snap.shape[1]
    GlobalHeigth = snap.shape[0]
    
    #---------------------------------------------
    #separador
    print(" ")
    print("-----------------")
    print("Ingresando a getRobot_fromSnapshot")

    
    #Para obtener el snap recortado.
    height_cont,width_cont = RecContorno[1] #height_cont
    
    #verificar si es usado --------
    """
    """
    tempWiMitad = SQRTDE2 * size[1] / 2
    tempHeMitad = SQRTDE2 * size[0] / 2
    
    
    Cx = center[0] #pasa los centros a variables para su identificacion, centro en X
    Cy = center[1] #Centro en Y


    EscalaColores = []
    
    rows = [int(Cy - tempHeMitad), int(Cy + tempHeMitad)]
    cols = [int(Cx - tempWiMitad), int(Cx + tempWiMitad)]
    #rows_1 = np.array([int(Cy - tempHeMitad), int(Cy + tempHeMitad)])
    #cols_1 = np.array([int(Cx - tempWiMitad), int(Cx + tempWiMitad)])


    #print(RecContorno)
    
    SemiCropCod = snap[rows[0]:rows[1], cols[0]:cols[1]] #hasta aqui todo bien al 19 de julio del 2020, variable no usada

    #Obtener matriz de rotacion de la imagen
    M = cv.getRotationMatrix2D(center, theta, 1)
    
    #se obtiene la perspectiva de la imagen basada en la matriz y las dimensiones de la imagen, esto es para recortar
    dst = cv.warpAffine(snap, M, (GlobalWidth, GlobalHeigth)) 
    #image_rotated = cv.warpAffine(SemiCropCod, temp_matRotated, (SemiCropCod_Heigth, SemiCropCod_Width), flags = cv.INTER_CUBIC)
    
    #Final_Crop_rotated = cv.getRectSubPix(image_rotated, (int(height_cont),int(width_cont)), (np.size(rows_1)/2.0, np.size(cols_1)/2.0))
    
    
    Final_Crop_rotated = cv.getRectSubPix(dst, size, center) #obtiene el recorte final.
    
    
    #cv.imshow("Init", SemiCropCod) 
    
    #para debug, muestra la imagen recortada y rotada
    cv.imshow("Rotated", dst) 
    cv.imshow("Final_crop",Final_Crop_rotated)
    #cv.waitKey(0)
    
    #obtiene las nuevas dimensiones del recorte, esto servira para otro filtro y para el resize de las imagenes
    height_Final_Rotated, width_Final_Rotated = Final_Crop_rotated.shape[:2]
    
    #para debug, imprime las dimensiones actuales de la imagen
    print("Dimensiones actuales: ")
    print(height_Final_Rotated, width_Final_Rotated)
    
    
    scale_percent = (codeSize/3.0)  # percent of original size, factor de reescala que se utiliza basado en el codigo
    #la variable MIN_IMAGE_SIZE es para que las imagenes mas peque;as que hayan pasado el primer filtro, no se tomen en cuenta
    #aqui lo que se se busca eliminar son imagenes o cuadros (normalmente los blancos en cada identificador)
    #sean eliminados para evitar confusiones de identificacion
    
    if (height_Final_Rotated < (MAX_IMAGE_SIZE * scale_percent) or width_Final_Rotated < (MAX_IMAGE_SIZE * scale_percent)):
        #para debug
        print("cumpli el if")
        ctrl = 0 #si la imagen es mas peque;a, entonces se lo salta
    else:
        ctrl = 1 #sino, entra a hacer todo el procesamiento de la imagen para la identificacion del ID.
        
    if ctrl == 1:
    
        
        """
        Este codigo esta pensado para funcionar reconociendo imagenes entre 114 x 114 hasta 120 x 120,
        se define como medida 116x166.
        El objetivo de esto es llevar los codigos a estas medidas en caso de ser necesario (si son de 3x3 puede que no)
        Por lo tanto, se calcula un porcentaje diferente tanto para el width como para el heigth de la imagen.
        """
        
        #calculo del porcentaje de escala para las medidas
        height_percent = (116/height_Final_Rotated) 
        width_percent = (116/height_Final_Rotated)
        
        #para debug, separador e imprime el factor de escala de la imagen.
        print("-----------------")
        print("% de escala", scale_percent)
        
        #para debug, muestra una de las medidas temporales de la imagen.
        print("Medida temporal: ", width_Final_Rotated * scale_percent)
        print("-----------------")
        
        #calcula las nuevas medidas
        width = int(width_Final_Rotated * width_percent)
        height = int(height_Final_Rotated* height_percent)
        
        #para debug, imprime como tupla las nuevas medidas.
        dim = (width, height)
        
        print("Dimensiones resized: ")
        print("-----------------")
        print(dim)
        
        # resize image
        resized = cv.resize(Final_Crop_rotated, dim, interpolation = cv.INTER_AREA)
        
        #para debug muestra la imagen recortada
        cv.imshow("Final_crop_resized",resized)
            
        #obtiene las nuevas medidas para los calculos 
        height_Final_Rotated, width_Final_Rotated = resized.shape[:2]
        
        
        #ppara debug, muestra las medidas, separador.
        print("height_Final_Rotated: ", height_Final_Rotated)
        print("width_Final_Rotated: ", width_Final_Rotated)
        print("-----------------")
    
        

        a = 0 #variable bandera, ya no se usa pero evita modificaciones sustanciales al codigo en cuanto a funcion e ifs
        
    
        
        if a == 0:
            
            """
            La mayoria de imshow() son para debug y mostrar las porciones recortadas.
            Lo que se hace aqui es buscar e identificar los cuadros dentro de cada identificador o codigo.
            Las medidas estan pensadas para imagenes con las medidas mencionadas, por eso se hace el resize.
            
            Estas lineas no se deben modificar a salvo este fallando la identifacion de los cuadros o se dese otro 
            tipo de identificacion. 
            
            Basicamente, por las caracteristicas del codigo/identificador utilizado, se tiene la siguiente figura:
                
            |-----------------------
            |   P  |    1  |   2   |
            |   -  |   -   |   -   |
            |   3  |   4   |   5   |
            |   -  |   -   |   -   |
            |   6  |   7   |   8   | 
            |------------------------
            
            Donde P representa al pivote y cuadro blanco y los numeros del 1 al 8 son los bits a0 hasta a7 para un 
            codigo de hasta 255.
            
            Este codigo identifica el pivote, y lo alinea siempre en la esquina superior izquierda (por eso se le
            aplica un filtro de blanco y negro para que los valores de igual forma queden entre 0 y 255).
            Luego, dependiendo donde este el pivote se rota hasta alinearlo. La rotacion inicial solo lo coloca con angulo 0.
            Finalmente, se ubican los diferentes cuadros y asi es como se identifica el codigo: 1 para gris, 0 para negro
            dependiendo los tresholds establecidos. 
            """
            #print(height_Final_Rotated)
            temp_ColorSupIzq = resized[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:40]
            temp_ColorInfIzq = resized[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)]
            temp_ColorSupDer = resized[int(height_Final_Rotated*1/8):40, 65:100]
            temp_ColorInfDer = resized[62:90, 70:90]
            
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
            cv.imshow("ColorSupIzq_1",resized[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:35])
            #cv.imshow("Pivote",Final_Crop_rotated[int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8) + 80, 35:110])
                
            #ColorSupDer = sum(sum(Final_Crop_rotated[15:45, 70:105]))
                #ColorSupDer = (ColorSupDer1[0] + ColorSupDer1[1] + ColorSupDer1[2])/3
            #print("Superior derecho")
            #print(ColorSupDer)
            #print(" ") 
            cv.imshow("supderecho",resized[int(height_Final_Rotated*1/8):40, 65:100])
                
            #ColorInfDer = sum(sum(Final_Crop_rotated[62:90, 70:90]))
                #ColorInfDer = (ColorInfDer1[0] + ColorInfDer1[1] + ColorInfDer1[2])/3
            #print("inferior derecho")
            #print(ColorInfDer)
            #print(" ") 
            
            cv.imshow("ColorInfDer1",resized[62:90, 70:90])
                
            #print("int(height_Final_Rotated*1/4 + 2))",int(height_Final_Rotated*1/4 + 2))
            #ColorInfIzq = sum(sum(Final_Crop_rotated[int(height_Final_Rotated*1/4 + 50):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 25)]))
                #ColorInfIzq = (ColorInfIzq1[0] + ColorInfIzq1[1] + ColorInfIzq1[2])/3
            #print("inferior izquierdo")
            #print(ColorInfIzq)
            #print(" ") 
            cv.imshow("ColorInfIzq1",resized[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)])
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
           
        tempFloatTheta = theta #el angulo al que esta rotado el codigo. 
        

        #comparacion mencionada, detecta cual de las esquinas tiene el mayor color para hacer la rotacion.
        if ((ColorSupDer > ColorSupIzq) and (ColorSupDer > ColorInfDer) and (ColorSupDer > ColorInfIzq)):
            print("90 en contra del reloj")
            print(" ")
            resized = cv.rotate(resized, cv.ROTATE_90_COUNTERCLOCKWISE)
            tempFloatTheta = tempFloatTheta + 90
            EscalaColores[2] = ColorSupDer
        elif ((ColorInfDer > ColorSupIzq) and (ColorInfDer > ColorSupDer) and (ColorInfDer > ColorInfIzq)):
            print("rotado 180")
            print(" ")
            resized = cv.rotate(resized,cv.ROTATE_180);
            tempFloatTheta = tempFloatTheta + 180;
            EscalaColores[2] = ColorInfDer
                
        elif ((ColorInfIzq > ColorSupIzq) and (ColorInfIzq > ColorInfDer) and (ColorInfIzq > ColorSupDer)):
            print("90 a favor del reloj")
            print(" ")
            resized = cv.rotate(resized, cv.ROTATE_90_CLOCKWISE)
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
        
        
        #a partir de aqui, se localizan los otros 8 cuadros dentro de la imagen y se calcula su valor. 
        
        #temp_ColorSupIzq = Final_Crop_rotated[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), 10:40]
        temp_a1 = resized[int(height_Final_Rotated*1/8):40, 65:100]
        temp_a5 = resized[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)]
        temp_a7 = resized[int(height_Final_Rotated*1/2) + 15:int(height_Final_Rotated*1/2) + 45, int(width_Final_Rotated*1/2)+20 :int(width_Final_Rotated*1/2) + 45]
            
       
        #print(int(temp_a1.shape[1]/2))
        
        #calcula justo el centro del cuadro para evitar tomar otros colores que no son. Solo toma un valor
        #entre 0 y 255 (255 para blanco) aunque con buena iluminacion, el gris esta entre 100 y 130, con iluminacion media
        #puede estar entre 60 y 80.
    
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
        #cv.imshow("Color_a1",Final_Crop_rotated[int(height_Final_Rotated*1/8):40, 65:100])
        #cv.imshow("Color_a7",Final_Crop_rotated[int(height_Final_Rotated*1/2) + 15:int(height_Final_Rotated*1/2) + 45, int(height_Final_Rotated*1/2) :int(height_Final_Rotated*1/2) + 26])
                
        #print("int(height_Final_Rotated*1/4 + 2))",int(height_Final_Rotated*1/4 + 2))
            #ColorInfIzq = sum(sum(Final_Crop_rotated[int(height_Final_Rotated*1/4 + 50):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 25)]))
                #ColorInfIzq = (ColorInfIzq1[0] + ColorInfIzq1[1] + ColorInfIzq1[2])/3
        #print("inferior izquierdo")
        #print(ColorInfIzq)
        #print(" ")
        
        
        #para debug, muestra los cuadros detectados
        #--------------------------------
        #cv.imshow("Color_a0",resized[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), int(height_Final_Rotated*1/8)+25:int(height_Final_Rotated*1/8)+52])
        cv.imshow("Color_a0_2",resized[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), int(width_Final_Rotated*1/8)+25:int(width_Final_Rotated*1/8)+55])
        cv.imshow("Color_a1",resized[int(height_Final_Rotated*1/8):40, 65:100])
        cv.imshow("Color_a2",resized[int(height_Final_Rotated*1/8)+30:int(height_Final_Rotated*1/8 + 30)+22, 12:38])
        cv.imshow("Color_a3",resized[int(height_Final_Rotated*1/8 + 2)+23:int(height_Final_Rotated*1/8 + 25)+30, 10+30:35+30])
        cv.imshow("Color_a4",resized[int(height_Final_Rotated*1/8)+30:40+30, 65:95])
        cv.imshow("Color_a5",resized[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8):int(height_Final_Rotated*1/8 + 23)])
        cv.imshow("Color_a6",resized[int(height_Final_Rotated*1/4 + 42):int(height_Final_Rotated*1/2 + 40), int(height_Final_Rotated*1/8)+30:int(height_Final_Rotated*1/8 + 23)+30])
        cv.imshow("Color_a7",resized[int(height_Final_Rotated*1/2) + 15:int(height_Final_Rotated*1/2) + 45, int(width_Final_Rotated*1/2)+20 :int(width_Final_Rotated*1/2) + 45])
        #--------------------------------
        
        
            #Generando los valores para detectar el codigo.
        temp_a3 = resized[int(height_Final_Rotated*1/8 + 2)+23:int(height_Final_Rotated*1/8 + 25)+30, 10+30:35+30]
        a3 = temp_a3[int(temp_a3.shape[0]/2),int(temp_a3.shape[1]/2)]
            
        #print("a3: ", a3)
            
        temp_a2 = resized[int(height_Final_Rotated*1/8)+30:int(height_Final_Rotated*1/8 + 30)+22, 12:38]
        a2 = temp_a2[int(temp_a2.shape[0]/2),int(temp_a2.shape[1]/2)]
        #print("a2: ", a2)
        
        #print("height_Final_Rotated*1/8: ",height_Final_Rotated*1/8)
        temp_a0 = resized[int(height_Final_Rotated*1/8 + 2):int(height_Final_Rotated*1/8 + 30), int(height_Final_Rotated*1/8)+25:int(height_Final_Rotated*1/8)+52]
        a0 = temp_a0[int(temp_a0.shape[0]/2),int(temp_a0.shape[1]/2)]
        #print("a0: ", a0)
            
            
        temp_a4 = resized[int(height_Final_Rotated*1/8)+30:40+30, 65:95]
        a4 = temp_a4[int(temp_a4.shape[0]/2),int(temp_a4.shape[1]/2)]
        #print("a4: ", a4)
            
        temp_a6 = resized[int(height_Final_Rotated*1/4 + 50):int(height_Final_Rotated*1/2 + 60), int(height_Final_Rotated*1/8)+20:int(height_Final_Rotated*1/8+30 + 23)+40]
        #cv.imshow("temp_a6", temp_a6)
        #cv.waitKey(0) 
        #print(temp_a6)
        #print(int(temp_a6.shape[0]/2))
        #print(int(temp_a6.shape[1]/2))
        a6 = temp_a6[int(temp_a6.shape[0]/2),int(temp_a6.shape[1]/2)]
        #print("a6: ", a6)
    
            
        #guarda los valores en este vector para luego proceder a su identificacion
        code = [a7,a6,a5,a4,a3,a2,a1,a0]
        
        #para debug, muestra como quedo el codigo al final
        cv.imshow("Codigo", resized)
        cv.waitKey(0)      
        
        
        #NO SE USA, PERO DE MOMENTO, NO SE BORRARA HASTA VERIFICAR QUE NO INTERFIERA CON EL FUNCIONAMIENTO 
        #DE ESTE CODIGO
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
        
        #Variable que guardara el valor del codigo
        CodigoBinString = ""
        
        #para debug, imprime el valor del vector de bits.
        print(code)
        #print(len(code))
        
        i = 0 #para evitar alguna sobreescritura de esta variable.
        for i in range (0, len(code)):
            #print(i)
            #print("codigo en la posicion i: ", code[i] )
            
            #con los tresholds establecidos, busca que valores sean grises y los cataloga como 1,
            #sino, los catalaga como 0.
            if code[i] > TRESHOLD_DETECT_MIN and code[i]< TRESHOLD_DETECT_MAX:
                
                CodigoBinString = CodigoBinString + "1"
            else:
                CodigoBinString = CodigoBinString + "0"

    
    
        #Guardamos los valores
        if a == 0:
            
            #para debug, imprime el codigo binario en formato string
            print("Codibo binario: ",CodigoBinString)
            
            #esta funcion pasa el string de bits a formato de numero int.
            tempID =int(CodigoBinString, 2)
            
            #calcula las posiciones y demas parametros del robot.
            tempFloatX = (anchoMesa / GlobalWidth) * Cx;
            tempFloatY = (largoMesa / GlobalHeigth) * Cy;
            tempX = int(tempFloatX)
            tempY = int(tempFloatY)
            tempTheta = int(tempFloatTheta)
            pos = [tempX, tempY, tempTheta]
            
            #para debug y seperacion
            print("ID temporal",tempID)
            print("-------------------")
            print(" ")
            
        else:
            #en caso de falla, aunque por las modificaciones ya no se usa,
            #de igual forma se deja para evitar errores
            tempID = 0
            tempFloatX = (anchoMesa / GlobalWidth) * Cx;
            tempFloatY = (largoMesa / GlobalHeigth) * Cy;
            tempX = int(tempFloatX)
            tempY = int(tempFloatY)
            tempTheta = int(tempFloatTheta)
            pos = [0, 0, 0]
        

        
        return Robot(tempID,"", pos) #si ctrl es 1, se retorna el valor correcto
    return Robot(0,"", [0,0,0]) #si ctrl es 0, retorna un araray vacio.

