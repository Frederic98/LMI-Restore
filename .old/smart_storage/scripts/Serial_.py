#! /usr/bin/env python
import rospy
import serial
import actionlib
from smart_storage.msg import motor_controlAction, motor_controlGoal, motor_controlResult, motor_controlFeedback

def do_blink():
	ser = serial.Serial('/dev/ttyACM0', 9600)
	ser.write("G")
	ser.write(chr(8))
	ser.write(chr(10))
	ser.write("X")
	rospy.sleep(1)
	print("done")
	print(ser.readline())

def main_blink():
	



	while not rospy.is_shutdown():
		
		do_blink();
	#rospy.spin()




if __name__ == '__main__':
	try:
		main_blink()
	except rospy.ROSInterruptException:
		pass


