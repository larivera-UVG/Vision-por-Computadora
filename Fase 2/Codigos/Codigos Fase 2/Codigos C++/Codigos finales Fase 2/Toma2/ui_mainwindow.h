/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.15.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTableWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QVBoxLayout *verticalLayout_2;
    QFormLayout *formLayout;
    QLabel *label_Obtencion;
    QVBoxLayout *verticalLayout;
    QLabel *label_TamCod;
    QLineEdit *Edit_NumCM;
    QPushButton *boton_AceptarCM;
    QPushButton *boton_ObtenerFirst;
    QGroupBox *groupBox_3;
    QVBoxLayout *verticalLayout_6;
    QHBoxLayout *horizontalLayout_2;
    QLabel *label_ImgRobot;
    QLabel *label_IdRobot;
    QHBoxLayout *horizontalLayout;
    QVBoxLayout *verticalLayout_3;
    QPushButton *boton_AceptarRobot;
    QPushButton *boton_BorrarRobot;
    QVBoxLayout *verticalLayout_4;
    QPushButton *boton_AceptarVRobots;
    QPushButton *boton_CancelarRobots;
    QLabel *label_ObtencionIPs;
    QPushButton *boton_ObtenerIPs;
    QGroupBox *groupBox_2;
    QVBoxLayout *verticalLayout_5;
    QTableWidget *tabla_robots;
    QLabel *label_Poses;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(730, 792);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        verticalLayout_2 = new QVBoxLayout(centralWidget);
        verticalLayout_2->setSpacing(6);
        verticalLayout_2->setContentsMargins(11, 11, 11, 11);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        formLayout = new QFormLayout();
        formLayout->setSpacing(6);
        formLayout->setObjectName(QString::fromUtf8("formLayout"));
        label_Obtencion = new QLabel(centralWidget);
        label_Obtencion->setObjectName(QString::fromUtf8("label_Obtencion"));
        QFont font;
        font.setBold(true);
        font.setWeight(75);
        label_Obtencion->setFont(font);

        formLayout->setWidget(0, QFormLayout::LabelRole, label_Obtencion);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setSpacing(6);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        label_TamCod = new QLabel(centralWidget);
        label_TamCod->setObjectName(QString::fromUtf8("label_TamCod"));
        label_TamCod->setMaximumSize(QSize(16777215, 10));
        QFont font1;
        font1.setPointSize(7);
        label_TamCod->setFont(font1);
        label_TamCod->setAlignment(Qt::AlignCenter);

        verticalLayout->addWidget(label_TamCod);

        Edit_NumCM = new QLineEdit(centralWidget);
        Edit_NumCM->setObjectName(QString::fromUtf8("Edit_NumCM"));

        verticalLayout->addWidget(Edit_NumCM);

        boton_AceptarCM = new QPushButton(centralWidget);
        boton_AceptarCM->setObjectName(QString::fromUtf8("boton_AceptarCM"));

        verticalLayout->addWidget(boton_AceptarCM);

        boton_ObtenerFirst = new QPushButton(centralWidget);
        boton_ObtenerFirst->setObjectName(QString::fromUtf8("boton_ObtenerFirst"));
        boton_ObtenerFirst->setEnabled(false);

        verticalLayout->addWidget(boton_ObtenerFirst);


        formLayout->setLayout(1, QFormLayout::LabelRole, verticalLayout);

        groupBox_3 = new QGroupBox(centralWidget);
        groupBox_3->setObjectName(QString::fromUtf8("groupBox_3"));
        QFont font2;
        font2.setBold(false);
        font2.setWeight(50);
        groupBox_3->setFont(font2);
        verticalLayout_6 = new QVBoxLayout(groupBox_3);
        verticalLayout_6->setSpacing(6);
        verticalLayout_6->setContentsMargins(11, 11, 11, 11);
        verticalLayout_6->setObjectName(QString::fromUtf8("verticalLayout_6"));
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        label_ImgRobot = new QLabel(groupBox_3);
        label_ImgRobot->setObjectName(QString::fromUtf8("label_ImgRobot"));
        label_ImgRobot->setMinimumSize(QSize(200, 200));
        label_ImgRobot->setAlignment(Qt::AlignCenter);

        horizontalLayout_2->addWidget(label_ImgRobot);

        label_IdRobot = new QLabel(groupBox_3);
        label_IdRobot->setObjectName(QString::fromUtf8("label_IdRobot"));
        label_IdRobot->setMaximumSize(QSize(50, 16777215));
        label_IdRobot->setAlignment(Qt::AlignCenter);

        horizontalLayout_2->addWidget(label_IdRobot);


        verticalLayout_6->addLayout(horizontalLayout_2);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        verticalLayout_3 = new QVBoxLayout();
        verticalLayout_3->setSpacing(6);
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        boton_AceptarRobot = new QPushButton(groupBox_3);
        boton_AceptarRobot->setObjectName(QString::fromUtf8("boton_AceptarRobot"));
        boton_AceptarRobot->setEnabled(false);

        verticalLayout_3->addWidget(boton_AceptarRobot);

        boton_BorrarRobot = new QPushButton(groupBox_3);
        boton_BorrarRobot->setObjectName(QString::fromUtf8("boton_BorrarRobot"));
        boton_BorrarRobot->setEnabled(false);

        verticalLayout_3->addWidget(boton_BorrarRobot);


        horizontalLayout->addLayout(verticalLayout_3);

        verticalLayout_4 = new QVBoxLayout();
        verticalLayout_4->setSpacing(6);
        verticalLayout_4->setObjectName(QString::fromUtf8("verticalLayout_4"));
        boton_AceptarVRobots = new QPushButton(groupBox_3);
        boton_AceptarVRobots->setObjectName(QString::fromUtf8("boton_AceptarVRobots"));
        boton_AceptarVRobots->setEnabled(false);

        verticalLayout_4->addWidget(boton_AceptarVRobots);

        boton_CancelarRobots = new QPushButton(groupBox_3);
        boton_CancelarRobots->setObjectName(QString::fromUtf8("boton_CancelarRobots"));
        boton_CancelarRobots->setEnabled(false);

        verticalLayout_4->addWidget(boton_CancelarRobots);


        horizontalLayout->addLayout(verticalLayout_4);


        verticalLayout_6->addLayout(horizontalLayout);


        formLayout->setWidget(1, QFormLayout::FieldRole, groupBox_3);

        label_ObtencionIPs = new QLabel(centralWidget);
        label_ObtencionIPs->setObjectName(QString::fromUtf8("label_ObtencionIPs"));
        label_ObtencionIPs->setFont(font);

        formLayout->setWidget(2, QFormLayout::LabelRole, label_ObtencionIPs);

        boton_ObtenerIPs = new QPushButton(centralWidget);
        boton_ObtenerIPs->setObjectName(QString::fromUtf8("boton_ObtenerIPs"));
        boton_ObtenerIPs->setEnabled(false);

        formLayout->setWidget(3, QFormLayout::LabelRole, boton_ObtenerIPs);

        groupBox_2 = new QGroupBox(centralWidget);
        groupBox_2->setObjectName(QString::fromUtf8("groupBox_2"));
        verticalLayout_5 = new QVBoxLayout(groupBox_2);
        verticalLayout_5->setSpacing(6);
        verticalLayout_5->setContentsMargins(11, 11, 11, 11);
        verticalLayout_5->setObjectName(QString::fromUtf8("verticalLayout_5"));
        tabla_robots = new QTableWidget(groupBox_2);
        tabla_robots->setObjectName(QString::fromUtf8("tabla_robots"));
        tabla_robots->setFont(font1);
        tabla_robots->horizontalHeader()->setDefaultSectionSize(100);

        verticalLayout_5->addWidget(tabla_robots);


        formLayout->setWidget(3, QFormLayout::FieldRole, groupBox_2);

        label_Poses = new QLabel(centralWidget);
        label_Poses->setObjectName(QString::fromUtf8("label_Poses"));

        formLayout->setWidget(4, QFormLayout::LabelRole, label_Poses);


        verticalLayout_2->addLayout(formLayout);

        MainWindow->setCentralWidget(centralWidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        label_Obtencion->setText(QCoreApplication::translate("MainWindow", "Obtencion de robots", nullptr));
        label_TamCod->setText(QCoreApplication::translate("MainWindow", "Tama\303\261o de codigos [cm]", nullptr));
        boton_AceptarCM->setText(QCoreApplication::translate("MainWindow", "Aceptar", nullptr));
        boton_ObtenerFirst->setText(QCoreApplication::translate("MainWindow", "Obtener robots", nullptr));
        groupBox_3->setTitle(QCoreApplication::translate("MainWindow", "Robot", nullptr));
        label_ImgRobot->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_IdRobot->setText(QCoreApplication::translate("MainWindow", "ID: 255", nullptr));
        boton_AceptarRobot->setText(QCoreApplication::translate("MainWindow", "Aceptar Robot", nullptr));
        boton_BorrarRobot->setText(QCoreApplication::translate("MainWindow", "Borrar Robot", nullptr));
        boton_AceptarVRobots->setText(QCoreApplication::translate("MainWindow", "Aceptar configuracion", nullptr));
        boton_CancelarRobots->setText(QCoreApplication::translate("MainWindow", "Cancelar configuracion", nullptr));
        label_ObtencionIPs->setText(QCoreApplication::translate("MainWindow", "Obtencion de IPs", nullptr));
        boton_ObtenerIPs->setText(QCoreApplication::translate("MainWindow", "Obtener IPs", nullptr));
        groupBox_2->setTitle(QCoreApplication::translate("MainWindow", "Tabla de robots", nullptr));
        label_Poses->setText(QCoreApplication::translate("MainWindow", "Poses de robots", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
