"""
1. process actions
"""
import time
import shlex
import datetime
import utils as utils
from fileManager import *
import subprocess
import actionCluster
import multiprocessing
fm = FileManager()

"""
Standard params:

tag: unique tag
timeStamp:
status: waiting/running/finish/
"""
class ActionManager:

    def __init__(self, params={}):
        self.status = 'waiting'
        self.experimentName = experimentName
        self.timeStamp = {utils.getTime() : self.status}
        self.setDefault(experimentName, directory)
        self.thisfile = "%s/actionManager.pickle" % self.logDir
        self.actionList = {}


    def start(self):
        current_status = 'running'
        while True:
            todoActions = self.getTodoActions()
            if len(todoActions) > 0:
                self.launchAction(todoActions)
                print "##### launched action: %s" % todoActions

            self.updateGroup()
            self.iprint("##### runList: ", self.groups)
            self.iprint("##### actionList: ", self.loadActionFile())
            self.updateStatus(current_status)
            self.flush()
            time.sleep(3)


    def to_dict(self):
        return self.__dict__


    def flush(self):
        while True:
            if fm.save_pickle(self, self.thisfile): break
            else: pass


    def reload(self):
        while True:
            params = fm.load_pickle(self.thisfile)
            if params: 
                self = params
                break
            else: pass


    def resume(self):
        self.reload()
        self.start()
        return


    def updateStatus(self, current_status):
        if self.status != current_status:
            self.status = current_status
            self.timeStamp[utils.getTime()] = self.status 
        return


    def setDefault(experimentName, directory):
        if directory is None:
            self.expDir = "/reg/d/psdm/%s/%s" % (experimentName[:3], experimentName)
            self.autoDir = "%s/scratch/%s/automation" % (self.expDir, utils.getUsername())
            self.logDir = "%s/logDir" % self.autoDir
            self.dataDir = "%s/dataDir" % self.autoDir
        else:
            self.expDir = directory
            self.autoDir = "%s/%s/automation" % (self.expDir, utils.getUsername())
            self.logDir = "%s/logDir" % self.autoDir
            self.dataDir = "%s/dataDir" % self.autoDir

        if not os.path.isdir(self.autoDir):
            os.makedirs(self.autoDir)
        if not os.path.isdir(self.logDir):
            os.makedirs(self.logDir)
        if not os.path.isdir(self.dataDir):
            os.makedirs(self.dataDir)

        self.expRunFile = "%s/exp-run.json" % self.dataDir
        self.expActionFile = "%s/exp-action.json" % self.dataDir
        return


    def silent(self, silent):
        if not isinstance(silent, bool):
            return False
        self.silent = bool(silent)
        self.flush()


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


    def updateGroup(self):
        groups = {}
        for run in self.expruns:
            groupName = self.expruns[run]['group']
            if groupName not in groups:
                groups[groupName] = [run]
            else:
                groups[groupName].append(run)
        self.groups = groups.copy()



    def launchAction(self, todoActions):
        if len(todoActions) == 0:
            return True
        else:
            try:
                actionID = todoActions.keys()[0]
                actionName = todoActions[actionID]['actionName']
                assert actionID not in self.actionList
                
                self.actionList[actionID] = todoActions[actionID].copy()
                self.actionList[actionID]['object'] = ac.actionObject(actionName)(actionID)
                p = mp.Process(target=self.actionList[actionID]['object'].start, args=())
                p.start()
                p = None
                return True 
            except Exception as err: 
                print(err)
                return False


    def getTodoActions(self):
        newActions = self.getActions()
        todoActions = {}
        
        lastProcessedActionID = '00000' if len(self.actionManagers) == 0 else max(self.actionManagers)
        
        if len(newActions) == 0:
            return {}
            
        if lastProcessedActionID == max(newActions):
            return {}
            
        for actionID in sorted(newActions):
            if actionID <= lastProcessedActionID:
                continue
            todoActions[actionID] = newActions[actionID].copy()
            break
            
        return todoActions


    def getActions(self):
        newRuns = self.loadActionFile()
        expruns = newRuns.copy()
        newActions = {}
        for run in newRuns:
            runNumber = int(run)
            actions = newRuns[run]['action']   ##actions = {"00001":'setup', "00002":'dump'}
            for actionID in sorted(actions):
                actionName = actions[actionID]
                if actionID not in newActions:
                    newActions[actionID] = {}
                    newActions[actionID]['name'] = actionName
                    newActions[actionID]['runList'] = [runNumber]
                else:
                    newActions[actionID]['runList'].append(runNumber)
        return newActions


    def loadActionFile(self):
        while True:
            actions = fm.load_json(self.expActionFile)
            if actions: return actions
            else: pass


    def checkStatusLocal(self):
        if "exit" in err.lower() or "exit" in out.lower():
            self.params["status"] = "exit"
        elif "terminate" in err.lower() or "terminate" in out.lower()::
            self.params["status"] = "terminate"
        else:
            self.params["status"] = "done"


    def checkStatusServer(self, jobID=None, jobName=None):
        if len(self.jobID) == 0:
            self.status = 'complete'
            self.completeness = '100%'
            self.flush()
            self.save()
            return True, 1.0
        else:
            complete = 0
            total = len(self.jobID)
            for each_jobID in self.jobID:
                if self.checkJobStatus(each_jobID):
                    complete += 1
            completeness = complete * 1.0 / total
            self.completeness = "%4.2f\%" % 100.0*completeness
            self.flush()
            self.save()
            return False, completeness
