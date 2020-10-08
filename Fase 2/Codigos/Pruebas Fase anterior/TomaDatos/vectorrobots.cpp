#include "VectorRobots.h"
#include "robot.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <vector>

using namespace std;


VectorRobots::VectorRobots()
{
}

void VectorRobots::agregar_robot(robot _robot)
{
    Vrobots.push_back(_robot);
}

int VectorRobots::buscarPosID_robot(int _id)
{
    int finalID = -1;
    for (int i = 0; i < Vrobots.size(); ++i) {
        robot tempRobot = Vrobots.at(i);
        if (tempRobot.id == _id) {
            finalID = i;
            break;
        }
    }

    return finalID;
}

robot VectorRobots::get_Robot(int _id)
{
    if (_id >= 0)
        return Vrobots.at(_id);
    else
        return robot(-1,"No hay robot",0,0,0);
}
