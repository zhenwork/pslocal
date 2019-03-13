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
manager = multiprocessing.Manager()

"""
Standard params:

tag: unique tag
timeStamp:
status: waiting/running/complete -> running/done/exit
"""

class ActionManager(multiprocessing.Process):

    def __init__(self, actionName=None, actionID=None, params={}):
        self.params = params.copy()
        self.status = 'waiting' 
        self.actionID = actionID
        self.actionName = actionName 
        self.actionParams = manager.dict()

        self.timeStamp = {utils.getTime() : self.status}
        if self.actionID is None:
            self.actionID = utils.getTime() 

        self.actionParams = utils.mergeDict(old=self.actionParams, new=self.params)
        if "jobName" not in self.actionParams:
            self.actionParams["jobName"] = "%s-%s"%(self.actionName, self.actionID)
        self.actionParams["jobID"] = None
        self.actionParams["status"] = "waiting"
        


    def start(self):
        ## Check whether the action is feasible 
        if not self.checkActionFeasibility():
            self.updateStatus("exit")
            return False

        ## process the action
        self.updateStatus("running")
        print "starting jobs"
        self.launchAction()
        return 


    def checkActionStatus(self):
        if self.status == "exit" or self.status=="done":
            return {"status":self.status, "completeness":0, "log":self.actionParams["output"]}
        elif self.params["mode"].lower() == "local":
            return self.checkStatusLocal()
        elif self.params["mode"].lower() == "launch":
            if self.actionParams["status"] == "complete":
                return self.checkStatusServer(jobID=self.actionParams["jobID"], jobName=self.actionParams["jobName"])
            else:
                return {"status":"running", "completeness":0, "log":{"out":None, "err":None}}
        else:
            return None


    def checkActionFeasibility(self):
        if self.actionName is None:
            return False
        if "mode" not in self.params:
            return False
        try:
            tmp = getattr(actionCluster, self.actionName)
            tmp = None
            return True
        except:
            return False


    def to_dict(self):
        return self.__dict__


    def updateStatus(self, current_status):
        if self.status != current_status:
            self.status = current_status
            self.timeStamp[utils.getTime()] = self.status 
        return


    def launchAction(self):
        try:
            actionObject = getattr(actionCluster, self.actionName)(self.actionParams)

            p = multiprocessing.Process(target=actionObject.start, args=())
            p.start()
            p = None
            print "submitted"
            self.updateStatus("running")
            return True
        except Exception as err: 
            self.updateStatus("exit")
            print err
            return False


    def checkStatusLocal(self): 

        status = self.actionParams["status"]
        if status == 'running' or status == "waiting":
            self.updateStatus("running")
            return {"status":"running", "completeness":0, "log":{"out":None, "err":None}}

        output = self.actionParams["output"]
        if not "out" in output or not "err" in output:
            return {"status":status, "completeness":0, "log":{"out":None, "err":None}}

        out = output["out"]
        err = output["err"]
        if self.actionParams["status"] != "complete":
            self.updateStatus("exit")
        elif "exit" in err.lower() or "exit" in out.lower():
            self.updateStatus("exit")
        elif "terminate" in err.lower() or "terminate" in out.lower():
            self.updateStatus("exit")
        else:
            self.updateStatus("done") 

        return {"status":status, "completeness":0, "log":self.actionParams["output"]}


    def checkStatusServer(self, jobID=None, jobName=None):
        ## no job id, no job name
        if jobID is None and jobName is None:
            print "testing"
            return None

        if self.actionParams["status"] == "exit":
            self.updateStatus("exit")
            return {"status":self.status, "completeness":0, "log":{"out":self.actionParams["output"]["out"], "err":self.actionParams["output"]["err"]}}
        elif self.actionParams["status"] == "running":
            self.updateStatus("running")
            return {"status":self.status, "completeness":0, "log":{"out":None, "err":None}}
        else:
            pass 

        ## with job id
        if jobID is not None:
            #print "using jobID", jobID

            cmd = "bjobs -d | grep " + str(jobID)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            
            # print out,err

            if "done" in out.lower():
                self.updateStatus("done")
                return {"status":self.status, "completeness":100, "log":{"out":out, "err":err}}
            elif len(out) == 0:
                self.updateStatus("running")
                return {"status":self.status, "completeness":0, "log":{"out":out, "err":err}}
            else:
                self.updateStatus("exit")
                return {"status":self.status, "completeness":100, "log":{"out":out, "err":err}}
        
        # with jobName
        if jobName is not None: 
            ## check in completed jobs
            #print "using jobname", jobName
            cmd = 'bjobs -J ' + '*\"' + jobName + '\"*' + ' -d | grep ps'
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            process = None

            #print out,err

            if "exit" in out:
                self.updateStatus("exit")
                return {"status":self.status, "completeness":0, "log":{"out":out, "err":err}}

            ## check in incomplete jobs
            cmd = 'bjobs -J ' + '*\"' + jobName + '\"*' + ' | grep ps'
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            process = None

            if len(out) == 0:
                self.updateStatus("done")
                return {"status":self.status, "completeness":100, "log":{"out":out, "err":err}}
            else:
                self.updateStatus("running")
                return {"status":self.status, "completeness":0, "log":{"out":out, "err":err}}            
