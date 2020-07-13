#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "calibracam.h"
#include <QPixmap>

/*
 * Codigo actualizado al dia 15 de junio de 2020 por Jose Pablo Guerra
 * Se agregan los comentarios pertinentes, ya que el codigo original no esta comentado
 */

using namespace cv; //para utilizar los elementos de opencv, como VideoCapture
using namespace std;

VideoCapture cam; //Crea el objeto de la camara.
Mat Snapshot, CaliSnapshot;
Point *Esqui;
int* MyWiHe;
Mat lambda;

void setCam(); //una funcion de set para la camara, no se usa en ninguna parte del codigo
Mat takePicture(); //Aqui se accede a tomar fotografia.

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    loadSettings();
    cam.open(0);
    //setCam();
    ui->botonCalibrar->setEnabled(false);
    ui->botonGuardar->setEnabled(false);
}

MainWindow::~MainWindow()
{
    delete ui;
}



void MainWindow::on_botonCalibrar_pressed()
{
    imshow("Output Image", Snapshot);
    Esqui = get_esquinas(Snapshot, 100, 0);
    lambda = getHomogenea(Esqui);
    MyWiHe = getWiHe(Esqui);
    cv::warpPerspective(Snapshot, CaliSnapshot, lambda, { MyWiHe[0],  MyWiHe[1] });
    imwrite("calisnap.jpg",CaliSnapshot);
    QImage img((const uchar*)CaliSnapshot.data, CaliSnapshot.cols, CaliSnapshot.rows, CaliSnapshot.step, QImage::Format_RGB888);
    QPixmap pixmap = QPixmap::fromImage(img.rgbSwapped());
    ui->label_cali->setPixmap(pixmap.scaled(ui->label_ori->width(),ui->label_ori->height(),Qt::KeepAspectRatio));
    ui->botonGuardar->setEnabled(true);
}

void MainWindow::closeEvent(QCloseEvent *event)
{
   /* int result = QMessageBox::warning(this, "Exit", "Are you sure you want to close this program?", QMessageBox::Yes, QMessageBox::No);
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
    ui->botonCalibrar->setEnabled(true);
    Snapshot = takePicture();
    QImage img((const uchar*)Snapshot.data, Snapshot.cols, Snapshot.rows, Snapshot.step, QImage::Format_RGB888);
    QPixmap pixmap = QPixmap::fromImage(img.rgbSwapped());
    ui->label_ori->setPixmap(pixmap.scaled(ui->label_ori->width(),ui->label_ori->height(),Qt::KeepAspectRatio));
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

    /*
     * Aqui es donde esta el error. Al menos en estas primeras pruebas
     * Lo que hace la linea anterior es leer un archivo que ya existe, resulta
     * que al no tener este archivo, el pixmap estaba como null.
     *
     * Lo que se hizo para arreglarlo es descomentar la parte de capturar la imagen
     * (las dos lineas antes)
     * Esto realiza una captura en tiempo real y ya activa el boton de calibrar y las otras opciones.
     *
     * Solucion encontrada al 15 de junio del 2020.
     *
     */

    return pic;
}

