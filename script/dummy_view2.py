#!/usr/bin/python

import roslib
roslib.load_manifest('std_msgs')
roslib.load_manifest('ratslam_ros')
import rospy

from std_msgs.msg import Int32
from ratslam_ros.msg import ViewTemplate

pub = 0
num = 0

def callback(data):
	global pub, num
	msg = ViewTemplate()
	msg.header.stamp = rospy.get_rostime()
	msg.header.seq = num
	msg.current_id = data.data
	msg.energy = 0
	pub.publish(msg)
	num += 1
    
# main
def main():
	global pub
	rospy.init_node('dummy_view')
	pub = rospy.Publisher('/irat_red/LocalView/Template', ViewTemplate, queue_size=10)
	rospy.Subscriber("/feature2view/view_id", Int32, callback)
	rospy.spin()
	
if __name__ == '__main__':
	main()
