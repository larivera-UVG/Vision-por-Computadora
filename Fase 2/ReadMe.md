[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Generic badge](https://img.shields.io/badge/Spyder-v4.1.4-<COLOR>.svg)](https://shields.io/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/) [![Generic badge](https://img.shields.io/badge/Swarm__robotic-v0.11.4-<COLOR>.svg)](https://shields.io/) [![Generic badge](https://img.shields.io/badge/toma__pose-v0.3.2-<COLOR>.svg)](https://shields.io/) [![Generic badge](https://img.shields.io/badge/GUI-v0.14.0-<COLOR>.svg)](https://shields.io/)
# Continuación Fase 1 de Algoritmo de Visión por Computadora.

## Indice:
1. [Introducción](#Introducción)

2. [Contenido del Repositorio](#contenido-del-repositorio)

2. [Requerimientos](#Requerimientos)

   1. [Software](#versiones-soft)
      1. [Instalación OpenCV utilizando Anaconda y MacOS](#Anaconda_install)
      2. [Librerías utilizadas en Python](#lib_python)

   2. [Hardware](#versiones-hard)

3. [Contenido del Repositorio](#RepoContent)

4. [Algoritmo Para el Reconocimiento de la Pose de Agentes](#algoritmo-pose-python)

   1. [Calibración de Cámara](#calibración-de-cámara)

   2. [Creación de Marcadores](#creación-de-marcadores)

   3. [Obtención de Pose](#obtención-de-pose)

5. [Otra documentación](#otra-documentación)


## Introducción
El objetivo principal de este repositorio es brindarle al usuario una herramienta de _software_ diseñada para reconocer o identificar la posición de los agentes o robots, normalmente empleados en la Robótica de Enjambre.

Principalmente se presentan dos versiones para dos lenguajes distintos: __C++__ y __Python__.
La versión original de esta herramienta fue creada en __C++__ y como objetivo de la __Fase 2__ se presenta una migración hacia __Python___.
Ambas herramientas permiten la [_calibración de la cámara_](#calibración-de-cámara), la generación de [_marcadores_](#creación-de-marcadores) y la [_obtención de pose_](#obtención-de-pose) de los robots en la mesa de trabajo.

Para una mejor navegación, este _ReadMe_ contiene varios hipervinculos que permiten al usuario encontrar de mejor manera las secciones dentro de este documento o carpetas dentro de este repositorio.

## Contenido del Repositorio
### Fase 2
Los programas están ubicados en la carpeta [__Codigos__](Codigos). Estos códigos son todos los programas utilizados para la herramienta de la toma de pose, creación de marcadores y calibración de la cámara. Están implementados en Python y C++ con implementación de POO y programación multi-hilos. Además, incluyen otros programas de ejemplos y referencias para el uso de la herramienta, así como ilustrar el uso de multi-hilos y las funciones de OpenCV.

Los documentos como manuales, la tesis de la fase 2 y otra documentación están ubicados en la carpeta [__Doc__](Doc).
