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

//using namespace cv;
//using namespace std;

#define PI 3.14159265
//VideoCapture cam(0);
Camara camara;

Mat takePicture();
//void Set_Camara(int WIDTH, int HEIGHT);

Mat Snap, CropSnap;
VectorRobots MyRobots;
int MyIteratorRobot, MyInitialRobots = 0;
int MyGlobalCannyInf = 100;
int MyGlobalCannySup = 380;
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

void My_thread1()
{
    cout<<"entre al hilo" << endl;
    while(1) {
    cout<<"corrida y obtencion de codigo" << endl;
        MyRobots = getRobotCodes(CropSnap, MyGlobalCannyInf, MyGlobalCannySup);
        cout << "Este es el vector robot" << endl;

        //cout << MyRobots.Vrobots.at(0);
        MyInitialRobots = MyRobots.Vrobots.size();
        cout << "El tama;o del vector de robots" << endl;
        cout << MyInitialRobots << endl;
    //
     sleep(1);
    }

    //pthread_exit(0);
}

void *My_thread2(void *ptr)
{
    cout<<"entre al hilo" << endl;
    while(1) {
    cout<<"corrida y obtencion de codigo" << endl;
        MyRobots = getRobotCodes(CropSnap, MyGlobalCannyInf, MyGlobalCannySup);
        cout << "Este es el vector robot" << endl;

        //cout << MyRobots.Vrobots.at(0);
        MyInitialRobots = MyRobots.Vrobots.size();
        cout << "El tama;o del vector de robots" << endl;
        cout << MyInitialRobots << endl;
    //
    sleep(2);
    }

    //pthread_exit(0);
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
    Snap = camara.Take_picture();
    cout << "Tome la foto" << endl;
    CropSnap = getCroppedSnapshot(Snap); //esto solo se hace la primera vez
    cout << "foto" << endl;
    //imshow("Cropped", CropSnap);
    cout << "A obtener el codigo" << endl;
    //esta es la funcion que debo poner en el multi-hilos
    cout << "Abri el hilo" << endl;
    //std::thread thread1(My_thread1);

    if (activate == 0){
    pthread_t thread2;
    pthread_create(&thread2, NULL, My_thread2, NULL);
    activate = 1;
    }
    //thread1.join();

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
        imshow("ejempo", Icod);
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
