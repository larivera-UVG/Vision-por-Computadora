#ifndef VECTORROBOTS_H
#define VECTORROBOTS_H

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include "robot.h"

using namespace std;
class VectorRobots
{
public:
    //Atributos
    vector<robot> Vrobots;


    //Metodos
    VectorRobots();
    void agregar_robot(robot _robot);
    int buscarPosID_robot(int _id);
    robot get_Robot(int _id);
};

#endif

