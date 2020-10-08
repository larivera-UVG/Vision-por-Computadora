# Codigos de lenguaje Python para Visión por Computadora

## Introducción

Esta carpeta incluye los códigos en lenguaje Python con POO y programación multi-hilos donde aplique.

## Indice:
1. [Introducción](#Introducción)

2. [Requerimientos](#Requerimientos)

3. [Contenido de la Carpeta](#Contenido-de-la-Carpeta)

4. [Algoritmo Para el Reconocimiento de la Pose de Agentes en Python](#Algoritmo-Para-el-Reconocimiento-de-la-Pose-de-Agentes-en-Python)

   1. [Librería Swarm_robotic.py](#Swarm)

   2. [Librería para la Toma de Pose](#TomaPose)

   3. [Programa Principal e Interfaz de Usuario](#GUI)

5. [Otra documentación](#otra-documentación)
   1. [Versionado de los programs en python](#Versionado-de-los-programs-en-python)
      1. [Versión inicial](#Al-5-de-julio-del-2020)
      2. [Versión 0.1](#Al-8-de-agosto-del-2020)
      3. [Versión 0.2](#Al-10-de-agosto-del-2020)
      4. [Versión Release](#5-de-octubre-del-2020)
## Requerimientos

Favor referirse a la sección de Requerimientos en el [ReadMe](https://github.com/larivera-UVG/Vision-por-Computadora/blob/master/Fase%202/ReadMe.md#Requerimientos) de la carpeta principal.

## Contenido de la Carpeta
La carpeta contiene lo siguiente:

1. [Codigos Python](Codigos%20Python) que contiene todos los códigos de la migración desde la versión original de __C++__ a __Python___

2. [Codigos C++](Codigos%20C++) que contiene la versión original en __C++__ pero con aplicación de Progrmación Orientada a Objetos y multi-hilos.

## Algoritmo Para el Reconocimiento de la Pose de Agentes en Python
### Librería Swarm_robotic.py  <a name="Swarm"></a>
### Librería para la Toma de Pose  <a name="TomaPose"></a>
### Programa Principal e Interfaz de Usuario  <a name="GUI"></a>

## Otra documentación
### Versionado de los programs en python

#### Al 5 de julio del 2020

Se tiene la calibración ya incluida, con unas funciones por migrar a Python.
Pruebas realizadas, exitosas. Calibración OK.

Para una mejor calibración, utilizar figuras circulares en los bordes de la mesa, esto hace que el algoritmo funcione mejor.
Luego de eso, con estas esquinas, se ajusta la perspectiva de la imagen, se guarda la matriz y ya se puede usar esa información.

Función de guardar la matriz pendiente.

#### Al 8 de agosto del 2020

Versión final (pendiente guardar calibración) de la calibración. Se agrega la parte de generar código para la detección de los robots en la mesa. Se agrega una interfaz gráfica que se pretende ir mejorando.

Los métodos y funciones están en el archivo: Calibracion.py
El archivo general __main__ es llamado Final_TestBed.py

Las imágenes agregadas en esta carpeta son pruebas correspondientes a la calibración para dejar constancia de su funcionamiento.
la imagen Cod.jpg es el código generado para la detección de los robots, a manera de comparativa con el código de André Rodas.

#### Al 10 de agosto del 2020

Se añaden varias funciones tanto en la GUI como en las diferentes liberías usadas para estos códigos (Para mayor información leer el versionado en cada uno de los archivos que están incluidos dentro de esta carpeta.

Esta versión ya cuenta con dos variaciones de documentos, una sin hilos y otra con hilos. De momento, la versión con hilos puede procesar e identificar los códigos, aunque faltaría un hilo de captura continua.


#### 5 de octubre del 2020

GUI mejor diseñada que unifica todas las funciones de esta herramienta. Mejoras al código en general y una versión _release_ que podría considerarse como final (a falta de revisar otros puntos de mejora si los hubiera.
