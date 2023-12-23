
#include "mainwindow.h"
//#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
 //   , ui(new Ui::MainWindow)
{
//    ui->setupUi(this);
    resize(1000, 540);
    KWidget* kwidget = new KWidget();
    setCentralWidget(kwidget);
}

MainWindow::~MainWindow()
{
//    delete ui;
}


