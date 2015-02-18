#!/usr/bin/env python

import sys, subprocess, time
from os import listdir, mkdir, system
from os.path import isfile, join, isdir
import shutil

def evaluate(fn):
	#start ratslam
	if isdir('/tmp/video'): shutil.rmtree('/tmp/video')
	mkdir('/tmp/video')
	p_ratslam = subprocess.Popen(["roslaunch","ratslam_ros","ft.launch"], stderr=subprocess.PIPE)
	p_img =    subprocess.Popen(["rosrun","image_view","extract_images","_sec_per_frame:=0","image:=/irat_red/PoseCell/MapImage",'_filename_format:=/tmp/video/%05i.jpg'])
	p_record = subprocess.Popen(["rosbag","record","-O","/tmp/eval_"+fn,"--lz4","/irat_red/PoseCell/MapMarker"], stderr=subprocess.PIPE)
	p_launch = subprocess.Popen(["rosbag","play","-r","3",fn], stderr=subprocess.PIPE)
	
	while p_launch.poll() is None:
		time.sleep(0.1)
		
	p_ratslam.kill()
	p_record.kill()
	p_img.kill()
	
	onlyfiles = [ int(f[0:5]) for f in listdir("/tmp/video") if isfile(join("/tmp/video",f)) ]
	if len(onlyfiles)<1: return
	#print onlyfiles
	print max(onlyfiles)
	shutil.move("/tmp/video/%05i.jpg"%max(onlyfiles), "/tmp/eval_"+fn+".jpg")
	
	system("ffmpeg -r 30 -b 2000 -i /tmp/video/%05d.jpg /tmp/eval_"+fn+".avi")

for fn in sys.argv[1:]:
	print fn
	evaluate(fn)
