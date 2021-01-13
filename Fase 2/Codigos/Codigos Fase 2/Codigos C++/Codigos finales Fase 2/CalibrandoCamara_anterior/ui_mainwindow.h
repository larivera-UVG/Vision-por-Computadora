/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.14.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *topHorizontalLayout;
    QSpacerItem *horizontalSpacer_2;
    QPushButton *botonTomar;
    QSpacerItem *horizontalSpacer_4;
    QSpacerItem *horizontalSpacer;
    QPushButton *botonCalibrar;
    QSpacerItem *horizontalSpacer_3;
    QHBoxLayout *horizontalLayout_2;
    QLabel *label_ori;
    QLabel *label_cali;
    QHBoxLayout *horizontalLayout;
    QSpacerItem *horizontalSpacer_6;
    QPushButton *botonGuardar;
    QSpacerItem *horizontalSpacer_5;
    QSpacerItem *horizontalSpacer_7;
    QLabel *label;
    QSpacerItem *horizontalSpacer_8;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(1050, 497);
        MainWindow->setStyleSheet(QString::fromUtf8(""));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        verticalLayout = new QVBoxLayout(centralWidget);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        topHorizontalLayout = new QHBoxLayout();
        topHorizontalLayout->setSpacing(6);
        topHorizontalLayout->setObjectName(QString::fromUtf8("topHorizontalLayout"));
        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        topHorizontalLayout->addItem(horizontalSpacer_2);

        botonTomar = new QPushButton(centralWidget);
        botonTomar->setObjectName(QString::fromUtf8("botonTomar"));
        botonTomar->setStyleSheet(QString::fromUtf8(""));

        topHorizontalLayout->addWidget(botonTomar);

        horizontalSpacer_4 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        topHorizontalLayout->addItem(horizontalSpacer_4);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        topHorizontalLayout->addItem(horizontalSpacer);

        botonCalibrar = new QPushButton(centralWidget);
        botonCalibrar->setObjectName(QString::fromUtf8("botonCalibrar"));
        botonCalibrar->setStyleSheet(QString::fromUtf8(""));

        topHorizontalLayout->addWidget(botonCalibrar);

        horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        topHorizontalLayout->addItem(horizontalSpacer_3);


        verticalLayout->addLayout(topHorizontalLayout);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        label_ori = new QLabel(centralWidget);
        label_ori->setObjectName(QString::fromUtf8("label_ori"));
        label_ori->setLineWidth(1);
        label_ori->setAlignment(Qt::AlignCenter);

        horizontalLayout_2->addWidget(label_ori);

        label_cali = new QLabel(centralWidget);
        label_cali->setObjectName(QString::fromUtf8("label_cali"));
        label_cali->setAlignment(Qt::AlignCenter);

        horizontalLayout_2->addWidget(label_cali);


        verticalLayout->addLayout(horizontalLayout_2);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalSpacer_6 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer_6);

        botonGuardar = new QPushButton(centralWidget);
        botonGuardar->setObjectName(QString::fromUtf8("botonGuardar"));
        botonGuardar->setStyleSheet(QString::fromUtf8(""));

        horizontalLayout->addWidget(botonGuardar);

        horizontalSpacer_5 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer_5);

        horizontalSpacer_7 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer_7);

        label = new QLabel(centralWidget);
        label->setObjectName(QString::fromUtf8("label"));

        horizontalLayout->addWidget(label);

        horizontalSpacer_8 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer_8);


        verticalLayout->addLayout(horizontalLayout);

        MainWindow->setCentralWidget(centralWidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "Calibrador de Tablero", nullptr));
        botonTomar->setText(QCoreApplication::translate("MainWindow", "Tomar Foto", nullptr));
        botonCalibrar->setText(QCoreApplication::translate("MainWindow", "Calibrar", nullptr));
        label_ori->setText(QCoreApplication::translate("MainWindow", "Im\303\241gen Captura", nullptr));
        label_cali->setText(QCoreApplication::translate("MainWindow", "Im\303\241gen Calibrada", nullptr));
        botonGuardar->setText(QCoreApplication::translate("MainWindow", " Guardar Calibraci\303\263n ", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "Nota: Volver a calibrar hasta que se ocupe las esquinas del tablero", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
