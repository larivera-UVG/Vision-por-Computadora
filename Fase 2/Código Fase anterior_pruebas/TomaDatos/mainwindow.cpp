#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "tomaposerobots.h"
#include "vectorrobots.h"
#include "robot.h"
#include "creadorcodbin.h"

using namespace cv;
using namespace std;

#define PI 3.14159265

Mat takePicture();

Mat Snap, CropSnap;
VectorRobots MyRobots;
int MyIteratorRobot, MyInitialRobots = 0;
int MyGlobalCannyInf = 94;
int MyGlobalCannySup = 350;
float MyMedidaCodigoCM = 5.0;

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

}

void MainWindow::on_boton_AceptarCM_pressed()
{
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
    Snap = takePicture();
    CropSnap = getCroppedSnapshot(Snap);
    MyRobots = getRobotCodes(CropSnap, MyGlobalCannyInf, MyGlobalCannySup, MyMedidaCodigoCM);
    MyInitialRobots = MyRobots.Vrobots.size();
    if (MyInitialRobots>0)
    {
        Mat Icod = imagenCod(MyRobots.Vrobots.at(0).id);
        //imshow("ejempo", Icod);
        //QImage imgCod((const uchar*)Icod.data, Icod.cols, Icod.rows, Icod.step, QImage::Format_Indexed8);
        //ui->label_ImgRobot->setPixmap(QPixmap::fromImage(imgCod));
        //string MySid = to_string(MyRobots.Vrobots.at(0).id);
        //QString MyQSid = QString::fromStdString(MySid);
        //ui->label_IdRobot->setText("ID: "+MyQSid);
    }
}


Mat takePicture() {
    Mat pic;
    pic = imread("p1.jpg");
    return pic;
}
