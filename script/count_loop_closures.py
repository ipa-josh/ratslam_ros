#!/usr/bin/python

import rosbag
import sys


for fn in sys.argv[1:]:
	nums=[0,0,0,0]
	scenes=[0,0]

	for topic, msg, t in rosbag.Bag(fn).read_messages():
		if topic == "/irat_red/PoseCell/TopologicalAction" and msg.action:
			nums[msg.action] += 1
		if topic == "/feature2view/view_id" and msg.data:
			scenes[0] = max(scenes[0], msg.data)
			scenes[1]+= 1
			if scenes[1]<scenes[0]: scenes[1]=scenes[0]
			
	print fn
	print ["","CREATE_NODE","CREATE_EDGE","SET_NODE"]		
	print nums
	print "found ",scenes[1]," scenes, recognized ",scenes[1]-scenes[0]," scenes"
