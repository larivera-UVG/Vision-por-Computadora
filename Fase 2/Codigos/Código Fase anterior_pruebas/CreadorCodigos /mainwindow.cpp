#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "creadorcodbin.h"

using namespace std;
using namespace cv;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_botonCrear_pressed()
{
    QString QSnum = ui->inputNum->text();
    string Snum = QSnum.toStdString();
    if(!QSnum.isEmpty()) {
        int Inum = stoi(Snum);
        Mat Icod = imagenCod(Inum);
        QImage img((const uchar*)Icod.data, Icod.cols, Icod.rows, Icod.step, QImage::Format_Indexed8);
        ui->labelCod->setPixmap(QPixmap::fromImage(img));
        ui->labelCodNum->setText("ID: "+QSnum);
        if (ui->checkGuardar->isChecked())
            imwrite(Snum+".jpg", Icod);
    }
}
