#include "mainwindow.h"
#include "opencv2/opencv.hpp"
#include <QApplication>
#include <iostream>

using namespace cv;
using namespace std;


VideoCapture cam(0);

int main(int argc, char *argv[])
{
//    QApplication a(argc, argv);
//    MainWindow w;
//    w.show();
    while(1){
        Mat frame;
        // Capture frame-by-frame
        cam >> frame;
        // If the frame is empty, break immediately
        if (frame.empty())
          break;
        // Display the resulting frame
        imshow( "Frame", frame );
        // Press  ESC on keyboard to exit
        char c=(char)waitKey(25);
        if(c==27)
          break;
      }

   // return a.exec();
    return 0;
}
