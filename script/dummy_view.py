#!/usr/bin/python

import roslib
roslib.load_manifest('nav_msgs')
roslib.load_manifest('ratslam_ros')
import rospy

from nav_msgs.msg import Odometry
from ratslam_ros.msg import ViewTemplate

pub = 0
num = 0

def callback(data):
	global pub, num
	msg = ViewTemplate()
	msg.header = data.header
	msg.current_id = num
	pub.publish(msg)
	num += 1
    
# main
def main():
	global pub
	rospy.init_node('dummy_view')
	pub = rospy.Publisher('/irat_red/LocalView/Template', ViewTemplate, queue_size=10)
	rospy.Subscriber("/odom", Odometry, callback)
	rospy.spin()
	
if __name__ == '__main__':
	main()
