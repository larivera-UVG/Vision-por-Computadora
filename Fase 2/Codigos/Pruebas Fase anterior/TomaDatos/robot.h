#ifndef ROBOT_H
#define ROBOT_H

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <vector>

using namespace std;

class robot
{
public:
    //Atributos
    int id, x, y, theta, vl, vr;
    string ip;
    //Metodos
    robot(int _id, string _ip, int _x, int _y, int _theta);
    void set_IP(string _ip);
    void set_Pose(int _x, int _y, int _theta);
    void set_Speed(int _vl, int _vr);
    vector<int> get_Pose();
    string get_IP();
    vector<int> get_Speed();

};

#endif

