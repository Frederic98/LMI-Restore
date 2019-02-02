#!/usr/bin/env python
import rospy
import actionlib
from std_msgs.msg import *
from smart_storage.msg import motor_controlAction, motor_controlGoal, motor_controlResult
from smart_storage.srv import *

#db = sqlite3.connect("SmartStorage.db")
#pub = rospy.Publisher('storage_result', String, queue_size=10)



def handle_order_service(req):
	global command
	SmartStorage = rospy.ServiceProxy('storage_service', storage_service)

	if (command['isBusy'] == 0):	
		
		#rospy.Subscriber("/storage_AddBox", Int8, storage_AddBox)
		
		if (req.type == 'set'):
			add = SmartStorage('add', req.box, 0, 0)
			if (add.error == 0):
				command = {'box': add.box, 'type': "set", 'row': add.row, 'column': add.column, 'message': add.message, 'error': add.error, 'isBusy': 1}
			print add.message
			return order_serviceResponse(add.box, add.row, add.column, add.message, add.error, 0)
		elif (req.type == 'get'):
			delete = SmartStorage('delete', req.box, 0, 0)
			if (delete.error == 0):
				command = {'box': delete.box, 'type': "get", 'row': delete.row, 'column': delete.column, 'message': delete.message, 'error': delete.error, 'isBusy': 1}
			print delete.message
			return order_serviceResponse(delete.box, delete.row, delete.column, delete.message, delete.error, 0)
		else:
			print 'Invalid Type'
			command = {'box': req.box, 'type': "", 'row': 0, 'column': 0, 'message': "Invalid Type", 'error': 1, 'isBusy': 0}
			return order_serviceResponse(req.box, 0, 0, "Invalid Type", 1, 0)
	else:
		search = SmartStorage('search', req.box, 0, 0)
		
		message = search.message
		
		if(search.error == 1):
			if (req.type == 'set'):
				message = "Box can be placed but the SmartStorage is currenly busy with another order"
			elif (req.type == 'get'):
				message = "Box is not in storage"
		elif(search.error == 0):			
			if (req.type == 'set'):
				message = "Box is already in storage"
			elif (req.type == 'get'):
				message = "Box is in storage but the SmartStorage is currenly busy with another order"

		return order_serviceResponse(search.box, search.row, search.column, message, search.error, 1)		


def handle_debug_motor_service(req):
        global command
	
	ltype = ''
	
	if (req.type == 'set' or req.type == 'get'):
		ltype = req.type
	else:
		return debug_motor_serviceResponse(req.row, req.column, 'Type is invalid, should be (set/get)')

        command = {'box': 'Debug Box', 'type': req.type, 'row': req.row, 'column': req.column, 'message': 'Debug: motor control active', 'error': 0, 'isBusy': 1}
        
        
        
        return debug_motor_serviceResponse(req.row, req.column, 'Command executed')


def demo_loop(ctype, row, column):
	order = rospy.ServiceProxy('debug_motor_service', debug_motor_service)
        add = order(ctype, row, column)


def SmartStorage():
	rospy.init_node('storage_node', anonymous=False)
	#order_service_server()
	s = rospy.Service('order_service', order_service, handle_order_service)
        s = rospy.Service('debug_motor_service', debug_motor_service, handle_debug_motor_service)
	
	global command
	global client

	command = {'box': 0, 'type': "", 'row': 0, 'column': 0, 'message': "", 'error': 0, 'isBusy': 0}

	client = actionlib.SimpleActionClient('motor_control_server', motor_controlAction)
	client.wait_for_server()


    	print "SmartStorage Online."
    	
	#pub = rospy.Publisher('SmartStorage_Available', int8, queue_size=10)
	#pub.publish(1)
	
	counter = 6
        #order = rospy.ServiceProxy('debug_motor_service', handle_debug_motor_service)

        rospy.sleep(30)

	while not rospy.is_shutdown():
		if(command['isBusy'] == 1):
			rospy.loginfo("MotorControl Active")
			#MotorControl()
			motor_control()

                else:
                        if(counter == 0):
                              demo_loop('get', 9, 3)
                              counter = 1
                        elif(counter == 1):
                              demo_loop('set', 5, 7)
                              counter = 2
                        elif(counter == 2):
                              demo_loop('get', 6, 2)
                              counter = 3
                        elif(counter == 3):
                              demo_loop('set', 2, 10)
                              counter = 4

                        elif(counter == 4):
                              demo_loop('get', 5, 7)
                              counter = 5
                        elif(counter == 5):
                              demo_loop('set', 9, 3)
                              counter = 6
                        elif(counter == 6):
                              demo_loop('get', 2, 10)
                              counter = 7
                        elif(counter == 7):
                              demo_loop('set', 6, 2)
                              counter = 0

	
def MotorControl():
	global command
	rospy.sleep(10)
	rospy.loginfo("Box " +str(command["box"]) + " will be " + str(command["type"]) + " at row "  + str(command["row"]) + ", column " + str(command["column"]))
	rospy.sleep(3)
	rospy.loginfo("Motor Done")
	command["isBusy"] = 0



def motor_control():
	goal = motor_controlGoal()
	goal.row = command["row"]
	goal.column = command["column"]
	goal.type = command["type"]

	client.send_goal(goal, feedback_cb=callfeedback)

	#rospy.sleep(2)
	#client.cancel_goal()

	#test_val = 0

	#client.wait_for_result()

	
	while (client.get_state() != 2 and client.get_state() != 3 and client.get_state() != 4 and not rospy.is_shutdown()):
		rospy.sleep(0.1)
		#test_val += 1	
		#print(test_val)
		'''c = getchar()
        	if c in ' \n':
        		print "Enter key was pressed! Goal is canceled."
			client.cancel_goal()
		if c in '27':
			print"Escape is pressed"
	'''
		
	if(client.get_state() == 4):
		SmartStorage = rospy.ServiceProxy('storage_service', storage_service)
		if(command["type"] == "set"):
			add = SmartStorage('delete', command["box"], 0, 0)
		elif(command["type"] == "get"):
			delete = SmartStorage('add', command["box"], 0, 0)


	print('Motor Control Finished: %s'%(client.get_result().r_message))
	command["isBusy"] = 0

def callfeedback(feedback):
	print('Motor Control Feedback: %u %s'%(feedback.fb_value, feedback.fb_message))


def shutdown():
	db.close()
	print 'shutdown'


if __name__ == '__main__':
	try:
		SmartStorage()
	except rospy.ROSInterruptException:
		shutdown()
