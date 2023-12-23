
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QColor>
#include <QPalette>



QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow

{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
public slots:

    void pickColor();
    void updateColor();
    void RgbChanged();
    void RgbToCmyk();
    void RgbToHsv();
    void CmykChanged();
    void HsvChanged();
    void updateSliders();
    void setTextHS1();
    void setTextHS2();
    void setTextHS3();
    void setTextHS4();
    void setTextHS5();
    void setTextHS6();
    void setTextHS7();
    void setTextHS8();
    void setTextHS9();
    void setTextHS10();



private:
    QColor color;
    QPalette palette;

    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
