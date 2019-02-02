#!/usr/bin/env python3
#importing communication protocol's
import zmq
import time
import sys
import re
import itertools
import random
from rt_controller import *
from barcodeScanner import Scanner

#import database
import mysql.connector

steps = {'x': StepConfig(140 / 360 * 1.8 / 960 * 1000, 16, 0),
         'y': StepConfig(140 / 360 * 1.8 * 1.1879194630872485, 16, 0),
         'z': StepConfig(8 / 360 * 1.8 * 626.9592476489028, 4, 0),
         'r': StepConfig(1000 / 360, 4, 53)}
nucleo = RTController('/dev/ttyACM0', steps, 2.3, 137, 137, 140)
nucleo.home(z=True)
nucleo.home(r=True)
nucleo.move_position(r=0)
nucleo.home(x=True, y=True)

scanner = Scanner('/dev/ttyS0', 9600)

container_id = 0

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
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

#recognition of certain text in messages to perform (placing new container)
re_placecontainerwith = re.compile(r'Place container with (\w+)')
re_placecontainertocolumn = re.compile(r'Place container to column (\d+)')
re_placecontainertorow = re.compile(r'Place container to row (\d+)')
re_insertqueue = re.compile(r'Insert to queue')
re_insertcontainer = re.compile(r'Insert container')

#recognition of certain text in messages to perform (requesting container)
re_obtaincontainer = re.compile(r'Obtain container (\d+)')
re_obtainqueue = re.compile(r'Obtain from queue')
re_deliver = re.compile(r'Deliver container')

re_getweight = re.compile(r'Whats the weight?')
re_getid = re.compile(r'Whats the ID?')
re_getname = re.compile(r'Whats the Name?')

re_buzzy = re.compile(r'Buzzy?')

re_movetoexit = re.compile(r'Move to exit')


def movetoexit():
    nucleo.move_position(0,0)
    #send commands to move to exit to Nucleo

def insert_and_weigh():
    global container_id
    nucleo.place_container(0,4)
    container_id = scanner.scan()

def buzzy():
    for x in range(0, 3):    
        message = socket.recv().decode()
        print(message)
        socket.send_string("yes") 

    message = socket.recv().decode()
    print(message)
    socket.send_string("no")

      

def insert_container(container_id, name, weight, col, row):
    print('placing container {} to storage'.format(container_id))
    try:
        sql = "INSERT INTO containers (id, description, weight, present, x, y) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (container_id, name, weight, 1, col, row)
        mycursor.execute(sql,val)
        mydb.commit()

        nucleo.place_container(int(col)-1, int(row)-1)
        #send insert coordinates to nucleo
        
        
    except Exception as e:
        print("this ID or place is already taken")
        print(e)
        pass


def request_container(container_id):
    print('requesting container'.format(container_id))
    try:
        # sql = "INSERT INTO containers (id, description, weight, present, y, x) VALUES (1, \"testbakje\", 283.45, 1, 1, 1)"
        sql = ("select x,y from containers where id = %s")
        mycursor.execute(sql, (container_id, ))
        myresult = mycursor.fetchall()
        for x in myresult:
          print(x)

        nucleo.pickup_container(col-1, row-1)
        
        sql = ("DELETE FROM containers WHERE id = %s")
        mycursor.execute(sql,(container_id, ))
        print(mycursor.rowcount, "record(s) deleted")
        
    except Exception:
        print("not able to do this")
        pass



print('Starting server...')

while True:
    #  Wait for next request from client
    message = socket.recv().decode()
    print(message)
    
    if re_placecontainerwith.match(message):
       name = re_placecontainerwith.match(message).group(1)
       print('name is', name)
       socket.send_string("I now know what containers name is")
       
    elif re_placecontainertocolumn.match(message):
        col = re_placecontainertocolumn.match(message).group(1)
        print('column is', col)
        socket.send_string("I now know what column my container needs to go to")
        
    elif re_placecontainertorow.match(message):
        row = re_placecontainertorow.match(message).group(1)
        socket.send_string("I now know what row my container needs to go to")

    elif re_insertqueue.match(message):
        socket.send_string("I am goiung to insert into queue and weight + scan the container")
        nucleo.place_container(0,3)
        container_id = scanner.scan()
        nucleo.pickup_container(0,3) 
        #socket.send_string("I am goiung to insert into queue and weight + scan the container")

    elif re_insertcontainer.match(message):
        insert_container(container_id, name, weight, col, row)
        socket.send_string("I am goiung to insert into the storage system and database, hang on :)")
        


    elif re_obtaincontainer.match(message):
        container_id=re_obtaincontainer.match(message).group(1)
        request_container(container_id)
        socket.send_string("Im going to get the container and remove it from my database, hang on :)")

  
    elif re_obtainqueue.match(message):
        socket.send_string("Moving the obtained container to the queue ")


    elif re_buzzy.match(message):
        socket.send_string("Checking if i'm buzzy, please wait")
        buzzy()
         
    elif re_movetoexit.match(message):
        socket.send_string("Moving to exit")
        movetoexit()

    elif re_obtainqueue.match(message):
        nucleo.place_container(0,3)
        container_id = scanner.scan()
        nucleo.pickup_container(0,3)      
        socket.send_string("Obtaining container to queue")
    elif re_getweight.match(message):
        socket.send_string('weight is 314.1592')
        weight = 314.1592
    elif re_getid.match(message):
        socket.send_string(str(container_id))
    elif re_getname.match(message):
        sql = ("select description from containers where id = %s")
        mycursor.execute(sql, (container_id, ))
        myresult = mycursor.fetchall()
        socket.send_string(str(myresult))
        
        
    else:
        socket.send_string("Unknown command")












##re_deliver = re.compile(r'Deliver container')
##
##re_buzzy = re.compile(r'Buzzy?')
##
##re_movetoexit = re.compile('Move to exit')
