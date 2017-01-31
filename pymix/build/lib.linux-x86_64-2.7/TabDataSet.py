import mixture
import copy
import numpy

class TabDataSet(mixture.ConstrainedDataSet):
        """
        Class TabDataSet
        """

        def __init__(self, *argv):
            mixture.ConstrainedDataSet.__init__(self, *argv)
            self.sampleNotes = [] # Annotations

        def setNotes(self, notes):
            self.sampleNotes = notes		
            
        def getHeaders(self):
            return self.headers

        def __copy__(self):
            """
            Interface to copy.copy function.
            @return: deep copy of 'self'
            """
            cop = TabDataSet()

            cop.N = self.N    
            cop.p = self.p
            cop.sampleIDs = copy.copy(self.sampleIDs)
            cop.sampleNotes = copy.copy(self.sampleNotes)
            cop.headers = copy.copy(self.headers)
            cop.dataMatrix = copy.deepcopy(self.dataMatrix)
            cop.internalData = copy.deepcopy(self.internalData)
            cop.classes = copy.deepcopy(self.classes)
            cop.labels = copy.deepcopy(self.labels)
            cop.noLabels = copy.copy(self.noLabels)
            cop.pairwisepositive = copy.deepcopy(self.pairwisepositive)
            cop.pairwisenegative = copy.deepcopy(self.pairwisenegative)

            cop._internalData_views = copy.deepcopy(self._internalData_views) # XXX

            cop.suff_dataRange = copy.copy(self.suff_dataRange)
            cop.suff_p = self.suff_p
            cop.suff_p_list = copy.deepcopy(self.suff_p_list)
            return cop

        def removeSamples(self, ids, silent = 1):
            """
            Remove a list of samples from the data set.
            
            @param ids: list of sample identifiers 
            @param silent: verbosity control
            """
            if self.internalData:
                print "Warning: internalInit has to be rerun after removeSamples."
                self.internalData = None
                self.suff_dataRange = None
                self.suff_p = None
                self.suff_p_list = []
            
            remove_lst = []
            for lst in range(0, len(self.labels)):
                remove_lst.append([0])
            
            for si in ids:
                for lst in range(0, len(self.labels)):
                    if si in self.labels[lst] :
                        remove_lst[lst][0] +=1
            #print "removal list", remove_lst
            
            for lst in range(0, len(remove_lst)):
                if remove_lst[lst][0] > 0:
                    n = remove_lst[lst][0]
                    for i in range(0, n):
                        index = self.labels[lst].pop()
                        for j in range(0, len(self.labels)):
                            for m in range(0, len(self.labels[j])):
                                if self.labels[j][m] > index:
                                    self.labels[j][m]-=1
                    
            #print "after removal", self.labels
            for si in ids:
                sind = self.sampleIDs.index(si)
                self.dataMatrix.pop(sind)
                self.sampleIDs.pop(sind)
                self.classes.pop(sind)
                
                if self.pairwisenegative:
                    print 'self.pairwisenegative',self.pairwisenegative
                    self.pairwisenegative.pop(sind)
                    for row in self.pairwisenegative:
                        row.pop(sind)
                if self.pairwisepositive:
                    self.pairwisepositive.pop(sind)
                    for row in self.pairwisepositive:
                        row.pop(sind)
            #print "classes", self.classes
            if not silent:
                print 'Samples '+str(ids)+' removed'
            
            self.N = self.N - len(ids)


        def fromArray(self, array, IDs = None, col_header = None, notes = None):
            super(TabDataSet,self).fromArray(array,IDs,col_header)
            if notes:
                self.sampleNotes = notes
            else:
                self.sampleNotes = ['-'] * self.N

        def fromList(self,List, IDs = None, col_header = None):
            super(TabDataSet,self).fromList(List,IDs,col_header)
            if notes:
                self.sampleNotes = notes
            else:
                self.sampleNotes = ['-'] * self.N

        def fromFile(self, fileName):
            self.complex = 0
            self.seq_p = 0

            f = open(fileName,"r")

            self.sampleIDs = f.next().rstrip().split("\t")[1:]
            self.classes = f.next().rstrip().split("\t")[1:]

            #converting labels to numbers
            unique_classes = list(set(self.classes))
            
            constrainedClasses = []
            for u in range(0, len(unique_classes)):
                constrainedClasses.append(list())
                
            for c in range(0, len(self.classes)):
                for uc in range(0, len(unique_classes)):
                    if self.classes[c] == unique_classes[uc]:
                        self.classes[c] = uc
                        constrainedClasses[uc].append(c)
             
            matrix = []
            for line in f:

                row = line.rstrip().split('\t')
                
                self.headers.append(row[0])
                self.sampleNotes.append(row[1])
                
                data_lin = [float(item) for item in row[1:]]
                matrix.append(data_lin)
                #self.dataMatrix.append(data_lin)
            #print matrix
            array = numpy.array(matrix)
            array = array.transpose()
            self.fromArray(array)
            super(TabDataSet, self).setConstrainedLabels(constrainedClasses)
            #self.N = len(self.dataMatrix)

            # checking data-label consistency
            #for i in range(self.N):
             #   assert len(self.dataMatrix[i]) == len(self.headers), "Different numbers of headers and data columns in files " + str(fileNames) + ", sample " + str(self.sampleIDs[i]) + " ," + str(len(self.dataMatrix[i])) + " != " + str( len(self.headers))

            #self.p = len(self.dataMatrix[0])

        def __str__(self):
            """
            String representation of the TabDataSet

            @return: string representation
            """
            strout = "Data set overview:\n"
            strout += "N = "+ str(self.N) + "\n"
            strout += "p = "+str(self.p) + "\n\n"       
            strout +=  "sampleIDs = " + str(self.sampleIDs)+ "\n\n"
            strout +=  "sampleNotes = " + str(self.sampleNotes)+ "\n\n"
            strout += "headers = "+ str(self.headers)+ "\n\n"
            #strout += "dataMatrix = "+str(self.dataMatrix) + "\n"
            
            return strout

        def writeFile(self, filename):
            f = open(filename, 'w')
            f.write("ID\tNT\t")
            f.write(strTabList(self.headers) + "\n")
            for i in range(self.N):
                f.write(str(self.sampleIDs[i]) + "\t" + str(self.sampleNotes[i]) + "\t" + strTabList(self.dataMatrix[i]) + "\n")
            f.close() 
            
        def center(self,columns = None):
            dataAux = numpy.array(self.dataMatrix)
            if columns==None:
                columns=range(self.p)
            for c in columns:
                dataAux[:,c] = dataAux[:,c]- numpy.mean(dataAux[:,c])
            self.dataMatrix=dataAux.tolist()

        def logTransform(self,columns = None):
            dataAux = numpy.array(self.dataMatrix,dtype='Float64')
            if columns==None:
                columns=range(self.p)
            #print "log", columns
            for c in columns:
                dataAux[:,c] = numpy.log(dataAux[:,c]+1.0)
            self.dataMatrix=dataAux.tolist()


        def normalize(self,columns=None):
            dataAux = numpy.array(self.dataMatrix)
            if columns==None:
                columns=range(self.p)
            for c in columns:
                dataAux[:,c] = dataAux[:,c]/numpy.std(dataAux[:,c])
            self.dataMatrix=dataAux.tolist()


        def shuffle(self,columns=None):
            dataAux = numpy.array(self.dataMatrix)
            if columns==None:
                columns=range(self.p)
            for c in columns:
                numpy.random.shuffle(dataAux[:,c])
            self.dataMatrix=dataAux.tolist()

def strTabList(List):
        stres = str(List[0])
        for elem in List[1:]:
            stres += "\t" + str(elem)
        return stres
