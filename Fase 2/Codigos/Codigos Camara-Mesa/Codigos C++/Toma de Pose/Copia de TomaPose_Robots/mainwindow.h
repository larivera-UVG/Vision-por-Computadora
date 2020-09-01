#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QFileDialog>
#include <QDir>
#include <QFile>
#include <QCloseEvent>
#include <QMessageBox>
#include <QSettings>
//#include "opencv2/opencv.hpp"

namespace Ui {
class MainWindow;

}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_boton_AceptarVRobots_pressed();

    void on_boton_AceptarCM_pressed();

    void on_boton_ObtenerFirst_pressed();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
