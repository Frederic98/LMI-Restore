#! /usr/bin/env python
import rospy
import serial
import serial.tools.list_ports
import actionlib
from smart_storage.msg import motor_controlAction, motor_controlGoal, motor_controlResult, motor_controlFeedback

def control_motor(goal):
	result = motor_controlResult()
	values_checked = 0
	read_line = True
	i_type = ""
	f_value = 0

	complete_state = False
	error_state = False
	
	if(goal.type == "set"):
		i_type = "P"
	elif(goal.type == "get"):
		i_type = "G"

	ser.write(i_type)
	ser.write(chr(goal.row))
	ser.write(chr(goal.column))
	ser.write("X")

	while (not complete_state and not error_state):
		if(ser.in_waiting):
			if(read_line):
				serial_line = ser.readline()
				serial_line = serial_line.replace("\r\n", "")
				read_line = False

			if((values_checked == 0 and serial_line == i_type)
					or (values_checked == 1 and serial_line == str(goal.row))
					or (values_checked == 2 and serial_line == str(goal.column))
					or (values_checked == 3 and serial_line == "X")):
				values_checked += 1
				read_line = True
			elif(values_checked == 4):
				if(serial_line == "Complete"):
					complete_state = True
					result.r_message = (serial_line)
				else:
					f_value += 1
					feedback = motor_controlFeedback()
					feedback.fb_message = serial_line
					feedback.fb_value = f_value
					server.publish_feedback(feedback)
					read_line = True
					
			else:
				print('error: %i %s'%(values_checked, serial_line))
				print('type: %s, row: %s, column: %s'%(i_type, goal.row, goal.column))
				result.r_message = (serial_line)
				server.set_aborted(result)
				error_state = True

	
	if(not error_state and complete_state):
		server.set_succeeded(result)


'''
	while result.updates_sent < goal.blink_amount:
		if(ser.in_waiting):
			blinks_perf = int(goal.blink_amount)-int(ser.readline())
			print(server.is_preempt_requested())
			if server.is_preempt_requested():
				ser.write(str(0))
				result.message = ("Canceld at %d" % blinks_perf)
				server.set_preempted(result, "Blinker preempted")
				return

			feedback = motor_controlFeedback()
			print(blinks_perf)
			feedback.blinks_perf = blinks_perf
			server.publish_feedback(feedback)
			result.updates_sent += 1

	server.set_succeeded(result)
'''


def main_motorcontrol():
	rospy.init_node('motor_control_server')
	global server
	global ser

	'''

	for p in serial.tools.list_ports.comports():
		print ("device: ", p.device)
		print ("name: ", p.name)
		print ("description: ", p.description)
		print ("hwid: ", p.hwid)
		print ("vid: ", p.vid)
		print ("pid: ", p.pid)
		print ("serial_number: ", p.serial_number)
		print ("location: ", p.location)
		print ("manufacturer: ", p.manufacturer)
		print ("product: ", p.product)
		print ("interface: ", p.interface)
	'''	

	arduino_ports = [
		p.device
		for p in serial.tools.list_ports.comports()
		if 'Arduino' in p.manufacturer
	]
	if not arduino_ports:
		print "Connection failed, no Arduino found"
		return
	if len(arduino_ports) > 1:
		print "More than 1 Arduino has been found, the first Arduino will be used"

	print "Connecting to %s"%(arduino_ports[0])

	#ser = serial.Serial('/dev/ttyACM0', 9600)
	ser = serial.Serial(arduino_ports[0])
	

	server = actionlib.SimpleActionServer('motor_control_server', motor_controlAction, control_motor, False)
	server.start()

	while not rospy.is_shutdown():
		rospy.sleep(0.1)
	#rospy.spin()




if __name__ == '__main__':
	try:
		main_motorcontrol()
	except rospy.ROSInterruptException:
		pass


