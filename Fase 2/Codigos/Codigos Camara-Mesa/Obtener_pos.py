#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 18:49:30 2020

@author: Jose Pablo Guerra

Codigo para la toma de poses de robots en la mesa de pruebas.


15/07/2020: Version 0.0.0 -- Creacion del archivo inicial.
15/07/2020: Version 0.1.0 -- Se crean los primeros metodos iniciales y las clases de robot y vector_robot
16/07/2020: Version 0.2.0 -- Se agregan funciones adicionales para su funcionamiento. 


Basado en el codigo escrito por André Rodas
"""
#Importando las librerias necesarias
import cv2 as cv #importando libreria para opencv 
import numpy as np #para la creacion de arrays
import math as mt #para el uso de herramientas matematicas como raiz cuadrada
#Robot = []

SQRTDE2 = 1.41421356
MyPI = 3.14159265

anchoMesa = 128.4
largoMesa = 88.4

GlobalCodePixThreshold = 5
GlobalColorDifThreshold = 20
GlobalWidth, GlobalHeigth = 0
#Mat GlobalLambda, GlobalCroppedActualSnap;

def getRobot_Code(snapshot, Canny_inf, Canny_sup, Medida_cod):
    blur_size = [3,3]
    height_im, width_im = snapshot.shape[:2]
    pixCodsiez = Medida_cod * width_im / anchoMesa
    gray_img = cv.cvtColor(snapshot, cv.COLOR_BGR2GRAY)
    gray_blur_img = cv.blur(gray_img, blur_size)
    canny_img = cv.Canny(gray_blur_img, Canny_inf, Canny_sup)
    image, contour, hierarchy = cv.findContours(canny_img, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    canny_img = cv.blur(canny_img, blur_size)
    
    for i in contour:
        RecCod = cv.minAreaRect(i)

class Robot():
        
    def set_robot(self, _id, _ip, _pos):
        self.id_robot = _id
        self.ip = _ip
        self.x = _pos[0]
        self.y = _pos[1]
        self.theta = _pos[2]
        self.vel_left = 0
        self.vel_right = self.vel_left
        self.robot = [self.id_robot,self.ip,self.x,self.y,self.theta,self.vel_right,self.vel_left]
        return self.robot
        
    def set_IP(self,ip):
        self.ip = ip
        return ip
    
    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.theta = pos[2]
        
    def get_pos(self):
        Pos = []
        Pos.append(self.x)
        Pos.append(self.y)
        Pos.append(self.theta)
        return Pos
        
    def get_IP (self):
        return self.ip
    
    def set_speed(self, vel):
        self.vel_right = vel[0]
        self.vel_left = vel[1]
        
    def get_speed(self):
        speed = []
        speed.append(self.vel_right)
        speed.append(self.vel_left)
        return speed
    
    
class vector_robot():
    #robot_vector_u = Robot()
    def __init__(self):
        self.Robot_vector = []
        
    
    def agregar_robot(self,vector_robot):
        #self.class_robot = class_robot
        #class_robot.id_robot = self
        #global _Robot
        self.Robot_vector.append(vector_robot)
        return self.Robot_vector
    
    def search_id_robot(self, _id):
        final_ID = -1
        for i in range (0, len(self.Robot_vector)):
            temp_Robot = self.Robot_vector[i]
            if (temp_Robot[0] == _id):
                final_ID = i 
                break
        return final_ID
    
    def get_robot(self, _id):
        if _id == 0:
            return print("No hay robot")
        else:
            return self.Robot_vector[_id]
        
bot = Robot()
vector_bot = vector_robot()
robot1 = bot.set_robot(1, 2,[0,1,3])

#print(bot.get_IP())

new_vector_robot = vector_bot.agregar_robot(robot1)
print(new_vector_robot[0][0])
#new_vector_robot.id_robot

#bot.set_IP(4)

#print(bot.get_IP())
#print(bot.get_speed())

    

