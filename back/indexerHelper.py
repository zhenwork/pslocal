import numpy as np 
import copy 
from expParams import experiparams


def indexCommand(experimentName=None, runNumber=None, detectorName=None, geomfile=None, outDir=None, \
                 queue=None, pixelSize=None, instrument=None, coffset=None, clenEpics=None, \
                 peakMethod='cxi', intRadius='3,4,5', indexingMethod='dirax', minPeaks=15, \
                 maxPeaks=2048, minRes=-1, tolerance='5,5,5,1.5', tag="", pkTag="", \
                 indexsample='crystal', chunkSize=200, indexnoe=-1, logger='False', \
                 keepData='True', likelihood=0, pdbfile=None):

    command = "indexCrystals" + \
            " -e " + experimentName + \
            " -d " + detectorName + \
            " --geom " + geomfile + \
            " --peakMethod " + peakMethod + \
            " --integrationRadius " + intRadius + \
            " --indexingMethod " + indexingMethod + \
            " --minPeaks " + str(minPeaks) + \
            " --maxPeaks " + str(maxPeaks) + \
            " --minRes " + str(minRes) + \
            " --tolerance " + str(tolerance) + \
            " --outDir " + str(outDir) + \
            " --sample " + indexsample + \
            " --queue " + queue + \
            " --chunkSize " + str(chunkSize) + \
            " --noe " + str(indexnoe) + \
            " --instrument " + instrument + \
            " --pixelSize " + str(pixelsize) + \
            " --coffset " + str(coffset) + \
            " --clenEpics " + clenEpics + \
            " --logger " + str(logger) + \
            " --keepData " + str(keepData) + \
            " --likelihood " + str(likelihood) + \
            " --tag " + str(tag) + \
            " --pkTag " + str(pkTag)

    if pdbfile is not None and os.path.isfile(pdbfile): 
        command += " --pdb " + pdbfile

    command += " --run " + str(runNumber)

    return command


class GeoFileManager:

    def __init__(self, experimentName=None,runNumber=None,detectorName=None):
        self.experimentName = experimentName
        self.runNumber = runNumber
        self.detectorName = detectorName
        self.loadPsanaGeo()

    def loadPsanaGeo(self):
        self.params = experiparams(self.experimentName, self.runNumber, detectorName=self.detectorName)
        self.params.setDefaultPsana() 
        self.detectorDistance = params.detectorDistance
        self.coffset = params.coffset
        self.clen = params.clen 

    def changeCenter(self, fromfile=None, newCenter=None, tofile=None):
        if tofile is None:
            tofile = self.input + "-newCenter-"+str(newCenter)
        return True
        
    def changeCoffset(self, newCoffset, fromfile=None, tofile=None):

        if fromfile is None:
            fromfile = self.params.cxiDir + "/.temp.geom"
        if tofile is None:
            tofile = self.input + "-newCoffset-"+str(newCoffset)
        if fromfile is None:
            fromfile = self.geomfile
            
        f = open(fromfile, 'r')
        content = f.readlines()
        f.close()

        f = open(tofile, 'w')
        for i, val in enumerate(content):
            if 'coffset =' in val: 
                content[i] = val.split('=')[0]+"= "+str(newCoffset)+'\n'
        f.writelines(content)
        f.close()

        self.geomfile = tofile 

        print "##### old geom: ", fromfile
        print "##### old params: distance=%f / coffset=%f / clen=%f"%(self.detectorDistance, self.coffset, self.clen) 

        self.coffset = newCoffset
        self.detectorDistance = self.coffset + self.clen 

        print "##### new geom: ", tofile
        print "##### new params: distance=%f / coffset=%f / clen=%f"%(self.detectorDistance, self.coffset, self.clen) 

        return tofile

    def changeDistance(self, newDistance, fromfile=None, tofile=None):

        if fromfile is None:
            fromfile = self.params.cxiDir + "/.temp.geom"
        if tofile is None:
            tofile = self.input + "-newDistance-"+str(newDistance)
        if fromfile is None:
            fromfile = self.geomfile

        self.detectorDistance = newDistance
        self.coffset = self.detectorDistance - self.clen 

        f = open(fromfile, 'r')
        content = f.readlines()
        f.close()

        f = open(tofile, 'w')
        for i, val in enumerate(content):
            if 'coffset =' in val: 
                content[i] = val.split('=')[0]+"= "+str(self.coffset)+'\n'
        f.writelines(content)
        f.close()

        self.geomfile = tofile 

        print "##### old geom: ", fromfile
        print "##### old params: distance=%f / coffset=%f / clen=%f"%(self.detectorDistance, self.coffset, self.clen) 

        print "##### new geom: ", tofile
        print "##### new params: distance=%f / coffset=%f / clen=%f"%(self.detectorDistance, self.coffset, self.clen) 

        return tofile


class IndexHelper:

    def __init__(self, experimentName, runNumber, detectorName):
        self.experimentName = experimentName
        self.runNumber = runNumber
        self.detectorName = detectorName 
        
    def setDefaultParams(self):
        params = experiparams(self.experimentName, self.runNumber, detectorName=self.detectorName)
        params.setDefaultPsana()
        
        self.queue = 'psanaq' 
        self.outDir = params.cxiDir
        self.indexnoe = -1
        self.pkTag = ""
        self.instrument = params.instrument
        self.pixelSize = params.pixelSize 
        self.pdbfile = None


    def indexCommand(self, geoManager):
        self.tag = "index-distance-"+str(round(params.detectorDistance*1000., 2)) 
        
        geoManager = GeoFileManager(self.geomfile)
        geoManager.changeCoffset(newCoffset=params.coffset)
        
        cmd = indexCommand(experimentName=self.experimentName, runNumber=self.runNumber, \
                           detectorName=self.detectorName, geomfile=geoManager.geomfile, \
                           outDir=self.outDir, queue=self.queue, pixelSize=self.pixelSize, \
                           instrument=self.instrument, coffset=self.coffset, clenEpics=self.clenEpics, \
                           tag=self.tag, pkTag = self.pkTag, pdbfile=self.pdbfile)
        
        return cmd 
        

