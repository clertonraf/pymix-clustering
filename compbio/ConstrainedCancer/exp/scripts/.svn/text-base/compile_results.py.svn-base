from os.path import *
import os

rootdir = "/media/Clerton_DATA/mestrado/sbrn/splitted/pomeroy-2002-v2_database"
size = 42

files = [-1]*(size)

for file in os.listdir(rootdir):
	filepath = sep + file
	path = rootdir + filepath
	if path.find(".txt") != -1:
		index = file.split(".txt")
		index = index[0].split("_")
		index = int(index[1])
		files[index-1] = file

		f = open(path,'r')
		line = f.readline()
		while len(line) > 0:
			if line.find("Error on test data") != -1:
				f.readline()
				classify = f.readline()
				classify = classify.strip()
				classify = classify.replace("           "," ")
				classify = classify.split(" ")
				files[index-1] = int(classify[3])
			line = f.readline()
print rootdir
print "Trainning vector: ", files
print "accuracy", sum(files)/float(len(files))
	
