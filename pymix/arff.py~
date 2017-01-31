class ArffFile():

    def __init__(self):
        """Construct an empty ARFF structure."""
        self.relation = ''
        self.attributes = []
        self.attribute_types = {}
        self.attribute_data = {}
        self.comment = []
        self.data = []
        pass
    
    def load(self,filepath):
        """Load an ARFF File from a file."""
        o = open(filepath)
        s = o.read()
        self.__parse(s)
    
    def __parse(self,s):
        isData = False
        countLines = 0
        for l in s.splitlines():
            countLines+=1
            if l.startswith('%'):
                self.comment.append(l[1:].strip())
            elif l.startswith('@relation'):
                l = l.split()
                self.relation = l[1]
            elif l.startswith('@attribute'):
                l = l.replace('\'','')
                l = l.replace(',',' ')
                l = l.replace('{','')
                l = l.replace('}','')
                l = l.split()
                self.attributes.append(l[1])
                aType = []
                for i in l[2:]:
                    aType.append(i)
                self.attribute_types[l[1]] = aType
            elif l.startswith('@data'):
                isData = True
            else:
                if isData:
                    l = l.replace('\'','')
                    l = l.replace(',',' ')
                    l = l.split()
                    self.data.append(l)
                elif len(l)>0:
                    print "Error in line "+str(countLines)+"!"
                    
        for i in range(0,len(self.data[0])):
            lst = []
            for j in self.data:
                lst.append(j[i])
            self.attribute_data[self.attributes[i]] = lst
            
    def writeTextFile(self,filepath,attributeClassName="class"):
        '''Parses a arff file into a \t separated text format'''
        myfile = open(filepath,'w')
        
        column_name = []
        for index in range(0,len(self.attribute_data[attributeClassName])):
            column_name.append('C'+str(index+1))
        column_name = '\t'.join(column_name)
        column_name = '\t' + column_name + '\n'
        myfile.write(column_name)
        
        class_name = '\t'.join(self.attribute_data[attributeClassName])
        class_name = '\t' + class_name + '\n'
        myfile.write(class_name)
        
        for key in self.attribute_data.keys():
            if key != attributeClassName:
                line = '\t'.join(self.attribute_data[key])
                line = key + '\t' + line + '\n'
                myfile.write(line)
        
if __name__ == '__main__':
    b = ArffFile()
    b.load('/home/craf/test1.arff')
    b.writeTextFile('test.txt')
