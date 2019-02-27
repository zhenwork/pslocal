"""
1. process actions
"""
import sys
import time
import shlex
import datetime
import utils
import fileManager
import subprocess 


def actionObject(actionName):
    return getattr(sys.modules[__name__], actionName)

"""
Standard params:

tag: unique tag
mode: local/launch
jobID: 
jobName: 
status: waiting/running/complete -> running/done/exit
input: 
output: 
"""

class ExpSetup:
    """
    default mode should be "local"
    """
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        self.params["status"] = "running"
        output = {}
        try:
            assert self.params["mode"].lower() == "local"

            cmd = "python ../back/run-01-expSetup.py "+ \
                utils.argsToCommand(self.params, item=["experimentName", "runNumber", "detectorName", "copyRun"], \
                                    _iter=["exp", "run", "det", "copyRun"])

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            output["out"] = out
            output["err"] = err
            output["cmd"] = cmd
            self.params["output"] = output.copy()
            self.params["status"] = "complete"
            process = None
        except Exception as err:
            self.params["output"] = {"out":None, "err":str(err)}
            self.params["status"] = "exit"
        return


class ExampleLocal:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        self.params["status"] = "running"
        output = {}
        try:
            assert self.params["mode"].lower() == "local"

            experimentName = self.params["experimentName"]
            runNumber = self.params["runNumber"]
            detectorName = self.params["detectorName"]
            
            cmd = "python ./test-pipeline.py "

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            output["out"] = out
            output["err"] = err
            self.params["output"] = output.copy()
            self.params["status"] = "complete"
            process = None
        except Exception as err:
            self.params["output"] = {"out":None, "err":str(err)}
            self.params["status"] = "exit"
        return


class ExampleLaunch:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        self.params["status"] = "running"
        output = {}
        try:
            assert self.params["mode"].lower() == "launch"

            experimentName = self.params["experimentName"]
            runNumber = self.params["runNumber"]
            detectorName = self.params["detectorName"]
            
            cmd = 'bsub -q psdebugq -x -n 1 -R "span[ptile=1]" -J ' + self.params["jobName"] + ' -o %J.out python ./test-pipeline.py'

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            output["out"] = out 
            output["err"] = err
            output["cmd"] = cmd

            time.sleep(3)

            self.params["jobID"] = utils.getJobID(out)
            self.params["output"] = output.copy()
            self.params["status"] = "complete"
            process = None
        except Exception as err:
            self.params["output"] = {"out":None, "err":str(err)}
            self.params["status"] = "exit"
        return


class PowderSum:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        return 



class DeployCenter:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        return 


class FindCenter:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        return 

class PeakFinder:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        return 


class Indexer:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        return 


class FinderDistance:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        return 


