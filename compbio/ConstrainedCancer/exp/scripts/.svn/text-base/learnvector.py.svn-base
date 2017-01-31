from math import sqrt

filename = "/home/craf/Desktop/Results/cluster/output/pomeroy-2002-v2_database5.txt"

print filename

f = open(filename,"r")

f.readline()
f.readline()
classes = f.readline()
classes = classes.replace("Classes ","")
classes = classes.lstrip('[')
classes = classes.rstrip(']\n')
classes = classes.split(',')
classes_lst = []
for i in classes:
	classes_lst.append(int(i))
learning_vector = []

line = f.readline()
while len(line) > 0:

	line = f.readline()
	if(len(line) == 0):
		break
	while (line.find("sample ") == -1) or (line.find("False") != -1):
		line = f.readline()
		if(len(line) == 0):
			break
	
	if(len(line) == 0):
		break	
	line = line.replace("sample ","")
	index = line.find(" of")
	sample = int(line[0:index])
	
	line = f.readline()
	if(len(line) == 0):
		break
	while line.find("mapClassify ") == -1:
		line = f.readline()
		if(len(line) == 0):
			break
	if(len(line) == 0):
		break	
	line = line.replace("mapClassify ","")
	mapClassify = int(line[0])
	if mapClassify == classes_lst[sample]:
		learning_vector.append(1)
	else:
		learning_vector.append(0)

	line = f.readline()
print "Learning vector:",learning_vector

tam = len(learning_vector)

mean = sum(learning_vector)/float(tam)

print "mean",mean

num = []

for index in learning_vector:
	num.append((index-mean)**2)

var = sum(num)/float(tam)

print "var",var

std = sqrt(var)

print "std",std
