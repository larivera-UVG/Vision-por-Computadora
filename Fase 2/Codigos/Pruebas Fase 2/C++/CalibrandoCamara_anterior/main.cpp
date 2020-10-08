#include "mainwindow.h"
#include <QApplication>
#include "opencv2/opencv.hpp"

using namespace cv;

VideoCapture cam2;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    cam2.open(0);

    return a.exec();
}
