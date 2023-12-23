
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QColorDialog>
#include <cmath>
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    ui->horizontalSlider->setValue(100);
    ui->horizontalSlider_2->setValue(100);
    ui->horizontalSlider_3->setValue(100);

    setTextHS1();
    setTextHS2();
    setTextHS3();

    connect(ui->horizontalSlider, SIGNAL(valueChanged(int)), this, SLOT(setTextHS1()));
    connect(ui->horizontalSlider_2, SIGNAL(valueChanged(int)), this, SLOT(setTextHS2()));
    connect(ui->horizontalSlider_3, SIGNAL(valueChanged(int)), this, SLOT(setTextHS3()));

    connect(ui->lineEdit, SIGNAL(textChanged(QString)), this, SLOT(RgbChanged()));
    connect(ui->lineEdit_2, SIGNAL(textChanged(QString)), this, SLOT(RgbChanged()));
    connect(ui->lineEdit_3, SIGNAL(textChanged(QString)), this, SLOT(RgbChanged()));



    connect(ui->horizontalSlider_4, SIGNAL(valueChanged(int)), this, SLOT(setTextHS4()));
    connect(ui->horizontalSlider_5, SIGNAL(valueChanged(int)), this, SLOT(setTextHS5()));
    connect(ui->horizontalSlider_6, SIGNAL(valueChanged(int)), this, SLOT(setTextHS6()));
    connect(ui->horizontalSlider_7, SIGNAL(valueChanged(int)), this, SLOT(setTextHS7()));

    connect(ui->lineEdit_4, SIGNAL(textChanged(QString)), this, SLOT(CmykChanged()));
    connect(ui->lineEdit_5, SIGNAL(textChanged(QString)), this, SLOT(CmykChanged()));
    connect(ui->lineEdit_6, SIGNAL(textChanged(QString)), this, SLOT(CmykChanged()));
    connect(ui->lineEdit_7, SIGNAL(textChanged(QString)), this, SLOT(CmykChanged()));



    connect(ui->horizontalSlider_8, SIGNAL(valueChanged(int)), this, SLOT(setTextHS8()));
    connect(ui->horizontalSlider_9, SIGNAL(valueChanged(int)), this, SLOT(setTextHS9()));
    connect(ui->horizontalSlider_10, SIGNAL(valueChanged(int)), this, SLOT(setTextHS10()));

    connect(ui->lineEdit_8, SIGNAL(textChanged(QString)), this, SLOT(HsvChanged()));
    connect(ui->lineEdit_9, SIGNAL(textChanged(QString)), this, SLOT(HsvChanged()));
    connect(ui->lineEdit_10, SIGNAL(textChanged(QString)), this, SLOT(HsvChanged()));

    connect(ui->pushButton, SIGNAL(clicked()), this, SLOT(pickColor()));

    RgbChanged();
}

void MainWindow::pickColor(){
    color = QColorDialog::getColor();

    ui->lineEdit->blockSignals(true);
    ui->lineEdit->setText(QString::number(color.red()));
    ui->lineEdit->blockSignals(false);

    ui->lineEdit_2->blockSignals(true);
    ui->lineEdit_2->setText(QString::number(color.green()));
    ui->lineEdit_2->blockSignals(false);


    ui->lineEdit_3->blockSignals(true);
    ui->lineEdit_3->setText(QString::number(color.blue()));
    ui->lineEdit_3->blockSignals(false);

    RgbChanged();
}

void MainWindow::RgbToHsv(){

    double r = (double)ui->lineEdit->text().toInt();
    double g = (double)ui->lineEdit_2->text().toInt();
    double b = (double)ui->lineEdit_3->text().toInt();
    double r1 = r/255;
    double g1 = g/255;
    double b1 = b/255;

    double cMax = std::max(r1, g1);
    cMax = std::max(cMax, b1);
    double cMin = std::min(r1, g1);
    cMin = std::min(cMin, b1);

    double delta = cMax - cMin;

    double h, s, v;

    if (delta == 0){
        h = 0;
    }
    else if(cMax == g1){
        h = 60 * ((b1 - r1)/delta + 2);
    }
    else if (cMax == r1){
        h = 60 * (fmod((g1 - b1)/delta, 6));
    }
    else{
        h = 60 * ((r1 - g1)/delta + 4);
    }

    if (cMax == 0){
        s = 0;
    }
    else{
        s = delta/cMax;
    }

    if (h < 0){
        h = 360 + h;
    }

    v = cMax;


    ui->lineEdit_8->blockSignals(true);
    ui->lineEdit_8->setText(QString::number((int)h));
    ui->lineEdit_8->blockSignals(false);

    ui->lineEdit_9->blockSignals(true);
    ui->lineEdit_9->setText(QString::number((int)(s * 100)));
    ui->lineEdit_9->blockSignals(false);


    ui->lineEdit_10->blockSignals(true);
    ui->lineEdit_10->setText(QString::number((int)(v * 100)));
    ui->lineEdit_10->blockSignals(false);


}

void MainWindow::RgbToCmyk(){
    double c, m, y;
    double k;
    double r = (double)ui->lineEdit->text().toInt();
    double g = (double)ui->lineEdit_2->text().toInt();
    double b = (double)ui->lineEdit_3->text().toInt();
    k = std::min(1 -  r/255, 1 - g/255);
    k = std::min(k, 1 - b/255);
    c = (1 - r/255 - k)/(1 - k);
    m = (1 - g/255 - k)/(1 - k);
    y = (1 - b/255 - k)/(1 - k);

    if (k == 1){
        c = 0;
        m = 0;
        y = 0;
    }

    ui->lineEdit_4->blockSignals(true);
    ui->lineEdit_4->setText(QString::number((int)(c * 100)));
    ui->lineEdit_4->blockSignals(false);


    ui->lineEdit_5->blockSignals(true);
    ui->lineEdit_5->setText(QString::number((int)(m * 100)));
    ui->lineEdit_5->blockSignals(false);


    ui->lineEdit_6->blockSignals(true);
    ui->lineEdit_6->setText(QString::number((int)(y * 100)));
    ui->lineEdit_6->blockSignals(false);


    ui->lineEdit_7->blockSignals(true);
    ui->lineEdit_7->setText(QString::number((int)(k * 100)));
    ui->lineEdit_7->blockSignals(false);

}


void MainWindow::CmykChanged(){
    int r, g, b;
    double c = (double)ui->lineEdit_4->text().toInt();
    double m = (double)ui->lineEdit_5->text().toInt();
    double y = (double)ui->lineEdit_6->text().toInt();
    double k = (double)ui->lineEdit_7->text().toInt();

    r = 255*(1 - c/100)*(1 - k/100);
    g = 255*(1 - m/100)*(1 - k/100);
    b = 255*(1 - y/100)*(1 - k/100);

    ui->lineEdit->blockSignals(true);
    ui->lineEdit->setText(QString::number((int)r));
    ui->lineEdit->blockSignals(false);

    ui->lineEdit_2->blockSignals(true);
    ui->lineEdit_2->setText(QString::number((int)g));
    ui->lineEdit_2->blockSignals(false);


    ui->lineEdit_3->blockSignals(true);
    ui->lineEdit_3->setText(QString::number((int)b));
    ui->lineEdit_3->blockSignals(false);

    RgbToHsv();
    updateColor();
}

void MainWindow::HsvChanged(){
    double r, g, b;
    double h = (double)ui->lineEdit_8->text().toInt();
    double s = (double)ui->lineEdit_9->text().toInt();
    double v = (double)ui->lineEdit_10->text().toInt();

    double s1 = s/100;
    double v1 = v/100;

    double c = v1 * s1;
    double x = c * (1 - std::abs(fmod(h/60, 2) - 1));
    double m = v1 - c;

    double r1, g1, b1;

    if (0 <= h && h < 60 || h == 360){
        r1 = c;
        g1 = x;
        b1 = 0;
    }
    else if(60<= h && h < 120){
        r1 = x;
        g1 = c;
        b1 = 0;
    }
    else if(120<= h && h < 180){
        r1 = 0;
        g1 = c;
        b1 = x;
    }
    else if(180<= h && h < 240){
        r1 = 0;
        g1 = x;
        b1 = c;
    }
    else if(240<= h && h < 300){
        r1 = x;
        g1 = 0;
        b1 = c;
    }
    else if(300<= h && h < 360){
        r1 = c;
        g1 = 0;
        b1 = x;
    }

    r = (r1 + m) * 255;
    g = (g1 + m) * 255;
    b = (b1 + m) * 255;


    ui->lineEdit->blockSignals(true);
    ui->lineEdit->setText(QString::number((int)r));
    ui->lineEdit->blockSignals(false);


    ui->lineEdit_2->blockSignals(true);
    ui->lineEdit_2->setText(QString::number((int)g));
    ui->lineEdit_2->blockSignals(false);


    ui->lineEdit_3->blockSignals(true);
    ui->lineEdit_3->setText(QString::number((int)b));
    ui->lineEdit_3->blockSignals(false);

    RgbToCmyk();
    updateColor();
}

void MainWindow::RgbChanged(){
    RgbToHsv();
    RgbToCmyk();
    updateColor();
}

void MainWindow::updateColor(){
    updateSliders();

    color.setRgb(ui->lineEdit->text().toInt(), ui->lineEdit_2->text().toInt(), ui->lineEdit_3->text().toInt());
    ui->label_15->setText(color.name());
    palette.setColor(QPalette::Window, color);
    ui->label->setAutoFillBackground(true);
    ui->label->setPalette(palette);
}

void MainWindow::setTextHS1(){
    ui->lineEdit->setText(QString::number(ui->horizontalSlider->value()));
}

void MainWindow::setTextHS2(){
    ui->lineEdit_2->setText(QString::number(ui->horizontalSlider_2->value()));
}

void MainWindow::setTextHS3(){
    ui->lineEdit_3->setText(QString::number(ui->horizontalSlider_3->value()));
}

void MainWindow::setTextHS4(){
    ui->lineEdit_4->setText(QString::number(ui->horizontalSlider_4->value()));
}

void MainWindow::setTextHS5(){
    ui->lineEdit_5->setText(QString::number(ui->horizontalSlider_5->value()));
}

void MainWindow::setTextHS6(){
    ui->lineEdit_6->setText(QString::number(ui->horizontalSlider_6->value()));
}

void MainWindow::setTextHS7(){
    ui->lineEdit_7->setText(QString::number(ui->horizontalSlider_7->value()));
}

void MainWindow::setTextHS8(){
    ui->lineEdit_8->setText(QString::number(ui->horizontalSlider_8->value()));
}

void MainWindow::setTextHS9(){
    ui->lineEdit_9->setText(QString::number(ui->horizontalSlider_9->value()));
}

void MainWindow::setTextHS10(){
    ui->lineEdit_10->setText(QString::number(ui->horizontalSlider_10->value()));
}

void MainWindow::updateSliders(){
    ui->horizontalSlider->blockSignals(true);
    ui->horizontalSlider_2->blockSignals(true);
    ui->horizontalSlider_3->blockSignals(true);
    ui->horizontalSlider_4->blockSignals(true);
    ui->horizontalSlider_5->blockSignals(true);
    ui->horizontalSlider_6->blockSignals(true);
    ui->horizontalSlider_7->blockSignals(true);
    ui->horizontalSlider_8->blockSignals(true);
    ui->horizontalSlider_9->blockSignals(true);
    ui->horizontalSlider_10->blockSignals(true);
    ui->horizontalSlider->setValue(ui->lineEdit->text().toInt());
    ui->horizontalSlider_2->setValue(ui->lineEdit_2->text().toInt());
    ui->horizontalSlider_3->setValue(ui->lineEdit_3->text().toInt());
    ui->horizontalSlider_4->setValue(ui->lineEdit_4->text().toInt());
    ui->horizontalSlider_5->setValue(ui->lineEdit_5->text().toInt());
    ui->horizontalSlider_6->setValue(ui->lineEdit_6->text().toInt());
    ui->horizontalSlider_7->setValue(ui->lineEdit_7->text().toInt());
    ui->horizontalSlider_8->setValue(ui->lineEdit_8->text().toInt());
    ui->horizontalSlider_9->setValue(ui->lineEdit_9->text().toInt());
    ui->horizontalSlider_10->setValue(ui->lineEdit_10->text().toInt());
    ui->horizontalSlider->blockSignals(false);
    ui->horizontalSlider_2->blockSignals(false);
    ui->horizontalSlider_3->blockSignals(false);
    ui->horizontalSlider_4->blockSignals(false);
    ui->horizontalSlider_5->blockSignals(false);
    ui->horizontalSlider_6->blockSignals(false);
    ui->horizontalSlider_7->blockSignals(false);
    ui->horizontalSlider_8->blockSignals(false);
    ui->horizontalSlider_9->blockSignals(false);
    ui->horizontalSlider_10->blockSignals(false);
}



MainWindow::~MainWindow()
{
    delete ui;
}





