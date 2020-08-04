#ifndef TOMAPOSEROBOTS_H
#define TOMAPOSEROBOTS_H

#include <math.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include "Swarm_robotic.h"

VectorRobots getRobotCodes(Mat _CropPhoto, int _CannyVinf, int _CannyVsup);
void updateRobotCodes(VectorRobots &_lastVRobotCodes, Mat _CropPhoto, int _CannyVinf, int _CannyVsup);
robot getRobotfromSnapShot(RotatedRect _RecContorno);
int getLambdaWiHe();
Mat getCroppedSnapshot(Mat _snap);


#endif // TOMAPOSEROBOTS_H
