import numpy as np
import os
import psana

# experiment parameters

class experiparams:

    def __init__(self, experimentName, runNumber, detectorName=None):
        
        self.experimentName = experimentName        # cxic0415  
        self.runNumber = runNumber                  # 98  
        self.detectorName = detectorName            # self.parent.detAlias = self.getDetectorAlias(str(self.parent.detInfo))  
        self.username = os.environ['USER']
        self.paraDir = os.path.dirname(os.path.realpath(__file__))
        self.outDir = None
        self.setDefaultPath() 


    def setDefaultPath(self):
        if self.outDir is None or not os.path.isdir(self.outDir):
            self.outDir = '/reg/d/psdm/'+self.experimentName[:3]+'/'+self.experimentName+'/scratch/'+str(self.username)+'/automation'
        self.cxiDir = self.outDir+'/r'+str(self.runNumber).zfill(4)
        self.logDir = self.outDir+'/logs/r'+str(self.runNumber).zfill(4)
        self.runDir = self.cxiDir
        

    def setDefaultPsana(self):
        try: 
            ds = psana.DataSource("exp="+self.experimentName+":run="+str(self.runNumber)+':idx')
        except: 
            raise Exception('!!!!! Invalid experiment name or run number')

        run = ds.runs().next()
        env = ds.env()
        times = run.times()
        det = psana.Detector(self.detectorName)
        epics = ds.env().epicsStore()
        counter = 0
        evt = None
        while evt is None:
            evt = run.event(times[counter])
            counter += 1

        self.clenEpics = str(self.detectorName)+'_z'              # detInfo_z
        self.instrument = det.instrument()        
        self.clen = epics.value(self.clenEpics) / 1000.
        self.detectorDistance = np.mean(det.coords_z(evt))*1.0e-6
        self.coffset = self.detectorDistance - self.clen
        self.pixelSize = det.pixel_size(run)*1.0e-6
