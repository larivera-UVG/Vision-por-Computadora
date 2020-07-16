#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 18:49:30 2020

@author: Jose Pablo Guerra

Codigo para la toma de poses de robots en la mesa de pruebas.


15/07/2020: Version 0.0.0 -- Creacion del archivo inicial.

Basado en el codigo escrito por André Rodas
"""

_Robot = []

class Robot():
    def __init__(self):
        _Robot = []
        
    def set_robot(self, _id, _ip, _pos):
        id_robot = _id
        ip = _ip
        #x = _pos[0]
        #y = _pos[1]
        #theta = _pos[2]
        velR = 0
        velL = velR
        robot = [id_robot,ip,_pos,velR,velL]
        return robot
        
    def set_IP(self,ip):
        return ip
    
    def set_pos(self, pos):
        x = pos[0]
        y = pos[1]
        theta = pos[2]
        
    def get_pos(self):
        Pos = []
        Pos.append(self.x)
        Pos.append(self.y)
        Pos.append(self.theta)
        return Pos
        
    def get_IP (self):
        return self.ip
    
    def set_speed(self, vel):
        vel_right = vel[0]
        vel_left = vel[1]
        
    def get_speed(self):
        speed = []
        speed.append(self.vel_right)
        speed.append(self.vel_left)
        return speed
    
    def agregar_robot(self,vector_robot):
        global _Robot
        _Robot.append(vector_robot)
        return _Robot
    
    def search_id_robot(self, _id):
        final_ID = -1
        for i in range (0, len(_Robot)):
            temp_Robot = _Robot[i]
            if (temp_Robot[0] == _id):
                final_ID = i 
                break
        return final_ID
        
Robot = Robot()
#Robot.set_IP(19)
#Robot.set_speed([9,0])
#Robot.set_pos([1,2,3])
r = Robot.set_robot(1, 19, [1,2,3])
r1 = Robot.set_robot(2, 19, [1,2,3])
r2 = Robot.set_robot(3, 19, [1,2,3])
Robot.agregar_robot(r)
Robot.agregar_robot(r1)
vector_robot = Robot.agregar_robot(r2)

print(vector_robot)
print(vector_robot[1])
ID = Robot.search_id_robot(3)
print(ID)