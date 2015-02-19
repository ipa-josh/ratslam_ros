#!/usr/bin/env python

import sys, subprocess, time
from os import listdir, mkdir, system
from os.path import isfile, join, isdir


for fn in sys.argv[1:]:
	if fn.find("stupid")!=-1:
		system("script/eval.py ft_eval.launch _stupid "+fn)
		continue
		
	for pc_vt_inject_energy in [3,5,10]:
		for pc_cell_x_size in [5,10,15]:
			li = open("config/template_config.txt.in", "r")
			lo = open("tmp_config.txt", "w")
			t = li.read()
			t = t.replace("$pc_vt_inject_energy",str(pc_vt_inject_energy/100.))
			t = t.replace("$pc_cell_x_size",str(pc_cell_x_size/100.))
			lo.write(t)
			li.close()
			lo.close()
			
			system("script/eval.py ft_eval.launch _"+str(pc_vt_inject_energy)+"_"+str(pc_cell_x_size)+" "+fn)

