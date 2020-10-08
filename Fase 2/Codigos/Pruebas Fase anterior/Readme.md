Este es el código utilizado en la fase anterior con leves modificaciones para correr en el sistema operativo MacOS Catalina
versión 10.15.4 (al 21 de mayo de 2020)

Para su correcto funcionamiento seguir estos pasos:

********************************************
*CONFIGURACION openCV MacOS*
********************************************


1. En la pestaña Projects (Proyecto) buscar la opción build
2. Luego, buscar Build Enviroment
3. Luego editar PATH, agregar después del último bin  __:/usr/local/bin/__ .
4. Click en ADD
5. Agregar el path /usr/local/lib/pkgconfig/  que puede ser obtenido con el comando:
    __find /usr/local -name "opencv.pc"__
6. El nombre de la variable debe ser __PKG_CONFIG_PATH__
7. En caso de tener otro error, irse a la pestaña de _RUN_, buscar __RUN ENVIROMENT__
8. Darle __unset__ a la variable con el nombre __DYLD_LIBRARY_PATH__

Finalmente, editar el .pro del proyecto y agregar esto al final:


QT_CONFIG -= no-pkg-config

CONFIG  += link_pkgconfig

PKGCONFIG += opencv

Si aparece algo con una libreria "hello-opencv" o similar a este nombre, eliminar todo eso y dejar solo lo listado arriba.
NO TOCAR OTRA CONFIGURACION DEL ARCHIVO.

Para un ejemplo, referirse a "example.pro"

PROBADO CON LA LIBRERIA OPENCV 3.4.1 y el uso de los siguientes links:
	•	https://www.learnopencv.com/configuring-qt-for-opencv-on-osx/
	•	https://medium.com/@romogo17/how-to-build-and-install-from-source-opencv-with-qt-support-in-macos-921989518ab5

Y el siguiente video:
	•	https://www.youtube.com/watch?v=SIXnD-9uh1k
