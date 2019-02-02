#include "mainwindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;


    //Show the window in fullscreen
    //w.showFullScreen();
    w.showMaximized();

    return a.exec();
}
