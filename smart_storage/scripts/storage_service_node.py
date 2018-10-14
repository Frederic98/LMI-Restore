#!/usr/bin/env python

import sqlite3
import rospy
from smart_storage.srv import *
from Storage_Functions import *

def handle_storage_service(req):
	db = sqlite3.connect("/home/ubuntu/catkin_ws/src/smart_storage/SmartStorage.db")
	#db = sqlite3.connect("SmartStorage.db")
	print "input: type: %s box: %s row: %s column: %s"%(req.type, req.box, req.row, req.column)
    	message = ""
	row = 0
	column = 0
	error = 0
	
	if (req.type == 'add'):
		add = AddBox(db, req.box)
		message = add["message"]
		row = add["row"]
		column = add["column"]
		error = add["error"]
		print 'added'
		print message
	elif (req.type == 'delete'):
		delete = DeleteBox(db, req.box)
		message = delete["message"]
		row = delete["row"]
		column = delete["column"]
		error = delete["error"]
		print 'delete'
		print message
	elif (req.type == 'search'):
		check = db_SearchBox(db, req.box)
		print 'search'
		print check
		if(str(check) == 'None'):
			message = "Box " + str(req.box) + " not found"
			error = 1
		else:
			row = check[0]
			column = check[1]
			message = "Box has been found on row " + str(row) + " column " + str(column)
	else:
		print 'Invalid Type'
	
	db.close()
	return storage_serviceResponse(req.box, row, column, message, error)

def storage_service_server():
	rospy.init_node('storage_service_server')
	s = rospy.Service('storage_service', storage_service, handle_storage_service)
	print "Ready to serv..ice..."
	rospy.spin()

if __name__ == "__main__":
    storage_service_server()
