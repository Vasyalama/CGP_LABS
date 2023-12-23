
#include "kwidget.h"
#include <QDir>
#include <QImageWriter>
#include <QString>
#include <QFileDialog>
#include <QTableWidget>
#include <QHeaderView>
#include <QAbstractItemView>

KWidget::KWidget(QWidget *parent)
    : QWidget{parent}
{
    setMinimumSize(1000, 540);
    model = new QFileSystemModel();
    model->setFilter(QDir::QDir::AllEntries);
    model->setRootPath("");
    list = new QListView();
    list->setMinimumSize(500,500);
    list->setMaximumWidth(500);
    list->setModel(model);
    connect(list, SIGNAL(doubleClicked(QModelIndex)), this, SLOT(onListDoubleClicked(QModelIndex)));
    connect(list, SIGNAL(clicked(QModelIndex)), this, SLOT(onListClicked(QModelIndex)));


    grid = new QGridLayout(this);
    grid->addWidget(list, 0 ,0);

    namelb = new QLabel("Название файла: ");
    namelb->setMinimumSize(200,50);

    sizelb = new QLabel("Разрешение: ");
    sizelb->setMinimumSize(200,50);
    dpilb = new QLabel("dpi: ");
    dpilb->setMinimumSize(200,50);
    colorDepthlb = new QLabel("Глубина цвета: ");
    colorDepthlb->setMinimumSize(200,50);
    compressionlb = new QLabel("Сжатие: ");
    compressionlb->setMinimumSize(200,50);

    name = new QLabel("x");
    name->setMinimumSize(200,50);
    size = new QLabel("x");
    size->setMinimumSize(200,50);
    dpi = new QLabel("x");
    dpi->setMinimumSize(200,50);
    colorDepth = new QLabel("x");
    colorDepth->setMinimumSize(200,50);
    compression = new QLabel("x");
    compression->setMinimumSize(200,50);

    vBox = new QVBoxLayout();
    QGridLayout* subGrid = new QGridLayout();
    subGrid->addWidget(namelb, 0, 0);
    subGrid->addWidget(name, 0, 1);
    subGrid->addWidget(sizelb, 1, 0);
    subGrid->addWidget(size, 1, 1);
    subGrid->addWidget(dpilb, 2, 0);
    subGrid->addWidget(dpi, 2, 1);
    subGrid->addWidget(colorDepthlb, 3, 0);
    subGrid->addWidget(colorDepth, 3, 1);
    subGrid->addWidget(compressionlb, 4, 0);
    subGrid->addWidget(compression, 4, 1);

    vBox->addLayout(subGrid);



    button = new QPushButton("Сравнить несколько файлов");
    connect(button, SIGNAL(pressed()), this, SLOT(onMultiButtonPressed()));
    button->setMinimumSize(300,100);
    vBox->addWidget(button, Qt::AlignCenter);
    grid->addLayout(vBox, 0, 1);



    setLayout(grid);

}

void KWidget::onListDoubleClicked(const QModelIndex& index){
    QFileInfo fileInfo = model->fileInfo(index);
    if (fileInfo.fileName() == ".."){
        QDir dir = fileInfo.dir();
        dir.cdUp();
        list->setRootIndex(model->index(dir.absolutePath()));

    }
    else if (fileInfo.fileName() == "."){
        list->setRootIndex(model->index(""));

    }
    else if (fileInfo.isDir()){
        list->setRootIndex(index);
    }

}

void KWidget::onListClicked(const QModelIndex& index){
    QFileInfo fileInfo = model->fileInfo(index);
    QString fileName = fileInfo.fileName();
    QString extention = fileName.remove(0, fileName.length() - 3);
    extention = extention.toLower();

    if (extention == "jpg" || extention == "gif" ||
        extention == "tif" || extention == "bmp" ||
        extention == "png" || extention == "pcx"){
        QImage img (model->filePath(index));
        QImageWriter k (model->filePath(index));
        name->setText(fileInfo.fileName());
        size->setText(QString::number(img.size().width()) + "x" + QString::number(img.size().height()));
        dpi->setText(QString::number(img.physicalDpiX()));
        colorDepth->setText(QString::number(img.bitPlaneCount()));
        if (k.compression() == -1){
            compression->setText("No compression");
        }
        else{
            compression->setText(QString::number(k.compression()));
        }

    }
}

void KWidget::onMultiButtonPressed(){
    QFileDialog* fileDialog = new QFileDialog();
    fileDialog->setWindowTitle("Выберите файлы");
    QList<QUrl> lst = fileDialog->getOpenFileUrls();
    QDialog* dialog = new QDialog();
    dialog->setWindowTitle("Свойства файлов");
    dialog->setMinimumSize(750,500);
    QGridLayout* gridLayout = new QGridLayout(dialog);
    QTableWidget* table = new QTableWidget(dialog);
    gridLayout->addWidget(table);
    table->setColumnCount(5);
    table->setEditTriggers(QAbstractItemView::NoEditTriggers);
    table->setRowCount(lst.size());
    table->setHorizontalHeaderItem(0, new QTableWidgetItem("Имя файла"));
    table->setHorizontalHeaderItem(1, new QTableWidgetItem("Разрешение"));
    table->setHorizontalHeaderItem(2, new QTableWidgetItem("dpi"));
    table->setHorizontalHeaderItem(3, new QTableWidgetItem("Глубина цвета"));
    table->setHorizontalHeaderItem(4, new QTableWidgetItem("Сжатие"));
    table->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);

    for (int i = 0; i < lst.size(); i++){
        QFile file(lst[i].toLocalFile());
        QFileInfo info(file.fileName());
        QString fileName = info.fileName();
        QString extention = fileName.remove(0, fileName.length() - 3);
        extention = extention.toLower();

        if (extention == "jpg" || extention == "gif" ||
            extention == "tif" || extention == "bmp" ||
            extention == "png" || extention == "pcx"){
            QImage img (lst[i].toLocalFile());
            QImageWriter k (lst[i].toLocalFile());
            table->setItem(i, 0, new QTableWidgetItem(info.fileName()));
            table->setItem(i, 1, new QTableWidgetItem(QString::number(img.size().width()) + "x" + QString::number(img.size().height())));
            table->setItem(i, 2, new QTableWidgetItem(QString::number(img.physicalDpiX())));
            table->setItem(i, 3, new QTableWidgetItem(QString::number(img.bitPlaneCount())));
            if (k.compression() == -1){
                table->setItem(i, 4, new QTableWidgetItem("No compression"));
            }
            else{
                table->setItem(i, 4, new QTableWidgetItem(QString::number(k.compression())));
            }

        }
        else{
            table->setRowCount(table->rowCount()-1);
        }
    }

    dialog->show();


    connect(dialog, SIGNAL(rejected()), this, SLOT(dialogClose()));
}

