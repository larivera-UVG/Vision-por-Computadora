#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "calibracam.h"
#include <QPixmap>
/*
 * Revision al 26 de junio de 2020
 * Se realiza una captura con mi mesa de pruebas de manera exitosa, la calibracion esta en un 70% correcta
 * Se debe consultar con Andre una explicacion del codigo para entender como funciona la calibracion
 *
 * De momento, se toma un parametro en el boton calibracion que ajusta la manera en como se calibra la imagen.
 *
 *
*/

using namespace cv;
using namespace std;

#define Calib_param 8

VideoCapture cam(0);
Mat Snapshot, CaliSnapshot;
Point *Esqui;
int* MyWiHe;
Mat lambda;

void setCam();
Mat takePicture();

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    loadSettings();
    setCam();
    ui->botonCalibrar->setEnabled(false);
    ui->botonGuardar->setEnabled(false);
}

MainWindow::~MainWindow()
{
    delete ui;
}



void MainWindow::on_botonCalibrar_pressed()
{

    Esqui = get_esquinas(Snapshot, Calib_param, 0);
    lambda = getHomogenea(Esqui);
    MyWiHe = getWiHe(Esqui);
    cv::warpPerspective(Snapshot, CaliSnapshot, lambda, { MyWiHe[0],  MyWiHe[1] });
    imshow("Output Image", CaliSnapshot);
    //imwrite("calisnap.jpg",CaliSnapshot);
    QImage img((const uchar*)CaliSnapshot.data, CaliSnapshot.cols, CaliSnapshot.rows, CaliSnapshot.step, QImage::Format_RGB888);
    QPixmap pixmap = QPixmap::fromImage(img.rgbSwapped());
    //imshow("Output Image", CaliSnapshot);
    ui->label_cali->setPixmap(pixmap.scaled(ui->label_ori->width(),ui->label_ori->height(),Qt::KeepAspectRatio));
    ui->botonGuardar->setEnabled(true);
}

void MainWindow::closeEvent(QCloseEvent *event)
{
    /*int result = QMessageBox::warning(this, "Exit", "Are you sure you want to close this program?", QMessageBox::Yes, QMessageBox::No);
    if(result == QMessageBox::Yes)
    {
        saveSettings();
        event->accept();
    }
    else
    {
        event->ignore();
    }*/
}

void MainWindow::loadSettings()
{
    QSettings settings("Packt", "Hello_OpenCV_Qt", this);
}

void MainWindow::saveSettings()
{
    QSettings settings("Packt", "Hello_OpenCV_Qt", this);
}

void MainWindow::on_botonTomar_pressed()
{

    Snapshot = takePicture();
    QImage img((const uchar*)Snapshot.data, Snapshot.cols, Snapshot.rows, Snapshot.step, QImage::Format_RGB888);
    QPixmap pixmap = QPixmap::fromImage(img.rgbSwapped());
    ui->label_ori->setPixmap(pixmap.scaled(ui->label_ori->width(),ui->label_ori->height(),Qt::KeepAspectRatio));
    ui->botonCalibrar->setEnabled(true);
    ui->label_cali->clear();
}

void MainWindow::on_botonGuardar_pressed()
{
    saveMat("homogenea",lambda);
    Mat dimen = Mat::eye(2, 1, CV_64F);
    dimen.at<double>(0, 0) = MyWiHe[0];
    dimen.at<double>(1, 0) = MyWiHe[1];
    saveMat("dim",dimen);

    ui->botonCalibrar->setEnabled(false);
    ui->botonGuardar->setEnabled(false);

}

void setCam() {
    cam.set(CV_CAP_PROP_FRAME_WIDTH, 960); //1280,640
    cam.set(CV_CAP_PROP_FRAME_HEIGHT, 720); //720,480
    cam.set(CAP_PROP_AUTOFOCUS, 0); // turn the autofocus off
    while (!cam.isOpened()) {
        std::cout << "Failed to make connection to cam" << std::endl;
        cam.open(0);
    }
}

Mat takePicture() {
    Mat pic;


    cam >> pic;
    imshow("eje", pic);
    //pic = imread("tab1.jpg");

    return pic;
}


