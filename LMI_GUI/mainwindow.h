#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_Add_container_button_clicked();

    void on_Home_button_clicked();

    void on_AddContainer_button_clicked();

    void on_AckAddContainerPage1_button_clicked();

    void on_Ack1AddContainer_button_clicked();

    void on_Skip1AddContainer_button_clicked();

    void on_Ack2AddContainer_button_clicked();

    void on_Skip2AddContainer_button_clicked();

    void on_BackToHome_button_clicked();

    void on_Skip3AddContainer_button_clicked();

    void on_RequestContainer_buton_clicked();

    void on_pushButton_clicked();

    void on_Skip1RequestContainer_Button_clicked();

    void on_Skip2RequestContainer_Button_clicked();

    void on_BackToHome_button2_clicked();

    void on_RoutineScan_button_clicked();

    void on_Skip1RoutineScan_clicked();

    void on_BackToHome_button3_clicked();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
