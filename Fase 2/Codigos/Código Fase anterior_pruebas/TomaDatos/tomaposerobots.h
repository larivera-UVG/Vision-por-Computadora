#ifndef TOMAPOSEROBOTS_H
#define TOMAPOSEROBOTS_H

#include <math.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include "vectorrobots.h"
#include "opencv2/highgui.hpp"

using namespace cv;
using namespace std;

#define SQRTDE2 1.41421356
#define MyPI 3.14159265

const float anchoMesa = 128.4;
const float largoMesa = 88.4;

int GlobalCodePixThreshold = 5;
int GlobalColorDifThreshold = 20;
int GlobalWidth, GlobalHeigth = 0;
Mat GlobalLambda, GlobalCroppedActualSnap;

Mat readHomogenea();
Mat readDims();
VectorRobots getRobotCodes(Mat _CropPhoto, int _CannyVinf, int _CannyVsup, float _CmCodeSize);
void updateRobotCodes(VectorRobots &_lastVRobotCodes, Mat _CropPhoto, int _CannyVinf, int _CannyVsup, float _CmCodeSize);
robot getRobotfromSnapShot(RotatedRect _RecContorno);
void getLambdaWiHe();
Mat getCroppedSnapshot(Mat _snap);
int binTxttoint(string a);


Mat readHomogenea() {
    Mat lambda;
    FileStorage storage("homogenea.yml", cv::FileStorage::READ);
    storage["homogenea"] >> lambda;
    storage.release();
    return lambda;
}

Mat readDims() {
    Mat dim;
    FileStorage storage("dim.yml", cv::FileStorage::READ);
    storage["dim"] >> dim;
    storage.release();
    return dim;
}

void updateRobotCodes(VectorRobots &_lastVRobotCodes, Mat _CropPhoto, int _CannyVinf, int _CannyVsup, float _CmCodeSize) {

    VectorRobots updatedRobots = getRobotCodes(_CropPhoto, _CannyVinf, _CannyVsup, _CmCodeSize);
    for (int i = 0; i < _lastVRobotCodes.Vrobots.size(); i++)
    {
        int CurrentID = _lastVRobotCodes.Vrobots.at(i).id;
        int NewID = updatedRobots.buscarPosID_robot(CurrentID);
        vector<int> NewPose = updatedRobots.Vrobots.at(NewID).get_Pose();
        _lastVRobotCodes.Vrobots.at(i).set_Pose(NewPose.at(0), NewPose.at(1), NewPose.at(2));
    }

}



VectorRobots getRobotCodes(Mat _CropPhoto, int _CannyVinf, int _CannyVsup, float _CmCodeSize)
{
    VectorRobots ActualRobots;
    Mat _CropGrayPhoto, _CannyPhoto;
    vector<vector<Point>> contornos;
    vector<Vec4i> jerarquia;

    GlobalCroppedActualSnap = _CropPhoto;

    float PixCodeSize = _CmCodeSize * (_CropPhoto.size().width / anchoMesa);

    cvtColor(_CropPhoto, _CropGrayPhoto, CV_BGR2GRAY);
    blur(_CropGrayPhoto, _CropGrayPhoto, Size(3, 3));
    Canny(_CropGrayPhoto, _CannyPhoto, _CannyVinf, _CannyVsup, 3);
    imshow("canny", _CannyPhoto);
    waitKey(0);
    findContours(_CannyPhoto, contornos, jerarquia, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));
    blur(_CropGrayPhoto, _CropGrayPhoto, Size(3, 3));

    RotatedRect SingleRecCod, LastRecCod;
    for (int i = 0; i < contornos.size(); i++)
    {
        SingleRecCod = minAreaRect(contornos[i]);
        if (((abs(SingleRecCod.size.width - PixCodeSize) < GlobalCodePixThreshold) && (abs(SingleRecCod.size.height - PixCodeSize) < GlobalCodePixThreshold)))
        {
            if (i == 0)
            {
                ActualRobots.agregar_robot(getRobotfromSnapShot(SingleRecCod));
                LastRecCod = SingleRecCod;
            }
            else if (((abs(SingleRecCod.center.x - LastRecCod.center.x) > GlobalCodePixThreshold) || (abs(SingleRecCod.center.y - LastRecCod.center.y) > GlobalCodePixThreshold)))
            {
                ActualRobots.agregar_robot(getRobotfromSnapShot(SingleRecCod));
                LastRecCod = SingleRecCod;
            }
        }
    }

    return ActualRobots;
}


robot getRobotfromSnapShot(RotatedRect _RecContorno)
{
    Mat SemiCropCodRotated, finalCropCodRotated;
    int tempID, tempX, tempY, tempTheta;
    float tempFloatX, tempFloatY, tempFloatTheta, tempWiMitad, tempHeMitad;

    tempWiMitad = SQRTDE2 *_RecContorno.size.width / 2;
    tempHeMitad = SQRTDE2 * _RecContorno.size.height / 2;
    Range rows((int)(_RecContorno.center.y - tempHeMitad), (int)(_RecContorno.center.y + tempHeMitad));
    Range cols((int)(_RecContorno.center.x - tempWiMitad), (int)(_RecContorno.center.x + tempWiMitad));
    Mat SemiCropCod = GlobalCroppedActualSnap(rows, cols);
    Mat tempRotMat = getRotationMatrix2D({ (float)(rows.size() / 2.0), (float)(cols.size() / 2.0)}, _RecContorno.angle, 1.0);
    warpAffine(SemiCropCod, SemiCropCodRotated, tempRotMat, SemiCropCod.size(), INTER_CUBIC);
    getRectSubPix(SemiCropCodRotated, _RecContorno.size, { (float)(rows.size() / 2.0), (float)(cols.size() / 2.0) }, finalCropCodRotated);
    cvtColor(finalCropCodRotated, finalCropCodRotated, CV_BGR2GRAY, 0);

    int EscalaColores[3]; //[2] blaco, [1] gris, [0] negro
    int ColorSupIzq = finalCropCodRotated.at<uchar>(finalCropCodRotated.size().height * 1 / 4, finalCropCodRotated.size().width * 1 / 4);
    int ColorSupDer = finalCropCodRotated.at<uchar>(finalCropCodRotated.size().height * 1 / 4, finalCropCodRotated.size().width * 3 / 4);
    int ColorInfDer = finalCropCodRotated.at<uchar>(finalCropCodRotated.size().height * 3 / 4, finalCropCodRotated.size().width * 3 / 4);
    int ColorInfIzq = finalCropCodRotated.at<uchar>(finalCropCodRotated.size().height * 3 / 4, finalCropCodRotated.size().width * 1 / 4);
    EscalaColores[0] = EscalaColores[1] = EscalaColores[2] = ColorSupIzq;
    tempFloatTheta = _RecContorno.angle;

    if ((ColorSupDer > ColorSupIzq) && (ColorSupDer > ColorInfDer) && (ColorSupDer > ColorInfIzq))
    {
        rotate(finalCropCodRotated, finalCropCodRotated, ROTATE_90_COUNTERCLOCKWISE);
        tempFloatTheta = tempFloatTheta + 90;
        EscalaColores[2] = ColorSupDer;
    }
    else if ((ColorInfDer > ColorSupIzq) && (ColorInfDer > ColorSupDer) && (ColorInfDer > ColorInfIzq))
    {
        rotate(finalCropCodRotated, finalCropCodRotated, ROTATE_180);
        tempFloatTheta = tempFloatTheta + 180;
        EscalaColores[2] = ColorInfDer;
    }
    else if ((ColorInfIzq > ColorSupIzq) && (ColorInfIzq > ColorInfDer) && (ColorInfIzq > ColorSupDer))
    {
        rotate(finalCropCodRotated, finalCropCodRotated, ROTATE_90_CLOCKWISE);
        tempFloatTheta = tempFloatTheta - 90;
        EscalaColores[2] = ColorInfIzq;
    }


    if ((ColorSupIzq <= ColorSupDer) && (ColorSupIzq <= ColorInfDer) && (ColorSupIzq <= ColorInfIzq))
        EscalaColores[0] = ColorSupIzq;
    else if ((ColorSupDer <= ColorSupIzq) && (ColorSupDer <= ColorInfDer) && (ColorSupDer <= ColorInfIzq))
        EscalaColores[0] = ColorSupDer;
    else if ((ColorInfDer <= ColorSupDer) && (ColorInfDer <= ColorSupIzq) && (ColorInfDer <= ColorInfIzq))
        EscalaColores[0] = ColorInfDer;
    else
        EscalaColores[0] = ColorInfIzq;

    imshow("Codigo", finalCropCodRotated);
    waitKey(0);

    int MatrizValColores[3][3];

    for (int u = 1; u <= 3; ++u) {
        for (int v = 1; v <= 3; ++v) {
            int ValColorTemp = finalCropCodRotated.at<uchar>((finalCropCodRotated.size().height * u / 4), (finalCropCodRotated.size().width * v / 4));
            MatrizValColores[(u - 1)][(v - 1)] = ValColorTemp;
            if ((ValColorTemp < EscalaColores[2] - GlobalColorDifThreshold) && (ValColorTemp > EscalaColores[0] + GlobalColorDifThreshold)) {
                EscalaColores[1] = ValColorTemp;
            }
        }
    }

    //Extraemos el codigo binario
    string CodigoBinString = "";
    for (int u = 0; u < 3; ++u) {
        for (int v = 0; v < 3; ++v) {
            if ((u == 0) && (v == 0))
                CodigoBinString = CodigoBinString;
            else if ((MatrizValColores[u][v] > EscalaColores[1] - GlobalColorDifThreshold) && (MatrizValColores[u][v] < EscalaColores[1] + GlobalColorDifThreshold))
                CodigoBinString = CodigoBinString + "1";
            else
                CodigoBinString = CodigoBinString + "0";
        }
    }

    //Guardamos los valores
    tempID = binTxttoint(CodigoBinString);
    tempFloatX = (anchoMesa / GlobalWidth) * _RecContorno.center.x;
    tempFloatY = (largoMesa / GlobalHeigth) * _RecContorno.center.y;
    tempX = (int)tempFloatX;
    tempY = (int)tempFloatY;
    //tempFloatTheta = tempFloatTheta * MyPI / 180;
    tempTheta = (int)tempFloatTheta;
    return robot(tempID,"", tempX, tempY, tempTheta);
}

void getLambdaWiHe()
{
    GlobalLambda = readHomogenea();
    Mat dims = readDims();
    GlobalWidth = (int)dims.at<double>(0, 0);
    GlobalHeigth = (int)dims.at<double>(1, 0);
}

Mat getCroppedSnapshot(Mat _snap)
{
    if (GlobalWidth == 0)
        getLambdaWiHe();
    Mat CropSnap;
    warpPerspective(_snap, CropSnap, GlobalLambda , { GlobalWidth, GlobalHeigth });
    return CropSnap;
}

int binTxttoint(string a)
{
    int idnum = 0;
    for (int i = 0; i < a.length(); ++i) {
        int n = a[i] - '0';
        idnum = idnum + (pow(2, i)*n);
    }
    return idnum;
}


#endif // TOMAPOSEROBOTS_H
