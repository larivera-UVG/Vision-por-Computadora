#ifndef CALIBRACION_CAM_H
#define CALIBRACION_CAM_H

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
#include "opencv2/opencv.hpp"

using namespace cv;
using namespace std;

int * getWiHe(Point* esquina);
Mat getHomogenea(Point* esquina);
int* readWiHe();
float mayor2float(float x1, float x2);
float distancia2puntos(Point p1, Point p2);
Point* get_esquinas(Mat src, int valueCanny, void*);
void saveMat(string name,Mat src);


//int PixCircleValue = 10;

class Camara
{
public:
    Mat Calibrar(Mat Snapshot, int calib_param);
    void Set_camara(int WIDTH, int HEIGHT);
    Mat Take_picture();
};

#endif // CALIBRACION_CAM_H
