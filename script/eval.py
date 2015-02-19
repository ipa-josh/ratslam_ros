#!/usr/bin/env python

import sys, subprocess, time
from os import listdir, mkdir, system
from os.path import isfile, join, isdir, basename
import shutil

def evaluate(fn, launch="ft.launch", prefix=""):
	#start ratslam
	if isdir('/tmp/video'): shutil.rmtree('/tmp/video')
	mkdir('/tmp/video')
	base = basename(fn)
	p_ratslam = subprocess.Popen(["roslaunch","ratslam_ros",launch])
	p_img =    subprocess.Popen(["rosrun","image_view","extract_images","_sec_per_frame:=0","image:=/irat_red/PoseCell/MapImage",'_filename_format:=/tmp/video/%05i.jpg'])
	p_record = subprocess.Popen(["rosbag","record","-O","/tmp/eval_"+base+prefix,"--lz4","/irat_red/PoseCell/MapMarker"])
	p_launch = subprocess.Popen(["rosbag","play","-r","3",fn])
	
	while p_launch.poll() is None:
		time.sleep(0.1)
		
	p_ratslam.kill()
	p_record.kill()
	p_img.kill()
	
	onlyfiles = [ int(f[0:5]) for f in listdir("/tmp/video") if isfile(join("/tmp/video",f)) ]
	if len(onlyfiles)<1: return
	#print onlyfiles
	print max(onlyfiles)
	shutil.move("/tmp/video/%05i.jpg"%max(onlyfiles), "/tmp/eval_"+base+prefix+".jpg")
	
	system("ffmpeg -r 30 -qscale 1 -i /tmp/video/%05d.jpg /tmp/eval_"+base+prefix+".avi")

for fn in sys.argv[3:]:
	print fn
	evaluate(fn, sys.argv[1], sys.argv[2])
