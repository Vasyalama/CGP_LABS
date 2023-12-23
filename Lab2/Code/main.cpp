
#include "mainwindow.h"

#include <QApplication>


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    QFont font("Times");
    font.setPointSize(10);
//    font.setStyleHint(QFont::Monospace);
    QApplication::setFont(font);
    w.show();
    return a.exec();
}
