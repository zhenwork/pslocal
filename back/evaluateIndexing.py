from scipy import stats
import numpy as np 
from streamManager import *
import utils as utils
    
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
        return [score]*6  
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


def volumeFilter(_lattice):
    """
    Lattice constants can be different, but single-unit-cell volume is the same
    """
    lattice = _lattice.copy()
    (nx,ny) = lattice.shape
    if nx < 20: 
        print "@@@@@ no enough crystals" 
        return lattice

    Volume = []
    for ii in range(nx):
        singleVolume = utils.latticeVolume(lattice[ii,0].copy(), \
                              lattice[ii,1].copy(), \
                              lattice[ii,2].copy(), \
                              lattice[ii,3]/180.*np.pi, \
                              lattice[ii,4]/180.*np.pi, \
                              lattice[ii,5]/180.*np.pi )
        Volume.append(singleVolume)

    Volume = np.array(Volume)
    # Vmedian = np.nanmedian(V)
    (hist, sampling) = np.histogram(Volume, bins=int(np.amax(Volume)/10000))
    Vcenter = sampling[np.argmax(hist)+1]

    index = np.where((Volume > Vcenter*0.9)*(Volume < Vcenter*1.1) == True)
    if len(index[0]) < 5:
        print "@@@@@ no enough crystals" 
        return lattice

    lattice = lattice[index].copy()
    print '##### volume filtering: ori -> now: ', nx,'->',len(lattice)

    return [lattice, Volume]
    
    
def evaluateIndexing(streamfile, withpdb=True):
    
    indexHistogram = getIndexHistogram(streamfile)
    lattice = indexHistogram[:,9:15].copy()
    print "##### numIndex: ", len(lattice)
    if not withpdb:
        lattice = volumeFilter(lattice)

    skewness, kurtosis = evaluateSkewKurt(lattice[:,0], lattice[:,1], lattice[:,2], lattice[:,3], lattice[:,4], lattice[:,5])
    print "##### skewness: ", skewness 
    print "##### kurtosis: ", kurtosis
    score = scoreIndexing(skewness, kurtosis)
    
    return score
    
    

    
    
