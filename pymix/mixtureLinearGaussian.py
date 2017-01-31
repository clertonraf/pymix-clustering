from numpy.linalg import linalg as la
import mixture
import numpy
import random
import copy

class EmptyComponent(mixture.MixtureError):
    """
    Raised if a Component is empty.
    """
    def __init__(self,message):
       self.message = message
    def __str__(self):
        return str(self.message)

class LinearGaussianDistribution(mixture.ProbDistribution):
	"""
	Linear Gaussian Distribution    
	"""

	def __init__(self,p, beta, sigma):
		"""
		Constructor

		@param p: dimensionality of the distribution
		@param beta: coeficiente
		@param sigma: desvio padrao do erro
		"""
		assert len(beta) == p, len(sigma) == 1
		self.p = p
		self.suff_p = p
		self.beta = numpy.array(beta, dtype='Float64')		# create a array (numpy) for variable beta
		self.sigma = numpy.array(sigma, dtype='Float64')	# create a array (numpy) for variable sigma
		self.freeParams = p + 1

	def __copy__(self):
		return LinearGaussianDistribution(self.p,self.beta, self.sigma)

	def __str__(self):
		return "LinearGaussian:  ["+str(self.beta)+", "+str(self.sigma) + "]"

	def __eq__(self,other):
		if not isinstance(other,LinearGaussianDistribution):
			return False
		if self.p != other.p:
			return False
		if not numpy.allclose( self.beta, other.beta ) or not numpy.allclose(self.sigma, other.sigma):        
			return False
		return True

	def pdf(self, data):
		if isinstance(data, mixture.DataSet):
			dt = data.internalData			
		elif isinstance(data, numpy.ndarray):
			dt = data
		else:		
			raise TypeError,"Unknown/Invalid input type."             

		# First column of data set of the matrix
		y = dt[:,0]
		# Matrix column of 1's concatenated with rest of columns of data set of the matrix
		x = numpy.concatenate((numpy.array([numpy.ones(len(dt))]).T, dt[:,1:]), axis=1)

		# Calculating the expoent (y - x*beta)^2 / (sigma)^2 
		exp = numpy.divide(numpy.power(numpy.subtract(y, numpy.dot(x, self.beta)),2), self.sigma[0] ** 2)
		# Calculating the factor 1/sqrt(2*pi*(sigma)^2)
		fat = 1 / (numpy.sqrt(2 * numpy.pi) * self.sigma[0])
		# Probability result
		res = numpy.log(fat) + exp
		return res

	def MStep(self,posterior,data,mix_pi=None):
		if isinstance(data, mixture.DataSet):
			dt = data.internalData
		elif isinstance(data,numpy.ndarray):
			dt = data
		else:
			raise TypeError, "Unknown/Invalid input to MStep."

		# First column of data set of the matrix
		y = dt[:,0]
		# Matrix column of 1's concatenated with rest of columns of data set of the matrix
		x = numpy.concatenate((numpy.array([numpy.ones(len(dt))]).T, dt[:,1:]), axis=1) 

		# Beta estimation
		xaux = numpy.array(numpy.multiply(x,numpy.matrix(posterior).T))

		beta_numerator = numpy.dot(xaux.T,y)
		beta_denominator = numpy.dot(xaux.T,x)
		
		try:
			self.beta = numpy.dot(numpy.linalg.inv(beta_denominator),beta_numerator)
		except la.LinAlgError:
			raise EmptyComponent, "Empty Component: Singular Matrix"

		# Sigma estimation
		y_x_betat = numpy.subtract(y, numpy.dot(x, self.beta.T))

		sigma_numerator = numpy.dot(numpy.multiply(y_x_betat,posterior), y_x_betat)
		sigma_denominator = posterior.sum()
                
		self.sigma[0] = numpy.sqrt( sigma_numerator / sigma_denominator )


	def sample(self):
		"""
		Samples from the Linear Gaussian Distribution
		"""
		s = [None] * self.p

		beta_zero = numpy.array([self.beta[0]]).T
		beta_lin = self.beta[1:]

		s[0] = 1
		# x's samples
		res = 1*self.beta[0]
		for i in range(1,self.p):
			s[i] = random.normalvariate(0, 1)
			res = res + self.beta[i]*s[i]

		# y sample
		s[0] = random.normalvariate(res, self.sigma[0])

		return s

	def sampleSet(self,nr):
		s = numpy.zeros((nr,self.p))
		for i in range(nr):
			x = self.sample()
			s[i,:] = x
		return s

	def isValid(self,x):
		if not len(x) == self.p:
			raise InvalidDistributionInput, "\n\tInvalid data: wrong dimension(s) "+str(len(x))+" in MultiNormalDistribution(p="+str(self.p)+")."
		for v in x:
			try:
				float(v)
			except (ValueError):
				raise InvalidDistributionInput, "\n\tInvalid data: "+str(x)+" in MultiNormalDistribution."

	def flatStr(self, offset):
		offset +=1
		return "\t"*offset+";LinearGaussian;"+str(self.p)+";"+str(self.mu.tolist())+";"+str(self.sigma.tolist())+"\n"        
