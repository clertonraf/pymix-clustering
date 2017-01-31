import mixture
import mixtureLinearGaussian
import TabDataSet
import numpy
import random
import copy
import optparse
import os
import sys
import pylab
from time import clock  
    
def runMixture(minCluster,maxCluster,data,dist,repetitions,iterations,stopCriteria):
        """
        Function that run the mixture model for a range of clusters
    
        @param minCluster: cluster minimal number
        @param maxCluster: cluster maximum number
        @param data: DataSet object
        @param dist: ProductDistribution of one component
        @param repetitions: number of repetitions
        @param iterations: EM iterations
        @param stopCriteria: EM stop criteria
    
        @return: models, NEC, BIC, AIC, classifies
        """
        models = [mixtureComponents(1, dist)]
        classifies = []
        #prior_matrix = getPairwiseConstrantMatrix(data, 2)
        #data.setPairwiseConstraints(None, prior_matrix)
        for k in range(minCluster,maxCluster+1):
            print "#################### MIXTURE CLUSTER %d ####################" % k
            # mixture model for k components with distribution dist
            train = mixtureComponents(k, dist)
            # finding the best model
            bestmix, previous_posterior = estimateWithReplication(train,data,repetitions,iterations,stopCriteria)
            models.append(bestmix)
            # classifying data
            classify = bestmix.classify(data, 0, 5, previous_posterior, 2)
            print "classify", classify, "\n"
            classifies.append(classify)
        NEC,BIC,AIC = mixture.modelSelection(data,models)
        return models, NEC, BIC, AIC, classifies

def getPairwiseConstrantMatrix(classes, prior_type):
    """
    @param data: TabDataSet object
    @param prior_type: 1 positive constr.
                       2 negative constr.
    """
    prior_matrix = []
    for class1 in classes:
        prior_row = []
        for class2 in classes:
            if class1 == class2:
                if prior_type == 1:
                    prior_row.append(1)
                else:
                    prior_row.append(0)
            else:
                if prior_type == 1:
                    prior_row.append(0)
                else:
                    prior_row.append(1)
        prior_matrix.append(prior_row)
    return prior_matrix

def runMixtureClassify(data, dist, cvArgs=None):
    """
    The function runs a classification for a mixture model
    
    @param data: TabDataSet object
    @param dist: distribution
    """

    n = data.noLabels #number of components
    pi = [1. / n] * n
    distributions = []
    for i in range(0, n):
        distributions.append(copy.deepcopy(dist))
    train = mixture.LabeledMixtureModel(n,pi,distributions)
    #train = mixture.LabeledMixtureModel(n,pi,[dist] * n)
    print "\nClasses", data.classes
    return leaveOneOut_CV(train, data, cvArgs)

def leaveOneOut_CV(mix, data, cvArgs = None):
    """
    The function performs the N-fold cross validation
   
    @param mixture: training mixture
    @param data: TabDataSet object
    
    @return: sensivity, specificity, precision, accuracy
    """
    true_classify = 0
    false_classify = 0
    
    classify_lst = []
    
    if cvArgs:
        data.setPairwiseConstraints(None, cvArgs.prior_matrix)
        #for row in cvArgs.prior_matrix:
            #print row
    
    coOcurrence_matrix_lst = [] 
    bestmix = None
    train_error = []
    for sample in range(0, data.N):
        
        train = copy.deepcopy(data)
        print sample
        train.removeSamples([sample])
        if sample == 1:
        	sys.exit(2)
        previous_posterior = None
        cm_argmax = None
        argmax = None
        if cvArgs:
            model = mixtureComponents(1, cvArgs.dist)
            train.internalInit(model)
            classifies = []
            for k in range(cvArgs.min_cluster,cvArgs.max_cluster+1):
                print "#################### MIXTURE CLUSTER %d ####################" % k
                training = mixtureComponents(k, cvArgs.dist)
                bestmix, previous_posterior = estimateWithReplication(training,train,cvArgs.repetitions,cvArgs.iterations,cvArgs.stopCriteria)
                print "\nCLASSES", train.classes
                argmax=list(numpy.argmax(previous_posterior, axis=0))
                print "ARGMAX ", argmax
                print "\nsample", sample, "of", len(data.classes)-1, "samples\n"
                cm_argmax, cm = confusionMatrixArgmax(data.noLabels, bestmix.G, train.classes, list(argmax))
                print "Confusion Matrix\n", cm
                print "ARGMAX - Confusion Matrix\n", cm_argmax
                true_train = 0
                false_train = 0
                for index in range(0, len(argmax)):
                    if train.classes[index] == mapClassify(cm_argmax, argmax[index]):
                        true_train +=1
                    else:
                        false_train +=1
                        print "False value: sample", index, "\n"
                training_error = 1-(true_train/float(false_train+true_train))
                    
                train_error.append(training_error)
                print "\nTraining error", training_error, "%\n"
                
                #print "Co-Occurence Matrix"
                #print numpy.array(cOccMatrix)
                #for row in cOccMatrix:
                #    print row
        else:
            classify_mix = copy.deepcopy(mix)
            train.internalInit(classify_mix)
            classify_mix.modelInitialization(train)
            print "classify_mix.classify(train):", classify_mix.classify(train)
        
        test = copy.deepcopy(data)
        test.removeSamples(train.sampleIDs)
        test.labels = []
        test.noLabels = 0
        classify = None
        if cvArgs:
            test.internalInit(bestmix)
            p_post = numpy.zeros((bestmix.G,test.N),dtype='Float64')
            classify = bestmix.classify(test, 0, 10, p_post, 2) #test, prior_positive,prior_negative,previous_posterior,prior_type
            print "classify", classify
            mapped_classify = mapClassify(cm_argmax, classify[0])
            print "mapClassify", mapped_classify, "\n\n"
            argmax.insert(k, classify[0])
            cOccMatrix = getPairwiseConstrantMatrix(list(argmax), 1)
            coOcurrence_matrix_lst.append(numpy.array(cOccMatrix))
        else:
            test.internalInit(classify_mix)
            classify = classify_mix.classify(test, silent=0)
        #print "classify", classify
        
        if cvArgs:
            if data.classes[sample] == mapClassify(cm_argmax, classify[0]):
                true_classify +=1
                classify_lst.append(1)
            else:
                false_classify +=1
                classify_lst.append(0)
                print "False classify: sample", sample
        else:
            if data.classes[sample] == classify[0]:
                true_classify +=1
                classify_lst.append(1)
            else:
                false_classify +=1
                classify_lst.append(0)
    
    if cvArgs:
        sum_matrix = numpy.zeros((len(data.classes),len(data.classes)), dtype='Float64') 
        for arr in coOcurrence_matrix_lst:
            sum_matrix += arr
        print "\nFinal Co-Occurence", sum_matrix
    
        mean_train_error = sum(train_error)/float(len(train_error))
    
        print "\nMean Training Error",mean_train_error
    else:
        mean_train_error = -1
        sum_matrix = -1
    
    accuracy = true_classify / float(true_classify+false_classify)
    print "\nLearning vector:", classify_lst, "\n"
    print "\nAccuracy", accuracy,"\n"
    
    return accuracy, mean_train_error, sum_matrix

def mapClassify(cm_argmax, number):
    return cm_argmax[number]

def confusionMatrixArgmax(noLabels, G, classes, argmax):
    
    cm = numpy.zeros((G, noLabels),dtype='Float64')
    for i in range(0, len(classes)):
        cm[argmax[i], classes[i]]+=1
    sum_cm = cm.sum(axis=0)
    cm_t = cm.transpose()
    print "Original cm \n", cm
    for index in range(0, len(sum_cm)):
        sum_cm[index] = 1/float(sum_cm[index])
        cm_t[index] = cm_t[index]*sum_cm[index]
    cm=cm_t.transpose()
    print "Sum Confusion Matrix ArgMax", sum_cm
    return list(numpy.argmax(cm, axis=1)), cm

def mixtureComponents(n,dist):
        """
        Function that return a MixtureModel with n components of dist distribution
    
        @param n: number of components
        @param dist: ProductDistribution of one component
    
        @return: MixtureModel with n components of dist distribution
        """
        pi = [1. / n] * n
        distributions = []
        for i in range(0, n):
            distributions.append(copy.deepcopy(dist))
        train = mixture.ConstrainedMixtureModel(n,pi,distributions)
        return train
    
def estimateWithReplication(_mixture, data, repetitions, iterations, stopCriteria):
        """
        Function replicating em estimation and returning maximum likelihood replicate
    
        @param _mixture: MixtureModel object
        @param data: DataSet object
        @param repetitions: number of repetitions
        @param iterations: EM iterations
        @param stopCriteria: EM stop criteria
    
        @return: mixture best
        """
        print 'repetitions',repetitions
        print 'iterations',iterations
        print 'stopCriteria',stopCriteria
        
        mixtureBest = []
        max = -float("inf");
        for j in range(repetitions):
            try:
                maux = copy.copy(_mixture)
                previous_posterior = maux.modelInitialization(data, 0, 100, 2)
                [l,log_l] = maux.EM(data,iterations,stopCriteria, 0, 100,previous_posterior,  2)
                if log_l > max:
                   l_max = l
                   max = log_l
                   mixtureBest = maux
            except mixture.ConvergenceFailureEM:
                pass
            except mixtureLinearGaussian.EmptyComponent:
                print "Empty Component"
            except mixture.InvalidPosteriorDistribution as ipd:
                print ipd, '\n'
        if mixtureBest == []:
            raise mixture.ConvergenceFailureEM,"Convergence failed."
        return mixtureBest, l_max

def createDistribution(data, distribution):
    # creating a component
    p = data.p
    # type of distribution
    dist = None
    if distribution == 'normal':
        p = []
        for i in range(data.p):
            p.append(mixture.NormalDistribution(0,1))
        dist = mixture.ProductDistribution(p)
    else:     
        sigma = [1]
        beta = []       
        for i in range(data.p):
            beta.append(random.normalvariate(0,1))
        dist = mixture.ProductDistribution([mixtureLinearGaussian.LinearGaussianDistribution(p, beta, sigma)])

    return dist
    
def main():
        t1 = clock()
        # parse command line options
        usage = "Usage: %prog [options] arg1 arg2...\nTry %prog -h or %prog --help to see the available options"
        parser = optparse.OptionParser(usage)
        parser.add_option('-f', '--file', type="string", dest="filename", default=None, help="Path to datafile")
        parser.add_option('-d', '--distribution', type="string", dest="distribution", default=None, help="Type of distribution")
        parser.add_option('-m', '--max-cluster', type="int",  dest="max_cluster", default=2, help="Cluster maximum number [default:%default]")
        parser.add_option('-r', '--repetitions', type="int",  dest="repetitions", default=15, help="Number of repetitions [default:%default]")
        parser.add_option('-i', '--iterations', type="int",  dest="iterations", default=10, help="EM iterations [default:%default]")
        parser.add_option('-s', '--stop-criteria', type="float",  dest="stop_criteria", default=0.1, help="EM stop criteria [default:%default]")
        parser.add_option('-p', '--pairwise-constraint', action="store_true", dest="pairwise_constraint", default=False,  help="Pairwise constraint [default:%default]")
        parser.add_option('-l', '--log', action="store_true", dest="log_matrix", default=False, help="Log of each matrix value [default:%default")
        parser.add_option('--classify', action="store_true", dest="classify", default=False)
        options, args = parser.parse_args()
    
        filename = options.filename
        min_cluster = options.max_cluster
        max_cluster = options.max_cluster
        repetitions = options.repetitions
        iterations = options.iterations
        stop_criteria = options.stop_criteria
        data = None
        distribution = options.distribution
        
        random.seed(3586662)
        
        if (max_cluster == None or filename == None):
            sys.exit(2)
    
        if (os.path.exists(filename)):
            data = TabDataSet.TabDataSet()
            print filename
            data.fromFile(filename)
            if(options.log_matrix):
                data.logTransform()
        else:
            print "Input data file does not exist."
            sys.exit(2)
        
        dist = createDistribution(data, distribution)
        
        if options.classify:
            class CVArgs:
                def __init__(self):
                    self.repetitions = repetitions
                    self.iterations = iterations
                    self.stopCriteria = stop_criteria
                    self.min_cluster = min_cluster
                    self.max_cluster = max_cluster
                    self.prior_type = 2
                    self.prior_matrix = getPairwiseConstrantMatrix(data.classes, self.prior_type)
                    self.dist = dist
            if options.pairwise_constraint:
                accuracy, mean_train_error, sum_matrix = runMixtureClassify(data, dist, cvArgs = CVArgs())
                newfilename = "_occurrenceMatrix"+str(min_cluster)+".txt"
                filename = filename.replace(".txt", newfilename)
                f = open(filename, "w")
                numpy.savetxt(f, sum_matrix, fmt="%i", delimiter='\t')
            else:
                runMixtureClassify(data, dist)
            t2 = clock()
            print "execution time = ", t2-t1, "seconds"
        else: 
            # run the main funcition
            models, NEC, BIC, AIC, classifies = runMixture(min_cluster, max_cluster, data, dist, repetitions, iterations, stop_criteria)
    
            clusters = range(1, max_cluster + 1)
            bestmodel = BIC.index(max(BIC))
    
            #NEC = numpy.array(NEC)
            BIC = -numpy.array(BIC)
            AIC = -numpy.array(AIC)
    
            #pylab.plot(NEC, label="NEC")
            #pylab.semilogy(clusters, BIC, label="BIC")
            #pylab.semilogy(clusters, AIC, label="AIC")
            #pylab.xlabel('clusters')
            #pylab.legend()
            #pylab.savefig(filename[:-4] + "_BIC_AIC.pdf")
    
            if bestmodel == 0:
                data.setNotes([0] * data.N)
            else: 
                data.setNotes(classifies[bestmodel-1])
            data.writeFile(filename[:-4] + "_classifies_" + str(clusters[bestmodel]) + ".txt")
    
            # printing results
            print ""
            print "#################### Models ####################\n", models, "\n"
            print "##################### NEC ######################\n", NEC, "\n"
            print "##################### BIC ######################\n", BIC, "\n"
            print "##################### AIC ######################\n", AIC, "\n"
            print "################## Classifies ##################\n", classifies, "\n"
        
if __name__ == "__main__":
        main()
