#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "tomaposerobots.h"
//#include "vectorrobots.h"
//#include "robot.h"
//#include "creadorcodbin.h"
//#include <iostream>
#include "Swarm_robotic.h"
#include <semaphore.h>
#include <pthread.h> //no funciona en C++
#include <thread>
#include <pthread.h>
#include <unistd.h>
#include <sys/time.h>

//using namespace cv;
//using namespace std;

#define PI 3.14159265
//VideoCapture cam(0);
Camara camara;

Mat takePicture();
//void Set_Camara(int WIDTH, int HEIGHT);
struct timeval ti, tf;
Mat Snap, CropSnap;
double tiempo;
VectorRobots MyRobots;
int MyIteratorRobot, MyInitialRobots = 0;
int MyGlobalCannyInf = 90;
int MyGlobalCannySup = 300;
float MyMedidaCodigoCM = 5.0;
int activate = 0;

//Para mis hilos
#define INIT_VALUE	1
void My_thread1();
//void My_thread2(void *ptr);
sem_t my_semaphore;	// counting semaphore

///
///Definiendo un nuevo hilo
///En este caso el hilo va a procesar y a obtener la pose de los robots
///mediante las mismas funciones ya declaradas en tomarposerobots.h
///

void *My_thread2(void *ptr)
{
    cout<<"entre al hilo" << endl;
    //cout<<"corrida y obtencion de codigo" << endl;
        MyRobots = getRobotCodes(CropSnap, MyGlobalCannyInf, MyGlobalCannySup);
        MyInitialRobots = MyRobots.Vrobots.size();
        cout << "El hilo termino" << endl;
        /*
        cout << "Este es el vector robot" << endl;
        vector<int> a = MyRobots.Vrobots.at(0).get_Pose();
        for(int i=0; i < a.size(); i++)
        std::cout << a.at(i) << ' ';
        //cout << a << endl;
        MyInitialRobots = MyRobots.Vrobots.size();
        cout << "El tama;o del vector de robots" << endl;
        cout << MyInitialRobots << endl;
       */

      pthread_exit(NULL);
}



///Funciones anteriores
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    //ui->tabla_robots->setRowCount(10);
    ui->tabla_robots->setColumnCount(5);
    QStringList horzHeaders;
    horzHeaders<<"ID"<<"IP"<<"X"<<"Y"<<"Theta";
    ui->tabla_robots->setHorizontalHeaderLabels(horzHeaders);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_boton_AceptarVRobots_pressed()
{
//cam.open(0);
}

void MainWindow::on_boton_AceptarCM_pressed()
{
    //Set_camara(960,720);
    QString QSnumCM = ui->Edit_NumCM->text();
    string SnumCM = QSnumCM.toStdString();
    if(!QSnumCM.isEmpty())
    {
        MyMedidaCodigoCM = stof(SnumCM);
        ui->Edit_NumCM->setEnabled(false);
        ui->boton_ObtenerFirst->setEnabled(true);
    }

}

void MainWindow::on_boton_ObtenerFirst_pressed()
{

// yo debo aplicar multi-hilos en esta parte
    camara.Set_camara(960, 720);

    /*
    cam.set(CV_CAP_PROP_FRAME_WIDTH, 960); //1280,640
    cam.set(CV_CAP_PROP_FRAME_HEIGHT, 720); //720,480
    cam.set(CAP_PROP_AUTOFOCUS, 0); // turn the autofocus off
    while (!cam.isOpened()) {
        std::cout << "Failed to make connection to cam" << std::endl;
        cam.open(0);
    }
    */
    cout << "Voy a tomar la foto" << endl;
    gettimeofday(&ti, NULL);   // Instante inicial
    Snap = camara.Take_picture();
    //cout << "Tome la foto" << endl;
    CropSnap = getCroppedSnapshot(Snap); //esto solo se hace la primera vez
    //cout << "foto" << endl;
    //imshow("Cropped", CropSnap);
    //cout << "A obtener el codigo" << endl;
    //esta es la funcion que debo poner en el multi-hilos
    cout << "Abri el hilo" << endl;
    //std::thread thread1(My_thread1);

    pthread_t thread2;
    pthread_create(&thread2, NULL, My_thread2, NULL);
    pthread_join(thread2, NULL);
    gettimeofday(&tf, NULL);   // Instante final
    tiempo = (tf.tv_sec - ti.tv_sec) * 1e6;
    tiempo = (tiempo + (tf.tv_usec - ti.tv_usec)) * 1e-6;
    cout << "Time taken by program is : " << fixed << tiempo << setprecision(6);
    activate = 0;
/*
    MyRobots = getRobotCodes(CropSnap, MyGlobalCannyInf, MyGlobalCannySup);
    cout << "Este es el vector robot" << endl;

    //cout << MyRobots.Vrobots.at(0);
    MyInitialRobots = MyRobots.Vrobots.size();
    cout << "El tama;o del vector de robots" << endl;
    cout << MyInitialRobots << endl;
*/
    if (MyInitialRobots>0)
    {
        Mat Icod = imagenCod(MyRobots.Vrobots.at(0).id);
        imshow("ejemplo", Icod);
        QImage imgCod((const uchar*)Icod.data, Icod.cols, Icod.rows, Icod.step, QImage::Format_Indexed8);
        ui->label_ImgRobot->setPixmap(QPixmap::fromImage(imgCod));
        string MySid = to_string(MyRobots.Vrobots.at(0).id);
        QString MyQSid = QString::fromStdString(MySid);
        ui->label_IdRobot->setText("ID: "+MyQSid);
    }
}

/*
void Set_camara(int WIDTH, int HEIGHT){
    cam.set(CV_CAP_PROP_FRAME_WIDTH, WIDTH); //1280,640
    cam.set(CV_CAP_PROP_FRAME_HEIGHT, HEIGHT); //720,480
    cam.set(CAP_PROP_AUTOFOCUS, 0); // turn the autofocus off
    while (!cam.isOpened()) {
        std::cout << "Failed to make connection to cam" << std::endl;
        cam.open(0);
    }
}
*/

/*
Mat takePicture() {
    Mat pic;
    cam >> pic;
    //pic = imread("P1.png");
    cout << "saliendo de tomar la foto" << endl;
    return pic;
}
*/
