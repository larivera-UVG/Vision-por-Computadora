import cv2
def Capturar():
    cam = cv2.VideoCapture(0)
    
    cv2.namedWindow("test")
    
    img_counter = 0
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error, frame no encontrado")
            break
        cv2.imshow("test", frame)
    
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC presionado
            print("Escape presionado, cerrando...")
            break
        elif k%256 == 32:
            # SPACE presionado
            img_name = "opencv_frame_{}.png".format(img_counter) #Formato del nombre de la imagen.
                                                #Guarda el numero de frame (foto) que se tomo.
            cv2.imwrite(img_name, frame) #Guarda la foro
            print("{} Guardado!".format(img_name)) #mensaje de Ok para el save de la foto.
            img_counter += 1 #aumenta el contador. 
        
    return frame
    cam.release()
    cv2.destroyAllWindows()
    
Capturar()

