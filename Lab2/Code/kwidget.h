
#ifndef KWIDGET_H
#define KWIDGET_H


#include <QWidget>
#include <QGridLayout>
#include <Qlabel>
#include <QFileSystemModel>
#include <QListView>
#include <QPushButton>
class KWidget : public QWidget
{
    Q_OBJECT
public:
    explicit KWidget(QWidget *parent = nullptr);

    QGridLayout* grid;
    QVBoxLayout* vBox;
    QListView* list;
    QFileSystemModel* model;
    QPushButton* button;

    QLabel* namelb;
    QLabel* sizelb;
    QLabel* dpilb;
    QLabel* colorDepthlb;
    QLabel* compressionlb;

    QLabel* name;
    QLabel* size;
    QLabel* dpi;
    QLabel* colorDepth;
    QLabel* compression;
public slots:
    void onListDoubleClicked(const QModelIndex& index);
    void onListClicked(const QModelIndex& index);
    void onMultiButtonPressed();
signals:


};

#endif // KWIDGET_H
