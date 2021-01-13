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
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
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
    QVBoxLayout *verticalLayout_2;
    QHBoxLayout *horizontalLayout;
    QSpacerItem *horizontalSpacer_2;
    QLabel *labelID;
    QLineEdit *inputNum;
    QSpacerItem *horizontalSpacer;
    QPushButton *botonCrear;
    QHBoxLayout *horizontalLayout_2;
    QLabel *labelCod;
    QVBoxLayout *verticalLayout;
    QLabel *labelCodNum;
    QCheckBox *checkGuardar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(407, 418);
        MainWindow->setAutoFillBackground(false);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        centralWidget->setLayoutDirection(Qt::LeftToRight);
        centralWidget->setAutoFillBackground(false);
        verticalLayout_2 = new QVBoxLayout(centralWidget);
        verticalLayout_2->setSpacing(6);
        verticalLayout_2->setContentsMargins(11, 11, 11, 11);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalLayout->setSizeConstraint(QLayout::SetDefaultConstraint);
        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer_2);

        labelID = new QLabel(centralWidget);
        labelID->setObjectName(QString::fromUtf8("labelID"));

        horizontalLayout->addWidget(labelID);

        inputNum = new QLineEdit(centralWidget);
        inputNum->setObjectName(QString::fromUtf8("inputNum"));
        inputNum->setMaxLength(3);

        horizontalLayout->addWidget(inputNum);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);


        verticalLayout_2->addLayout(horizontalLayout);

        botonCrear = new QPushButton(centralWidget);
        botonCrear->setObjectName(QString::fromUtf8("botonCrear"));
        botonCrear->setStyleSheet(QString::fromUtf8("border: 2px solid #222222; \n"
"border-radius: 10px;\n"
"background-color: #9999ff; \n"
"min-width: 80px; \n"
"min-height: 35px; \n"
""));

        verticalLayout_2->addWidget(botonCrear);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        labelCod = new QLabel(centralWidget);
        labelCod->setObjectName(QString::fromUtf8("labelCod"));
        labelCod->setAlignment(Qt::AlignCenter);

        horizontalLayout_2->addWidget(labelCod);


        verticalLayout_2->addLayout(horizontalLayout_2);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setSpacing(6);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        labelCodNum = new QLabel(centralWidget);
        labelCodNum->setObjectName(QString::fromUtf8("labelCodNum"));
        labelCodNum->setAlignment(Qt::AlignCenter);

        verticalLayout->addWidget(labelCodNum);


        verticalLayout_2->addLayout(verticalLayout);

        checkGuardar = new QCheckBox(centralWidget);
        checkGuardar->setObjectName(QString::fromUtf8("checkGuardar"));

        verticalLayout_2->addWidget(checkGuardar);

        MainWindow->setCentralWidget(centralWidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "Creador de codigos", nullptr));
        labelID->setText(QCoreApplication::translate("MainWindow", "ID [0-255]: ", nullptr));
        botonCrear->setText(QCoreApplication::translate("MainWindow", "Crear", nullptr));
        labelCod->setText(QString());
        labelCodNum->setText(QCoreApplication::translate("MainWindow", "ID: ", nullptr));
        checkGuardar->setText(QCoreApplication::translate("MainWindow", "Guardar", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
