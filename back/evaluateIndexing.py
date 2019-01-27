from scipy import stats
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
	score = kurtosis/4. - np.abs(skewness)
	return score 


def evaluateSkewKurt(a,b,c,alpha,beta,gamma):
	
	skewness = [None]*6
	kurtosis = [None]*6
	
	if len(a) < 50:
		return None, None
	
	skewness[0] = stats.skew(a)
	skewness[1] = stats.skew(b)
	skewness[2] = stats.skew(c)
	skewness[3] = stats.skew(alpha)
	skewness[4] = stats.skew(beta)
	skewness[5] = stats.skew(gamma)
	
	kurtosis[0] = stats.kurtosis(a)
	kurtosis[1] = stats.kurtosis(b)
	kurtosis[2] = stats.kurtosis(c)
	kurtosis[3] = stats.kurtosis(alpha)
	kurtosis[4] = stats.kurtosis(beta)
	kurtosis[5] = stats.kurtosis(gamma)
	
	return np.array(skewness), np.array(kurtosis)


def volumeFilter(lattice):
	"""
	Lattice constants can be different, but single-unit-cell volume is the same
	"""
	return True
	
	
def evaluateIndexing(streamfile):
	
	indexHistogram = getIndexHistogram(streamfile)
	lattice = indexHistogram[:,9:15].copy()
	
	skewness, kurtosis = evaluateSkewKurt(lattice[:,0], lattice[:,1], lattice[:,2], lattice[:,3], lattice[:,4], lattice[:,5])
	print "##### numIndex: ", len(lattice)
	print "##### skewness: ", skewness 
	print "##### kurtosis: ", kurtosis
	score = scoreIndexing(skewness, kurtosis)
	
	return score
	
	

	
	
