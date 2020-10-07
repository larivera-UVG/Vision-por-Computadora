[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Generic badge](https://img.shields.io/badge/Spyder-v4.1.4-<COLOR>.svg)](https://shields.io/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
# Continuación Fase 1 de Algoritmo de Visión por Computadora.

## Indice:
1. [Introducción](#Introducción)

2. [Requerimientos](#Requerimientos)

   1. [Versiones de Software](#versiones-soft)
  
   2. [Hardware](#versiones-hard)

3. [Contenido del Repositorio](#RepoContent)

4. [Algoritmo Para el Reconocimiento de la Pose de Agentes](#algoritmo-pose-python)

5. [Uso de la Herramienta](#Herramienta)

   1. [Calibración de Cámara](#calibración-de-cámara)
   
   2. [Creación de Marcadores](#creación-de-marcadores)
   
   3. [Obtención de Pose](#obtención-de-pose)



## Introducción
El objetivo principal de este repositorio es brindarle al usuario una herramienta de _software_ diseñada para reconocer o identificar la posición de los agentes o robots, normalmente empleados en la Robótica de Enjambre. 

Principalmente se presentan dos versiones para dos lenguajes distintos: __C++__ y __Python__.
La versión original de esta herramienta fue creada en __C++__ y como objetivo de la __Fase 2__ se presenta una migración hacia __Python___.
Ambas herramientas permiten la [_calibración de la cámara_](#calibración-de-cámara), la generación de [_marcadores_](#creación-de-marcadores) y la [_obtención de pose de los robots en la mesa de trabajo_](#obtención-de-pose)

## Requerimientos <a name="Requerimientos"></a>
  ### Versiones de Software <a name="versiones-soft"></a>
  Para la versión en Python se utiliza la Suite de Anaconda que incluye diferentes programas relacionados con Python. Es recomendable utilizar esta suite ya que incluye todos las librerías que se necesitan y hace más fácil la instalación de cualquier otra que se necesite.
  Su versión de instalación para Windows, MacOS y Linux se puede obtener de aquí: https://www.anaconda.com/products/individual
  La versión de Python utilizada fue __v3.7.6__, que es la versión por default que trae Anaconda con el IDE de Spyder. 
  
  #### Instalación OpenCV utilizando Anaconda y MacOS
  En caso de desear utilizar la suite de anaconda, se instala anaconda utilizando el instalador del sitio web oficial y se procede a seguir este hilo de solución:
  https://github.com/conda/conda/issues/9367
  
Específicamente, estos comandos son los que se necesita correr en la terminal:

conda create -n opencv
conda activate opencv
conda install -c anaconda opencv

estos comandos instalan la version 3.4.2 que para fines de uso, considero adecuados, si se desea la 4 (por alguna razón) ejecutar este comando (no probado)

conda install -c conda-forge opencv

esto instala opencv3

Se procede a instalar opencv en el environment de anaconda llamado OpenCV (creado con las líneas de comando mencionadas arriba) y se requiere instalar spyder en este nuevo environment (probado).

#### Tutorial para instalar openCV para Python MacOS

Esta versión de instalación se usa para correr OpenCV sin utilizar la Suite de Anaconda. 

https://www.youtube.com/watch?v=nO3csmVyoOQ

Y en caso de falla, utilizar el siguiente en comando
pip install opencv-python==4.1.2.30

De preferencia, instalar python 3.7 (probado) no la version 3.8

  
  
  ### Hardware <a name="versiones-hard"></a>

## Contenido del Repositorio <a name="RepoContent"></a>
### Fase 2
En esta carpeta incluye la documentación y programas de la fase 2. 
El objetivo es realizar la migraición del programa orignal en C++ hacia el lenguaje Python.
Contiene dos carpetas "Codigos" y "Doc".

Los programas ubicados en la carpeta __Codigos__ estan los codigos en Python y C++ con implementación de POO y programación multi-hilos.
Los programas ubicados en la carpeta __Doc__ se tienen los archivos referentes a guías, manuales y documentación en general.

## Algoritmo Para el Reconocimiento de la Pose de Agentes <a name="algoritmo-pose-python"></a> 

## Uso de la Herramienta <a name="Herramienta"></a>
### Calibración de Cámara
### Creación de Marcadores
### Obtención de Pose




