#!/usr/bin/env python3
import sys
#sys.settrace()
import zmq
import time
import random
import re
import itertools
import mysql.connector

#log-in to mySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="LMI",
  passwd="LMI",
  database="LMI"
)

mycursor = mydb.cursor(buffered=True)

port = 5555
context = zmq.Context()
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)


from PyQt4 import uic
from PyQt4.QtCore import QPoint, QThread, QObject, QTimer
from PyQt4.QtGui import QWidget, QApplication, QMainWindow
#import LMI_resources          # QT Resource file compiled to python file, was built for qt5, so doesn't work for now...

def cell_to_pos(cell: str):
    return ('ABCDEFGHIJ'.index(cell[0]) + 1, int(cell[1:]))

def pos_to_cell(pos: tuple):
    return 'ABCDEFGHIJ'[pos[0] - 1] + str(pos[1])

# Client code, slave of servercode
class LMI_UI(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('mainwindow.ui', self)     # Change to the name of the .ui file


        # -----------Codes belonging to add_container-----------

        # move to add_container page 1 from the home menu
        self.AddContainer_button.clicked.connect(self.build_next_page)

        # move to add_container page 2
        # see def add_product_coordinate
        self.Ack1AddContainer_button.clicked.connect(self.add_product_coordinate)

        # move to add_container page 3
        # see def robot_positioned
        self.Skip1AddContainer_button.clicked.connect(self.robot_positioned) #comment this, because it is only for test purposes

        # move to add_container page 4
        # see def robot_to_queue
        self.Ack2AddContainer_button.clicked.connect(self.robot_to_queue)

        # move to add_container page 5
        # see def Data_ack
        self.Skip2AddContainer_button.clicked.connect(self.Data_ack) # comment this, because it is only for test purposes

        # move to add_container page 6
        # see def Move_storage
        self.Skip3AddContainer_button.clicked.connect(self.Move_storage)  # comment this, because it is only for test purposes

        # move back to the home_page
        self.BackToHome_button.clicked.connect(lambda click: self.Page_index.setCurrentIndex(0))


        # -----------Codes belonging to routine scan-----------

        # move to request_container page 1 from the home menu
        self.RequestContainer_buton.clicked.connect(self.build_next_page2)

        # move to request_container page 2
        # see def Search_product
        self.pushButton.clicked.connect(self.Search_product)

        # move to request_container page 3
        # see def Check_queue
        self.Skip1RequestContainer_Button.clicked.connect(self.Check_queue)  # comment this, because it is only for test purposes

        # move to request_container page 4
        # see def Move_pickup
        self.Skip2RequestContainer_Button.clicked.connect(self.Move_pickup)  # comment this, because it is only for test purposes

        #move back to the home_page
        self.BackToHome_button2.clicked.connect(lambda click: self.Page_index.setCurrentIndex(0))



    # list of defines
        # list of defines
    def build_next_page(self):
        
        sql = 'select x,y from containers where present=1'
        mycursor.execute(sql)
        taken = mycursor.fetchall()
        spots = list(itertools.product(range(2,11), range(2,11)))
        for t in taken:
            if t in spots:
                spots.remove(t)
      
        
        self.Coordinate_ComboBox.clear()
        for t in spots:
            self.Coordinate_ComboBox.addItem(pos_to_cell(t))
        
        print('Add container')
        self.Page_index.setCurrentIndex(1)

    def build_next_page2(self):
        
        sql = 'select id, description from containers where present=1'
        mycursor.execute(sql)
        containers = mycursor.fetchall()

        self.ProductSearch_comboBox.clear()
        for t in containers:
            num, desc = t
            name = str(num) + " " + str(desc)
            self.ProductSearch_comboBox.addItem(name)
        
        print('Request Containers')
        self.Page_index.setCurrentIndex(7)
    
    def add_product_coordinate(self):
        #Productname is send to server
        Productname = self.ProductName_LineEdit.text()
        print(Productname)
        
        Productplace = self.Coordinate_ComboBox.currentText()
        print(Productplace)
        col, row = cell_to_pos(Productplace)
        print(col,row)
        
        print("Sending request to place", Productname ,"to row" ,row ,"and column" , col)
        
        socket.send_string("Place container with {}".format(Productname))
        #  Get the reply.
        message = socket.recv()
        print("Received name reply ", message)
        
        socket.send_string("Place container to column {}".format(col))
        #  Get the reply.
        message = socket.recv()
        print("Received col reply ", message)
        
        socket.send_string("Place container to row {}".format(row))
        #  Get the reply.
        message = socket.recv()
        print("Received row reply ", message)


        socket.send_string("Move to exit")
        #  Get the reply.
        message = socket.recv()
        print("Received move to exit reply ", message)
        
        poller = MotionWaiter()
        poller.finished.connect(self.robot_positioned)
        poller.start()
        self.Page_index.setCurrentIndex(2)

    def robot_positioned(self):
        self.Page_index.setCurrentIndex(3)
        print('Robot positioned')

    def robot_to_queue(self):
        self.Page_index.setCurrentIndex(4)

        socket.send_string("Insert to queue")
        message = socket.recv().decode()

        waiter = MotionWaiter()
        waiter.finished.connect(self.Get_container_info)
        waiter.start()
        print('Robot is allowed to move to the queue')

    def Data_ack(self):
        print('Waiting for motion...')
        poller = MotionWaiter()
        poller.finished.connect(self.Page_index_6)
        poller.start()
        self.Page_index.setCurrentIndex(5)
        print('Information in queue is checked')

    def Page_index_6(self):
        self.Page_index.setCurrentIndex(6)
    
    def Move_storage(self):

        self.Page_index.setCurrentIndex(6)
        print('Robot is allowed to move to storage')

    def Search_product(self):

        SelectedContainer = self.ProductSearch_comboBox.currentText()
        print(SelectedContainer)
        SelectedID = int(SelectedContainer.split(' ')[0])
        print(SelectedID)
                
        self.Page_index.setCurrentIndex(8)
        
        socket.send_string("Obtain container {}".format(SelectedID))
        message = socket.recv().decode()

        socket.send_string("Obtain from queue")
        message = socket.recv().decode()

        waiter = MotionWaiter()
        waiter.finished.connect(self.Get_container_info2)
        waiter.start()
        print('Container is allowed to move to the queue')

    def Check_queue(self):
        # xxxxxxxxxxxxxxxxx INSERT ID FOR: "ProductID_TextEdit" xxxxxxxxxxxxxxxxxxxxxxxx
        # xxxxxxxxxxxxxxxxx INSERT PRODUCTNAME FOR: "ProductName_TextEdit" xxxxxxxxxxxxxxxxxxxxxxxx
        # xxxxxxxxxxxxxxxxx INSERT MASS FOR: "Mass_TextEdit2" xxxxxxxxxxxxxxxxxxxxxxxx
        self.Page_index.setCurrentIndex(9)
        print('Container is allowed to move to the queue')

    def Move_pickup(self):
        self.Page_index.setCurrentIndex(10)
        print('Container is allowed to move to the pickup')

    def Get_container_info(self):
        socket.send_string("Whats the weight?")
        message = socket.recv().decode()
        weight = float(re.match("weight is ([\d\.]+)", message).group(1))
        self.Mass_TextEdit.setText('{:.2f}g'.format(weight))
        
        socket.send_string("Whats the ID?")
        id = socket.recv().decode()
        self.BarcodeID_TextEdit.setText(id)

        socket.send_string("Insert container")
        socket.recv()

        SSTimer(3500, self.Data_ack)

    def Get_container_info2(self):
        socket.send_string("Whats the weight?")
        message = socket.recv().decode()
        weight = float(re.match("weight is ([\d\.]+)", message).group(1))
        self.Mass_TextEdit2.setText('{:.2f}g'.format(weight))
        
        socket.send_string("Whats the ID?")
        id = socket.recv().decode()
        self.ProductID_TextEdit.setText(id)

        socket.send_string("Whats the Name?")
        name = socket.recv().decode()
        self.ProductName_TextEdit.setText(name)

        SSTimer(3500, self.Move_pickup)

        
        


class MotionWaiter(QThread):
    threads = []
    def __init__(self):
        QThread.__init__(self)
        for t in self.threads:
            if not t.isRunning():
                self.threads.remove(t)
        self.threads.append(self)
    
    def run(self):
        socket.send_string("Buzzy?")
        #  Get the reply.
        message = socket.recv()
        print("Received Buzzy? reply ", message)

        buzzy = True

        while buzzy:
            socket.send_string("are you buzzy?")
            #  Get the reply.
            message = socket.recv().decode()
            print("Received buzzy reply ", message)

            if message == "yes":
                buzzy = True
            elif message == "no":
                buzzy = False

class SSTimer():
    instances = []
    def __init__(self, *args, **kwargs):
        self.instances.append(self)
        self.timer = QTimer.singleShot(*args, **kwargs)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # screenres = app.desktop().screenGeometry(1)
    ui = LMI_UI()
    # ui.move(QPoint(screenres.x(), screenres.y()))
    # ui.resize(screenres.width(), screenres.height())
    ui.show()
    rc = app.exec_()
    sys.exit(rc)

    # page transitions to add_container
    # def MainWindow::on_AddContainer_button_clicked():
    # {
    #     ui.Page_index->setCurrentIndex(1); # Go to add_container_page1
    # }
