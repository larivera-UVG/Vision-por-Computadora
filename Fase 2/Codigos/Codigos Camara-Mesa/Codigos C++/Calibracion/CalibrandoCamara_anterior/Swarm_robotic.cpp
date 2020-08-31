#include "Swarm_robotic.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include "opencv2/core/persistence.hpp"
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

Point *Esqui;
int* MyWiHe;
Mat lambda;


VideoCapture cam_libreria(0);

//FUNCIONES ADICIONALES PARA LAS CLASES Y OTRAS.
/// nuevas funciones
///
///

int binTxttoint(string a)
{
    int idnum = 0;
    for (int i = 0; i < a.length(); ++i) {
        int n = a[i] - '0';
        idnum = idnum + (pow(2, i)*n);
    }
    return idnum;
}

/// funciones anterioes

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
//Mat lambda;
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

void saveMat()
{
    int counter = 0;
    //int dummy;
            int pipe_BtoA;		// for file descriptors
            int n =0;
                    //dummy = system("mkfifo CalibtoPose");

            cout << lambda << endl;
            Mat dummy = lambda;
            double a = lambda.at<double>(0,0);

            pipe_BtoA = open("/tmp/CalibtoPose", O_WRONLY);

            //Mat dimen = Mat::eye(2, 1, CV_64F);
            int Widht;
            int Height;
            Widht = MyWiHe[0];
            Height = MyWiHe[1];
            cout << Widht <<endl;
            //cout << size_mat << endl;
            if(pipe_BtoA < 0)
            {
                cout << "/tmp/CalibtoPose error" << endl;
                exit(-1);
            }


            while(n < 3)
            {
                cout << n << endl;

                if (n == 0){
                for (int i = 0; i <3; i++){
                    for (int j=0; j < 3; j++){
                sleep(1);
                a = lambda.at<double>(i,j);
                if(write(pipe_BtoA, &a, sizeof(a)) != sizeof(a))
                {
                    cout <<"/tmp/CalibtoPose write error" << endl;;
                    exit(-1);
                }

                    }
                }
               }

             else if (n == 1){
                    //sleep(1);
                if(write(pipe_BtoA, &Widht, sizeof(Widht)) != sizeof(Widht))
                    {
                        cout <<"/tmp/CalibtoPose write error" << endl;;
                        exit(-1);
                    }
                cout << Widht <<endl;
                }

             else if (n == 2){
                    //sleep(1);

                   if(write(pipe_BtoA, &Height, sizeof(Height)) != sizeof(Height))
                       {
                           cout <<"/tmp/CalibtoPose write error" << endl;;
                           exit(-1);
                       }
                       cout << Height <<endl;
                   }

                counter++;
                n++;
            }
     //close(0);
            //cout << lambda << endl;
    /*
    FileStorage storage2("probando.txt", FileStorage::WRITE);
    storage2 << "name" << a;
    storage2.release();


    cout << name << endl;
    FileStorage storage(name+".txt", FileStorage::WRITE);
    storage << "name" << src;
    storage.release();
    */

    FileStorage fs("test.yml", FileStorage::WRITE);
      fs << "frameCount" << 5;
      time_t rawtime; time(&rawtime);
      fs << "calibrationDate" << asctime(localtime(&rawtime));
      Mat cameraMatrix = (Mat_<double>(3,3) << 1000, 0, 320, 0, 1000, 240, 0, 0, 1);
      Mat distCoeffs = (Mat_<double>(5,1) << 0.1, 0.01, -0.001, 0, 0);
      fs << "cameraMatrix" << cameraMatrix << "distCoeffs" << distCoeffs;
      fs << "features" << "[";
      for( int i = 0; i < 3; i++ )
      {
          int x = rand() % 640;
          int y = rand() % 480;
          uchar lbp = rand() % 256;
          fs << "{:" << "x" << x << "y" << y << "lbp" << "[:";
          for( int j = 0; j < 8; j++ )
              fs << ((lbp >> j) & 1);
          fs << "]" << "}";
      }
      fs << "]";
      fs.release();
}
string intToBinString(unsigned int val)
{
    unsigned int mask = 1 << (sizeof(int) * 8 - 1);
    string binString = "";
    for (int i = 0; i < sizeof(int) * 8; i++)
    {
        if ((val & mask) == 0)
            binString = binString + "0";
        else
            binString = binString + "1";
        mask >>= 1;
    }
    return binString;
}

Mat imagenCod(int Inum)
{
    Mat Mcod = Mat::zeros(Size(200, 200), CV_8UC1);

    if ((Inum > 0) && (Inum < 256)) {
        string Snum = intToBinString(Inum);
        string Sbin = Snum.substr(24, 32);
        int u, v, k;

            k = -1;
            for (u = 0; u <= 2; ++u) {
                for (v = 0; v <= 2; ++v) {
                    if (k==-1) ///Pivote
                        Mcod(Range((u * 50 + 25), (u * 50 + 75)), Range((v * 50 + 25), (v * 50 + 75))) = 255;
                    else {
                        char t = Sbin[7-k];
                        int n = t - '0';
                        Mcod(Range((u * 50 + 25), (u * 50 + 75)), Range((v * 50 + 25), (v * 50 + 75))) = n * 125 ;
                    }
                    k++;
                }
            }
    }

    return Mcod;
}

//METODOS CLASE CAMARA
Mat Camara::Calibrar(Mat Snapshot,int calib_param)
{
    Mat CaliSnapshot;
    Point* Esqui = get_esquinas( Snapshot, calib_param, 0);
    lambda = getHomogenea(Esqui);
    MyWiHe = getWiHe(Esqui);
    warpPerspective(Snapshot, CaliSnapshot, lambda, { MyWiHe[0],  MyWiHe[1] });
    return CaliSnapshot;
}

void Camara::Set_camara(int WIDTH, int HEIGHT){
    cam_libreria.set(CV_CAP_PROP_FRAME_WIDTH, WIDTH); //1280,640
    cam_libreria.set(CV_CAP_PROP_FRAME_HEIGHT, HEIGHT); //720,480
    cam_libreria.set(CAP_PROP_AUTOFOCUS, 0); // turn the autofocus off
    while (!cam_libreria.isOpened()) {
        std::cout << "Failed to make connection to cam" << std::endl;
        cam_libreria.open(0);
    }
}

Mat Camara::Take_picture(){
    Mat pic;
    cam_libreria >> pic;
    imshow("eje", pic);
    //pic = imread("tab1.jpg");

    return pic;
}


//CLASE ROBOT
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


//CLASE VECTOR ROBOT

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
