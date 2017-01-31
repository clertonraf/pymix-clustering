from os import *
from time import clock  
import optparse
import os

usage = "Usage: %prog [options] arg1 arg2...\nTry %prog -h or %prog --help to see the available options"
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--input-directory', type="string", dest="inputdir", default=None, help="Path to input datafile")
parser.add_option('-o', '--target-directory', type="string", dest="outputdir", default=None, help="Path to output datafile")
options, args = parser.parse_args()

inputdir = options.inputdir
outputdir = options.outputdir

for file in listdir(inputdir):
        print "File:",file
        filename = file.replace('.txt','')
        filepath = sep + filename
        inputpath = inputdir + filepath + '.txt' 
        outputpath = outputdir + sep+ "result.txt" 
        comando = "python mixtureTools.py -d normal -f "+inputpath+" --classify >> "+outputpath
        os.system(comando)
	
