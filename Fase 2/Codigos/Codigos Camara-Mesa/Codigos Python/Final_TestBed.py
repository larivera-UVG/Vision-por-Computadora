#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:26:33 2020
@author: Jose Pablo Guerra
Codigo que implementa Calibracion y generacion de codigos para la mesa de pruebas
Proximamente: detectar la pose de los robots.
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
"""


from Calibracion import camara, vector_robot, Robot
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

#-------------------------------------------------------
#Para la generacion de los codigos y la tome de poses


#from Robot import vector_robot, Robot

#de momento no se usan
SQRTDE2 = 1.41421356
MyPI = 3.14159265

#revisar si es que se usan
anchoMesa = 14.5
largoMesa = 28.0

#de momento no se usan
GlobalCodePixThreshold = 80
GlobalColorDifThreshold = 10

#si se usan
MyGlobalCannyInf = 185
MyGlobalCannySup = 330
Code_size = 1.0 #no se usa

#si se usan
MAX_IMAGE_SIZE = 75

#Para detectar los cuadros grises, normalmente con buena iluminacion pueden llegar a tener un valor de 130 (o mas)
#pero para condiciones de poca luz, el valor MIN puede variar. 
TRESHOLD_DETECT_MIN = 65
TRESHOLD_DETECT_MAX = 130

#Mat GlobalLambda, GlobalCroppedActualSnap;

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
            vector.agregar_robot(getRobot_fromSnapshot(RecCod, gray_blur_img, Medida_cod))

    #para debug, imprime el ID del robot que se identifico y lo  busca en la base de vector_robot()
    #print("Yo soy el robot con 40 y tengo los siguientes atributos: ", vector.get_robot_id(40))
    #print("Yo soy el robot con 30 y tengo los siguientes atributos: ", vector.get_robot_id(30))
    #print("Yo soy el robot con 50 y tengo los siguientes atributos: ", vector.get_robot_id(50))
    return vector

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
        

        
        return robot.set_robot(tempID,"", pos) #si ctrl es 1, se retorna el valor correcto
    return robot.set_robot(0,"", [0,0,0]) #si ctrl es 0, retorna un araray vacio.

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
        getRobot_Code(snapshot_robot, MyGlobalCannyInf, MyGlobalCannySup, numCod)
    
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