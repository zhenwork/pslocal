"""
1. process actions
"""
import time
import shlex
import datetime
from fileManager import *
import subprocess as sp
zf = iFile()


class actionManager:
    def __init__(self, actionID, actionName, runList):
        self.status = 'start'
        self.actionName = actionName
        self.actionID = actionID
        self.runList = runList
        self.path = "/reg/d/psdm/cxi/cxic0415/scratch/tmpData/logFile/actionfile-%s-%s.pickle" % (self.actionName, self.actionID)
        self.actionfile = '/reg/d/psdm/cxi/cxic0415/scratch/tmpData/logFile/actionfile.json'
        self.startTime = self.getTime()
        self.stopTime = None
        self.jobID = {}   ## ID:'running'
        
        
    def start(self):
        self.save()
        sleepTime = 0
        
        while True:
            self = self.reload()
            
            if self.status.lower() == 'stop':
                self.stopTime = self.getTime()
                self.flush()
                break
            elif self.status.lower() == 'complete':
                print ">>>>> %s-%s is complete"%(self.actionID, self.actionName)
                self.stopTime = self.getTime()
                self.flush()
                break
            elif self.status.lower() == 'running':
                print ">>>>> %s-%s is running"%(self.actionID, self.actionName)
                self.checkStatus() 
                sleepTime = min(sleepTime+1, 10)
                time.sleep(sleepTime)
                continue
            elif self.status.lower() == 'sleep': 
                self.sleep()
                continue
            elif self.status.lower() == 'resume':
                self.status = 'running'
                self.save()
                continue
            elif self.status.lower() == 'fail':
                self.stopTime = self.getTime()
                self.flush()
                break
            elif self.status.lower() == 'start':
                pass
            else:
                print '>>>>> unknown status of %s'%self.actionID
                self.stopTime = self.getTime()
                self.flush()
                break
                
            assert self.status.lower() == 'start'
            
            launchAction = self.getLaunchFunction(self.actionName)
            status = launchAction()
            assert status
            
            self.status = 'running'
            self.save()
            self.flush()
            time.sleep(5)
        
        
    

    def getLaunchFunction(self, actionName):
        if actionName == 'setup':
            return self.launchSetup
        if actionName == 'fast-powder':
            return self.launchFastPowder
        if actionName == 'optz-center':
            return self.launchOptimizeCenter
        if actionName == 'optz-detz':
            return self.launchOptimizeDistance
        if actionName == 'optz-unitcell':
            return self.launchOptimizeUnitcell
        if actionName == 'merge-stream':
            return self.launchMergeStream
        if actionName == 'peakfinder':
            return self.launchPeakFinder
        if actionName == 'indexer':
            return self.launchIndexer
        if actionName == 'pointless':
            return self.launchPointless
        if actionName == 'gen-mtz':
            return self.launchGenerateMTZ
        if actionName == 'run-niggli':
            return self.launchRunNiggli
        return lambda: None
        

    def getTime(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S.%f')


    def save(self):
        while True:
            if zf.save_pickle(self, self.path): break
            else: pass
    
    
    def reload(self):
        while True:
            para = zf.load_pickle(self.path)
            if para: return para
            else: pass
    

    def flush(self):
        if not os.path.isfile(self.actionfile):
            actions = {}
        else:
            actions = zf.load_json(self.actionfile)

        if self.actionID not in actions:
            actions[self.actionID] = {}
            
        actions[self.actionID]['action'] = self.actionName
        actions[self.actionID]['runList'] = self.runList
        actions[self.actionID]['params'] = {} 
        actions[self.actionID]['startTime'] = self.startTime
        actions[self.actionID]['stopTime'] = self.stopTime
        actions[self.actionID]['status'] = self.status
        
        while True:
            if zf.save_json(actions, self.actionfile): break
            else: pass
        #print ">>>>> saved action file: %s"%self.actionfile
    
    
    def readActionFile(self):
        while True:
            actions = zf.load_json(self.actionfile)
            if actions: return actions
            else: pass


    def stop(self):
        self.status = 'stop'
        self.save()


    def setSleepTime(self, sleepTime=300):
        self.status = 'sleep'
        self.sleepTime = sleepTime
        self.save()


    def sleep(self):
        tic = time.time()
        while True:
            self = self.reload()
            if time.time() - tic > self.sleepTime:
                return True
            if self.status == 'resume':
                self.setStatus('running')
                self.save()
                return True
            time.sleep(30)
        
        
    def resume(self):
        self.status = 'resume'
        self.save()


    def silent(self, silent):
        if not isinstance(silent, bool):
            return False
        self.silent = bool(silent)
        self.save()


    def iprint(self, *arg):
        if self.silent: 
            return False
        if not isinstance(arg, tuple):
            print arg 
            return True
        for each in arg:
            if isinstance(each, dict):
                for dictkey in sorted(each):
                    print dictkey, each[dictkey]
            else:
                print each
        return True
        

    def checkActionStatus(self):




    def getRunStatistics(self, runNumber):
        
        return


    def getStatistics(self, runList=[]):
        if len(runList) == 0:
            return None
        return


    def postStatistics(self, fsave):

        return 
        

    def launchSetup(self):
        print ">>>>> we are in launchsetup ", self.runList
        
        try:
            cmd = "python ./runSetup.py --exp %s --run %d --detInfo %s" % (self.experimentName, self.runNumber, self.det)
            p = sp.Popen(shlex.split(cmd))
            return True
        except Exception as err: 
            print "!!!!! ERROR MESSAGE: ", err
            self.status = 'fail'
            self.flush()
            self.save()
            return False
        
        
    def launchFastPowder(self):
        print ">>>>> we are in launchFastPowder", self.runList
        
        try:
            cmd = "bsub -q psanaq -x -n 24 -o .%J.log mpirun python ./runPowderSum.py --exp %s --run %d" % (self.experimentName, self.runList)
            p = sp.Popen(shlex.split(cmd))
            return True
        except Exception as err: 
            print "!!!!! ERROR MESSAGE: ", err
            self.status = 'fail'
            self.flush()
            self.save()
            return False
        
        
        
    def launchOptimizeCenter(self):
    
        return
        
        
        
    def launchOptimizeDistance(self):
        print ">>>>> we are in launchOptimizeDistance", self.runList

        try:
            cmd = "python ./indexerCommand.py --exp %s --run %d" % (self.experimentName, self.runList)
            p = sp.Popen(shlex.split(cmd))
            return True
        except Exception as err: 
            print "!!!!! ERROR MESSAGE: ", err
            self.status = 'fail'
            self.flush()
            self.save()
            return False
        
        
    def launchOptimizeUnitcell(self):
        return
        
        
        
    def launchMergeStream(self):    
        print ">>>>> we are in merge-stream", self.runList
        return True
        
        
        
    def launchPeakFinder(self):
        return
        
        
        
    def launchIndexer(self):
        return
        
        
        
    def launchPointless(self):
        return
        
        
        
    def launchGenerateMTZ(self):
        print ">>>>> we are in gen-mtz", self.runList
        return True
        
        
        
    def launchRunNiggli(self):
        return
            
            

