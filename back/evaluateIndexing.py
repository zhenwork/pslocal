import numpy as np 
from streamManager import *

	
def countIndexNumber(streamfile):
	indexHistogram = getIndexHistogram(streamfile)
	return len(indexHistogram)
	

def getIndexHistogram(streamfile):
	"""
	Using stream manager to extract information.
	
	TODO: 
	1. the stream manager may be slow, may need updates
	"""
	sm = iStream() 
	sm.initial(streamfile)
	sm.get_label()
	sm.get_info()
	indexHistogram = sm.crystal
	sm.clear()	
	return indexHistogram


def scoreIndexing(skewness, kurtosis, numIndex=None):
	"""
	1. Higher score means better distribution;
	2. Score can be negative;
	
	TODO: 
	1. take numIndex into consideration
	"""
	
	score = -999.
	if skewness is None or kurtosis is None:
		return score  
	score = kurtosis/2. - np.abs(skewness)
	return score 


def evaluateSkewKurt(a,b,c,alpha,beta,gamma):
	
	skewness = [None]*6
	kurtosis = [None]*6
	
	if len(a) < 50:
		return None, None
	
	skewness[0] = np.abs(scipy.stats.skew(a))
	skewness[1] = np.abs(scipy.stats.skew(b))
	skewness[2] = np.abs(scipy.stats.skew(c))
	skewness[3] = np.abs(scipy.stats.skew(alpha))
	skewness[4] = np.abs(scipy.stats.skew(beta))
	skewness[5] = np.abs(scipy.stats.skew(gamma))
	
	kurtosis[0] = scipy.stats.kurtosis(a)
	kurtosis[1] = scipy.stats.kurtosis(b)
	kurtosis[2] = scipy.stats.kurtosis(c)
	kurtosis[3] = scipy.stats.kurtosis(alpha)
	kurtosis[4] = scipy.stats.kurtosis(beta)
	kurtosis[5] = scipy.stats.kurtosis(gamma)
	
	return np.array(skewness), np.array(kurtosis)


def volumeFilter(lattice):
	"""
	Lattice constants can be different, but single-unit-cell volume is the same
	"""
	return True
	
	
def evaluateIndexing(streamfile):
	
	indexHistogram = getIndexHistogram(streamfile)
	lattice = indexHistogram[9:15].copy()
	
	skewness, kurtosis = evaluateSkewKurt(lattice[:,0], lattice[:,1], lattice[:,2], lattice[:,3], lattice[:,4], lattice[:,5])
	
	score = scoreIndexing(skewness, kurtosis)
	
	return score
	
	

	
	
