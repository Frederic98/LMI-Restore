#! /usr/bin/env python
import rospy
import actionlib
import sys
from smart_storage.msg import motor_controlAction, motor_controlGoal, motor_controlResult
import select
import sys, termios



def callfeedback(feedback):
	print('[Feedback] feedback test: %f'%(feedback.blinks_perf))

def getchar():
    char = '_'
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~(termios.ECHO | termios.ICANON) # turn off echo and canonical mode which sends data on delimiters (new line or OEF, etc)
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new) # terminal is now 
        ready, steady, go = select.select([sys.stdin], [], [], 1)
        if ready:
            char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return char
	



def blink_client():

	global client
	client = actionlib.SimpleActionClient('blinker', motor_controlAction)
	client.wait_for_server()

	goal = motor_controlGoal()
	blinks = input("Enter the amount of blinks:")
	goal.blink_amount = blinks

	client.send_goal(goal, feedback_cb=callfeedback)

	#rospy.sleep(2)
	#client.cancel_goal()
	print "Press Enter to cancel the goal"
	while (client.get_state() != 2 and client.get_state() != 3 and client.get_state() != 4 and not rospy.is_shutdown()):
		rospy.sleep(0.1)
		c = getchar()
        	if c in ' \n':
        		print "Enter key was pressed! Goal is canceled."
			client.cancel_goal()
		if c in '27':
			print"Escape is pressed"
			
		

	print('Blinks done: %s'%(client.get_result().message))
	blink_client()	


if __name__ == '__main__':
	try:
		rospy.init_node('blinker_client')
		blink_client()
		

			
	except rospy.ROSInterruptException:
		
		pass

