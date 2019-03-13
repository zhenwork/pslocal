import os,sys
import time

if "/reg/neh/home/zhensu/Develop/pslocal" not in sys.path:
    sys.path.append("/reg/neh/home/zhensu/Develop/pslocal")
    
import front.actionManager as actionManager

class AutoSFXSingle:
    """
    Three different Modes:
    1. known distance, known unit cell
    2. known distance, unknown unit cell
    3. unknown distance, known unit cell
    """
    def __init__(self, experimentName=None, detectorName=None, detectorDistance=None, pdbFile=None, runNumber=None, actionList=[]):
        self.known = {}
        self.known["experimentName"] = experimentName
        self.known["detectorDistance"] = detectorDistance
        self.known["detectorName"] = detectorName 
        self.known["pdb"] = pdbFile
        self.params = {}
        self.guess = {}
        self.actionObject = {}
        self.actionList = actionList
        self.runNumber = runNumber
        self.status = {}
        self.actionID = 1
    
    def setDefault(self):
        for action in self.actionList:
            self.params[action] = self.known.copy()
        return
    
    
    def checkActionFeasibility(self):
        if self.runNumber is None:
            return False 
        if self.known["experimentName"] is None or self.known["detectorName"] is None:
            return False
        if self.known["detectorDistance"] is None and self.known["pdb"] is None:
            return False
        return True
    
    
    def start2end(self):
        if not self.checkActionFeasibility():
            raise Exception("!! Not feasible")
        
        ## steup
        try:
            self.monitor( self.runSetup(), sleepTime=1e9 )
            self.monitor( self.runPowderSum(), sleepTime=1e9 )
            self.monitor( self.runFinderCenter(), sleepTime=1e9 )
            self.monitor( self.runPeakFinder(), sleepTime=1e9 )
            self.monitor( self.runIndexer(), sleepTime=1e9 )
            self.monitor( self.runEvaluateStream(), sleepTime=1e9 )
            self.monitor( self.runFindNiggli(), sleepTime=1e9 )
            return True
        except Exception as err:
            print err
            return False
    
    def runSetup(self):
        params = {}
        params["experimentName"] = self.known["experimentName"]
        params["detectorName"] = self.known["detectorName"]
        params["runNumber"] = self.runNumber
        params["mode"] = "local" 

        ActionManager = actionManager.ActionManager(actionName="ExpSetup", actionID=str(self.actionID).zfill(5), params=params)
        ActionManager.start()
        self.actionObject[str(self.actionID).zfill(5)] = {"actionName":"ExpSetup", "params":params}
        self.actionID += 1
        return ActionManager
    
    def runPowderSum(self): 
        params = {}
        params["experimentName"] = self.known["experimentName"]
        params["runNumber"] = self.runNumber
        params["detectorName"] = self.known["detectorName"]
        params["noe"] = 2000
        params["mode"] = "launch"

        ActionManager = actionManager.ActionManager(actionName="PowderSum", actionID=str(self.actionID).zfill(5), params=params) 
        ActionManager.start()
        self.actionObject[str(self.actionID).zfill(5)] = {"actionName":"PowderSum", "params":params}
        self.actionID += 1
        return ActionManager
    
    def runFinderCenter(self): 
        params = {}
        params["experimentName"] = self.known["experimentName"]
        params["runNumber"] = self.runNumber
        params["detectorName"] = self.known["detectorName"]
        params["mode"] = "local"

        ActionManager = actionManager.ActionManager(actionName="FindCenter", actionID=str(self.actionID).zfill(5), params=params)
        ActionManager.start()
        self.actionObject[str(self.actionID).zfill(5)] = {"actionName":"FindCenter", "params":params}
        self.actionID += 1
        return ActionManager
        
    def runPeakFinder(self):
        params = {}
        params["experimentName"] = self.known["experimentName"]
        params["runNumber"] = self.runNumber
        params["detectorName"] = self.known["detectorName"]
        params["pkTag"] = "TesT"
        params["noe"] = 2000
        params["mode"] = "launch"

        ActionManager = actionManager.ActionManager(actionName="PeakFinder", actionID=str(self.actionID).zfill(5), params=params)
        ActionManager.start()
        self.actionObject[str(self.actionID).zfill(5)] = {"actionName":"PeakFinder", "params":params}
        self.actionID += 1
        return ActionManager

    def runIndexer(self, detectorDistance=0):
        params = {}
        params["experimentName"] = self.known["experimentName"]
        params["runNumber"] = self.runNumber
        params["detectorName"] = self.known["detectorName"]
        params["pkTag"] = "TesT"
        params["pdb"] = self.known["pdb"]
        params["detectorDistance"] = detectorDistance
        params["mode"] = "launch"
        params["tag"] = "d-"+str(round(params["detectorDistance"])).zfill(5) +"-"+ str(self.actionID).zfill(5)

        ActionManager = actionManager.ActionManager(actionName="Indexer", actionID=str(self.actionID).zfill(5), params=params) 
        ActionManager.start()
        self.actionObject[str(self.actionID).zfill(5)] = {"actionName":"Indexer", "params":params}
        self.actionID += 1
        return ActionManager

    def runEvaluateStream(self):
        from back.expParams import experiparams
        params = {}
        params["experimentName"] = self.known["experimentName"]
        params["runNumber"] = self.runNumber
        params["detectorName"] = self.known["detectorName"] 
        params["pdb"] = str(self.known["pdb"] is not None)
        params["mode"] = "local"
        indexTag = self.lookup(actionName="Indexer")
        expParams = experiparams(params["experimentName"], params["runNumber"], detectorName=params["detectorName"])
        params["stream"] = "%s/%s_%.4d_%s.stream"%(expParams.cxiDir, params["experimentName"], params["runNumber"], indexTag["params"]["tag"])
        # cxic0415_0100_d-000.0-00001.stream

        print params 
        ActionManager = actionManager.ActionManager(actionName="EvaluateIndex", actionID=str(self.actionID).zfill(5), params=params) 
        ActionManager.start()
        self.actionObject[str(self.actionID).zfill(5)] = {"actionName":"EvaluateIndex", "params":params}
        self.actionID += 1
        return ActionManager

    def runFindNiggli(self):
        from back.expParams import experiparams
        params = {}
        params["experimentName"] = self.known["experimentName"]
        params["runNumber"] = self.runNumber
        params["detectorName"] = self.known["detectorName"] 
        params["pdb"] = str(self.known["pdb"] is not None)
        params["mode"] = "local"
        indexTag = self.lookup(actionName="Indexer")
        expParams = experiparams(params["experimentName"], params["runNumber"], detectorName=params["detectorName"])
        params["stream"] = "%s/%s_%.4d_%s.stream"%(expParams.cxiDir, params["experimentName"],\
                                                   params["runNumber"], indexTag["params"]["tag"])

        ActionManager = actionManager.ActionManager(actionName="FindNiggli", actionID=str(self.actionID).zfill(5), params=params) 
        ActionManager.start()
        self.actionObject[str(self.actionID).zfill(5)] = {"actionName":"FindNiggli", "params":params}
        self.actionID += 1
        return ActionManager        

    def monitor(self, ActionManager, sleepTime=60):
        currentStatus = "waiting"
        tic = time.time()
        while True:
            output = ActionManager.checkActionStatus()
            if output["status"] != currentStatus:
                currentStatus = output["status"]
                print output["status"]
            if output["status"] == "done":
                return True
            if output["status"] == "exit":
                return False
            if time.time() - tic > sleepTime:
                print "## monitor is sleeping"
                break
            time.sleep(2)
            
    def lookup(self, actionID=None, actionName=None, sort="new"):
        if actionID is not None:
            return self.actionObject[actionID]
        if len(self.actionObject) == 0:
            return None
        if actionName is None:
            maxID = max(self.actionObject)
            return self.actionObject[maxID]

        if sort == "new":
            for eachID in sorted(self.actionObject)[::-1]:
                if self.actionObject[eachID]["actionName"] == actionName:
                    return self.actionObject[eachID]
                else:
                    pass
        else:
            for eachID in sorted(self.actionObject):
                if self.actionObject[eachID]["actionName"] == actionName:
                    return self.actionObject[eachID]
                else:
                    pass
        return None
        