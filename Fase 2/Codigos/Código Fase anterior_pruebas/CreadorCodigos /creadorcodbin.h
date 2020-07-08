#ifndef CREADORCODBIN_H
#define CREADORCODBIN_H

#include <QMainWindow>
#include <QFileDialog>
#include <QDir>
#include <QFile>
#include <QCloseEvent>
#include <QMessageBox>
#include <QSettings>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include "opencv2/opencv.hpp"

using namespace cv;
using namespace std;

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
    QMessageBox msgBox;
    msgBox.setText("ERROR: Ingresar valores entre 1 a 255.");

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
    } else
        msgBox.exec();
    return Mcod;
}

#endif // CREADORCODBIN_H
