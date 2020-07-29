#include "calibracion_cam.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

/*
 * Autor: Jose Pablo Guerra, basado en el codigo original por Andre Rodas
 * Libreria para la calibracion de la camara, toma de fotos y seteo de width y height de la camara
 *
 * Las funciones siguientes se usan en la calibracion:
 *
 * int * getWiHe(Point* esquina);
    Mat getHomogenea(Point* esquina);
    int* readWiHe();
    float mayor2float(float x1, float x2);
    float distancia2puntos(Point p1, Point p2);
    Point* get_esquinas(Mat src, int valueCanny, void*);
    void saveMat(string name,Mat src);
 *
 * Los siguientes, son los metodos utilizados en la clase Camara
 *
 * -------------------------------------------------------------
 * Mat Calibrar(Mat Snapshot, int calib_param);
 * Recibe: Snapshot - la foto de la camara
 *         calib_param - Parametro de calibracion para canny
 * Retorna: La fotografia calibrada en las esquinas identificadas.
 * -------------------------------------------------------------
 * void Set_camara(int WIDTH, int HEIGHT);
 * Recibe: WIDTH - Alto de la imagen que se desea que la camara capture
 *         HEIGHT - Ancho de la imagen que se desea que la camara capture
 * Retorna: Nada
 * -------------------------------------------------------------
 * Mat Take_picture();
 * Reciber: Nada
 * Retorna: La foto capturada por la camara
 * -------------------------------------------------------------
*/

VideoCapture cam(0);
int * getWiHe(Point* esquina)
{
    static int  WiHeMax[2];
    float W1 = distancia2puntos(esquina[0], esquina[2]);
    float W2 = distancia2puntos(esquina[1], esquina[3]);
    float WiMax = mayor2float(W1, W2);
    float H1 = distancia2puntos(esquina[0], esquina[1]);
    float H2 = distancia2puntos(esquina[2], esquina[3]);
    float HeMax = mayor2float(H1, H2);
    WiHeMax[0] = (int)WiMax;
    WiHeMax[1] = (int)HeMax;
    return WiHeMax;
}

Mat getHomogenea(Point* esquina)
{
    Mat lambda;
    int *WH = getWiHe(esquina);
    Point2f esquinaFloat[4] = { esquina[0],esquina[2],esquina[1] ,esquina[3] };
    Point2f esquinasFinales[4] = { { 0, 0 },{ (float)WH[0], 0 },{ 0,(float)WH[1] },{ (float)WH[0], (float)WH[1] } };
    lambda = getPerspectiveTransform(esquinaFloat, esquinasFinales);
    return lambda;
}


int* readWiHe()
{
    static int  Dim[2];
    Mat myDim = Mat::eye(2, 1, CV_64F);
    FileStorage storage2("dim.yml", cv::FileStorage::READ);
    storage2["dim"] >> myDim;
    storage2.release();
    Dim[0] = (int)myDim.at<double>(0, 0);
    Dim[1] = (int)myDim.at<double>(1, 0);
    return Dim;
}

float mayor2float(float x1, float x2)
{
    if (x1 > x2)
        return x1;
    else
        return x2;
}

float distancia2puntos(Point p1, Point p2)
{
    int distancex = (p2.x - p1.x) * (p2.x - p1.x);
    int distancey = (p2.y - p1.y) * (p2.y - p1.y);
    float distance = (sqrt(distancex + distancey) + 0.5);
    return distance;
}


Point* get_esquinas(Mat src, int valueCanny, void*)
{
    Mat src_gray, canny_out;
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;
    static Point esquina[4];

    cvtColor(src, src_gray, CV_BGR2GRAY, 0);
    blur(src_gray, src_gray, Size(3, 3));
    Canny(src_gray, canny_out, valueCanny, valueCanny * 1.4, 3);
    findContours(canny_out, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));

    imshow("Res", canny_out);
    /// Draw contours
    Mat drawing = Mat::zeros(canny_out.size(), CV_8UC3);
    bool a = true;

    Point bordesMAX[4] = { Point(0, 0) , Point(0, drawing.size().height) , Point(drawing.size().width, 0) , Point(drawing.size().width, drawing.size().height) };

    for (int i = 0; i< contours.size(); i++)
    {
        RotatedRect cod;
        cod = minAreaRect(contours[i]);
        //if ((abs(cod.size.width - cod.size.height)<2) && ((cod.size.height > PixCircleValue-3 && cod.size.height < PixCircleValue+3) && (cod.size.width > PixCircleValue-3 && cod.size.width < PixCircleValue+3)))
        //{
            if (a) {
                for (int i = 0; i < 4; i++)
                    esquina[i] = cod.center;
                a = false;
            }
            else {
                for (int i = 0; i < 4; i++)
                    if (distancia2puntos(bordesMAX[i], cod.center)<distancia2puntos(bordesMAX[i], esquina[i]))
                        esquina[i] = cod.center;
            }
        //}
    }

    //cout << esquina[0]<< endl;
    //cout << esquina[1]<< endl;
    //cout << esquina[2]<< endl;
    //cout << esquina[3]<< endl;
    return esquina;
}

void saveMat(string name, Mat src)
{
    FileStorage storage(name+".yml", cv::FileStorage::WRITE);
    storage << name << src;
    storage.release();
}

Mat Camara::Calibrar(Mat Snapshot,int calib_param)
{
    Mat CaliSnapshot;
    Point* Esqui = get_esquinas( Snapshot, calib_param, 0);
    Mat lambda = getHomogenea(Esqui);
    int* MyWiHe = getWiHe(Esqui);
    warpPerspective(Snapshot, CaliSnapshot, lambda, { MyWiHe[0],  MyWiHe[1] });
    return CaliSnapshot;
}

void Camara::Set_camara(int WIDTH, int HEIGHT){
    cam.set(CV_CAP_PROP_FRAME_WIDTH, WIDTH); //1280,640
    cam.set(CV_CAP_PROP_FRAME_HEIGHT, HEIGHT); //720,480
    cam.set(CAP_PROP_AUTOFOCUS, 0); // turn the autofocus off
    while (!cam.isOpened()) {
        std::cout << "Failed to make connection to cam" << std::endl;
        cam.open(0);
    }
}

Mat Camara::Take_picture(){
    Mat pic;
    cam >> pic;
    imshow("eje", pic);
    //pic = imread("tab1.jpg");

    return pic;
}
