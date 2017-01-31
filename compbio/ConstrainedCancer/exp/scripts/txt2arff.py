from os.path import *
import os

rootdir = "/media/Clerton_DATA/mestrado/sbrn/splitted/chen-2002_database"
nclasses = "1,2"

for file in os.listdir(rootdir):
	filepath = sep + file
	path = rootdir + filepath
	if isdir(path):
		path1 = path + sep
		for fold in os.listdir(path):
			if (path1+fold).find(".txt") != -1:

				relation = fold.split(" .txt")[0]
			
				print "converting to " + path1 + relation+".arff\n"
				arff = open(path1 + relation + '.arff','w')

				arff.write('@relation '+relation + '\n\n')

				txt = open(path1 + fold,"r")

				line = txt.readline()
				attributes = line.replace("\"","")
				attributes = attributes.replace("\n","")
				attributes = attributes.split("\t")
				for index in attributes:
					attribute = '@attribute ' + index
					if index == 'class':
						attribute += ' {' + nclasses + '} \n\n' 
					else:
						attribute +=' numeric \n' 
					arff.write(attribute)

				arff.write('@data\n')

				while(len(line) > 0):
					line = txt.readline()
					sample = line.split("\t")
					sample.pop(0)
					if len(line) > 0:
						sample[len(sample)-1] = str(int(sample[len(sample)-1]))
		
					data = ",".join(sample)
					arff.write(data + "\n")



#dir_in = "/media/Clerton_DATA/mestrado/sbrn/splitted/armstrong-2002-v1_database/1/"
#dir_out = "/media/Clerton_DATA/mestrado/sbrn/splitted/armstrong-2002-v1_database/1/"
#relation = "armstrong-2002-v1_database_test_1 "
#nclasses = "1,2"

#arff = open(dir_out + relation + '.arff','w')

#arff.write('@relation '+relation + '\n\n')

#txt = open(dir_in + relation + ".txt","r")

#line = txt.readline()
#attributes = line.replace("\"","")
#attributes = attributes.replace("\n","")
#attributes = attributes.split("\t")
#for index in attributes:
#	attribute = '@attribute ' + index
#	if index == 'class':
#		attribute += ' {' + nclasses + '} \n\n' 
#	else:
#		attribute +=' numeric \n' 
#	arff.write(attribute)

#arff.write('@data\n')

#while(len(line) > 0):
#	line = txt.readline()
#	sample = line.split("\t")
#	sample.pop(0)
#	if len(line) > 0:
#		sample[len(sample)-1] = str(int(sample[len(sample)-1]))
		
#	data = ",".join(sample)
#	arff.write(data + "\n")
