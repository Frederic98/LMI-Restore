// add the following pages
#include "mainwindow.h"
#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui; 
}

// codes for transitioning to another window/page


// Return to homepage button
void MainWindow::on_Home_button_clicked()
{
  ui->Page_index->setCurrentIndex(0); //return to homepage
}

// page transitions to add_container
void MainWindow::on_AddContainer_button_clicked()
{
  ui->Page_index->setCurrentIndex(1); //Go to add_container_page1
}

void MainWindow::on_Ack1AddContainer_button_clicked()
{
    ui->Page_index->setCurrentIndex(2); //Go to add_container_page2
}

void MainWindow::on_Skip1AddContainer_button_clicked()
{
    ui->Page_index->setCurrentIndex(3); //Skip to add_container_page3
}

void MainWindow::on_Ack2AddContainer_button_clicked()
{
    ui->Page_index->setCurrentIndex(4); //Skip to add_container_page4
}

void MainWindow::on_Skip2AddContainer_button_clicked()
{
    ui->Page_index->setCurrentIndex(5); //Skip to add_container_page5
}

void MainWindow::on_Skip3AddContainer_button_clicked()
{
    ui->Page_index->setCurrentIndex(6); //Skip to add_container_page6
}

void MainWindow::on_BackToHome_button_clicked()
{
  ui->Page_index->setCurrentIndex(0); //return to homepage
}


// page transitions belonging to request_container
void MainWindow::on_RequestContainer_buton_clicked()
{
 ui->Page_index->setCurrentIndex(7); //Go to request_container_page1
}

void MainWindow::on_pushButton_clicked()
{
 ui->Page_index->setCurrentIndex(8); //Go to request_container_page2
}

void MainWindow::on_Skip1RequestContainer_Button_clicked()
{
 ui->Page_index->setCurrentIndex(9); //Go to request_container_page3
}

void MainWindow::on_Skip2RequestContainer_Button_clicked()
{
    ui->Page_index->setCurrentIndex(10); //Go to request_container_page4
}

void MainWindow::on_BackToHome_button2_clicked()
{
    ui->Page_index->setCurrentIndex(0); //return to homepage
}

// page transitions belonging to Routine_Scan
void MainWindow::on_RoutineScan_button_clicked()
{
    ui->Page_index->setCurrentIndex(11); //Go to routine_scan_page1
}

void MainWindow::on_Skip1RoutineScan_clicked()
{
   ui->Page_index->setCurrentIndex(12); //Skip to routine_scan_page2
}

void MainWindow::on_BackToHome_button3_clicked()
{
  ui->Page_index->setCurrentIndex(0); //return to homepage
}










