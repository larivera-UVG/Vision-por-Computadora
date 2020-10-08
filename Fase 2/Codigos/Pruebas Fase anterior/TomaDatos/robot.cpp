#include "robot.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <vector>

using namespace std;


robot::robot(int _id, string _ip, int _x, int _y, int _theta)
{
    id = _id;
    ip = _ip;
    x = _x;
    y = _y;
    theta = _theta;
    vl = vr = 0;
}

void robot::set_IP(string _ip)
{
    ip = _ip;
}

void robot::set_Pose(int _x, int _y, int _theta)
{
    x = _x;
    y = _y;
    theta = _theta;
}

vector<int> robot::get_Pose()
{
    vector<int> Pose;
    Pose.push_back(x);
    Pose.push_back(y);
    Pose.push_back(theta);
    return Pose;
}

string robot::get_IP()
{
    return ip;
}

vector<int> robot::get_Speed()
{
    vector<int> speed;
    speed.push_back(vl);
    speed.push_back(vr);
    return speed;
}

void robot::set_Speed(int _vl, int _vr)
{
    vl = _vl;
    vr = _vr;
}

