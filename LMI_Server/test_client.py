import zmq
import sys
import time
import random

port = 5555
context = zmq.Context()
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)


#  Do 10 requests, waiting each time for a response
for bakje in range (1,150):
    print("Sending request ", bakje ,"...")
    selectedID = (random.randint(0,1000))
    socket.send_string("Pak bakje {}".format(selectedID))
    #  Get the reply.
    message = socket.recv()
    print("Received reply ", message)
    time.sleep(1)
    
for bakje in range (1,10):
    print("Sending request ", bakje ,"...")
    
    socket.send_string("Plaats bakje {}".format(random.randint(0,1000)))
    #  Get the reply.
    message = socket.recv()
    print("Received reply ", message)
    time.sleep(1)
    
for bakje in range (1,10):
    print("Sending request ", bakje ,"...")
    
    socket.send_string("Scan systeem")
    #  Get the reply.
    message = socket.recv()
    print("Received reply ", message)
    time.sleep(1)