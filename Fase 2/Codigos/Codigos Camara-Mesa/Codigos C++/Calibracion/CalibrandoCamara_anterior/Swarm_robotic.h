#ifndef SWARM_ROBOTIC_H
#define SWARM_ROBOTIC_H

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
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>

#include <sys/stat.h>
#include <limits.h>
using namespace cv;
using namespace std;


//FUNCIONES ADICIONALES
int * getWiHe(Point* esquina);
Mat getHomogenea(Point* esquina);
int* readWiHe();
float mayor2float(float x1, float x2);
float distancia2puntos(Point p1, Point p2);
Point* get_esquinas(Mat src, int valueCanny, void*);
void saveMat();
string intToBinString(unsigned int val);
Mat imagenCod(int Inum);
int binTxttoint(string a);


//DE TOMA DE POSE


//CLASE CAMARA
class Camara
{
public:
    Mat Calibrar(Mat Snapshot, int calib_param);
    void Set_camara(int WIDTH, int HEIGHT);
    Mat Take_picture();
};


//CLASE ROBOT
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

//CLASE VECTOR ROBOT
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

#endif // SWARM_ROBOTIC_H
