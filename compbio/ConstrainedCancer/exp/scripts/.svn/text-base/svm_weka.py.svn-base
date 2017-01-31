from os.path import *
import os

rootdir = "/media/Clerton_DATA/mestrado/sbrn/splitted/pomeroy-2002-v2_database"

for file in os.listdir(rootdir):
	filepath = sep + file
	path = rootdir + filepath
	if isdir(path):
		path1 = path + sep
		train = None
		test = None
		for fold in os.listdir(path):
			path2 = path1+fold
			if path2.find(".arff") != -1:
				if path2.find("train") != -1:
					train = path2
				if path2.find("test") != -1:
					test = path2
		print "train: ",train
		print "test: ",test
		print "output :",rootdir+sep+"result_"+file+".txt"
		output = " > "+rootdir+sep+"result_"+file+".txt"
		command = "java -Xmx1024M -cp /media/Clerton_DATA/mestrado/Weka/weka.jar weka.classifiers.functions.SMO -i -C 1.0 -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K -t " + train + " -T " + test + output
		os.system(command)
