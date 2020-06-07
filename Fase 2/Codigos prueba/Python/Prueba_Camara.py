"""
Jose Pablo Guerra 
Programa de ejemplo para captura de video y procesamiento de imagen usando OpenCV

Version final.

"""

"""
Anotaciones iniciales:
    
De preferencia utilizar la suite de anaconda, esto permite instalar los paquetes 
de manera mas adecuada y evitar errores entre versionres o que las librerias esten
correctamente linkeadas al compilador. 

"""


import cv2 as cv #importando libreria para opencv 

cap = cv.VideoCapture(0) #VideoCapture(n) n = 0 para otras que no sean la camara principal.

if not cap.isOpened(): #detectando si la camara esta disponible.
    print("Cannot open camera")
    exit()
while True:

    ret, frame = cap.read() #lectura y caputra del frame

    #print(ret)
    if not ret: #debugin del frame, si hay problemas sale del programa
                #Al inicio siempre puede dar un problema para detectar los frames de video
                
        print("Can't receive frame (stream end?). Exiting ...")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #captura de video y procesamiento de imagen a tono de grises.

    cv.imshow('frame', gray) #despliega los cambios hechos en el frame
    if cv.waitKey(1) == ord('q'): #para salir presione q. 
        break

#salir correctamente. 
cap.release()
cv.destroyAllWindows()
