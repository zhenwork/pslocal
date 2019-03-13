"""
1. process actions
"""
import os
import sys
import time
import shlex
import datetime
import utils
import fileManager
import subprocess 
import multiprocessing
fm = fileManager.OtherFileManager()
sys.path.append("/reg/neh/home/zhensu/Develop/pslocal")
thisPath = "/reg/neh/home5/zhensu/Develop/pslocal"


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
            self.params["output"] = {"out":"", "err":str(err)}
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

            print "cmd", cmd

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
            self.params["output"] = {"out":"", "err":str(err)}
            self.params["status"] = "exit"
        return


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
            
            cmd = "python " + thisPath + "/back/run-01-expSetup.py "+ \
                utils.argsToCommand(self.params, item=["experimentName", "runNumber", "detectorName", "copyRun"], \
                                    _iter=["exp", "run", "det", "copyRun"])
            
            sys.stdout.write(cmd)
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            output["out"] = out
            output["err"] = err
            output["cmd"] = cmd
            self.params["output"] = output.copy()
            self.params["status"] = "complete"
            process = None
        except Exception as err:
            self.params["output"] = {"out":"", "err":str(err)}
            self.params["status"] = "exit"
        return
    
    
class PowderSum:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        self.params["status"] = "running"
        output = {}
        try:
            assert self.params["mode"].lower() == "launch"
            
            cmd = 'bsub -q psdebugq -x -n 12 -R "span[ptile=12]" -J ' + self.params["jobName"] + ' -o %J.out ' +\
                ' mpirun python ' + thisPath + "/back/run-02-powderSum.py " + \
                utils.argsToCommand(self.params, item=["experimentName", "runNumber", "detectorName", "noe"], \
                                    _iter=["exp", "run", "det", "noe"])

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            output["out"] = out 
            output["err"] = err
            output["cmd"] = cmd

            time.sleep(4)

            self.params["jobID"] = utils.getJobID(out)
            self.params["output"] = output.copy()
            self.params["status"] = "complete"
            process = None
        except Exception as err:
            self.params["output"] = {"out":"", "err":str(err)}
            self.params["status"] = "exit"
        return



class DeployCenter:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        return 


class FindCenter:
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
            
            cmd = "python " + thisPath + "/back/run-03-findCenter.py "+ \
                utils.argsToCommand(self.params, item=["experimentName", "runNumber", "detectorName"], \
                                    _iter=["exp", "run", "det"])

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            output["out"] = out
            output["err"] = err
            output["cmd"] = cmd
            self.params["output"] = output.copy()
            self.params["status"] = "complete"
            process = None
        except Exception as err:
            self.params["output"] = {"out":"", "err":str(err)}
            self.params["status"] = "exit"
        return

    
class PeakFinder:
    """
    default mode should be "local"
    """
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        self.params["status"] = "running"
        output = {}
        try:
            assert self.params["mode"].lower() == "launch"
            import back.peakfinderHelper as pfHelper       
            pf = pfHelper.peakFinderHelper(self.params["experimentName"], self.params["runNumber"], self.params["detectorName"])
            pf.setDefaultParams()
            pf.setAdaptiveMode()
            pf.pkTag = self.params["pkTag"]
            pf.noe = self.params["noe"]
            pf.jobName = self.params["jobName"]
            
            cmd = pf.getCommand() 
            sys.stdout.write(cmd)
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            time.sleep(10)
            output["out"] = out
            output["err"] = err
            output["cmd"] = cmd
            self.params["jobID"] = utils.getJobID(out)
            self.params["output"] = output.copy()
            self.params["status"] = "complete"
            process = None
        except Exception as err:
            sys.stdout.write(str(err))
            self.params["output"] = {"out":"", "err":str(err)}
            self.params["status"] = "exit"
        return


    
class Indexer:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        self.params["status"] = "running"
        output = {}
        try:
            assert self.params["mode"].lower() == "launch" 
            
            cmd = "python " + thisPath + "/back/run-05-indexer.py "+ \
        utils.argsToCommand(self.params, item=["experimentName", "runNumber", "detectorName", "pdb", "pkTag", "detectorDistance", "tag"],\
                                    _iter=["exp", "run", "det", "pdb", "pkTag", "distance", "tag"])
            
            self.params["jobName"] = "%s_%d*%s"%(self.params["experimentName"], self.params["runNumber"], self.params["tag"])
            sys.stdout.write(cmd)
            sys.stdout.write(str(self.params["jobName"]))
            
            process = subprocess.Popen(shlex.split(cmd))
            out, err = process.communicate()
            
            time.sleep(20)
            
            output["out"] = out
            output["err"] = err
            output["cmd"] = cmd
            self.params["output"] = output.copy()
            self.params["status"] = "complete"
            process = None
            
        except Exception as err:
            sys.stdout.write(str(err))
            self.params["output"] = {"out":"", "err":str(err)}
            self.params["status"] = "exit"
        return


class EvaluateIndex:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        self.params["status"] = "running"
        output = {}
        try:
            import back.evaluateIndexing as ei
            sys.stdout.write("## evaluating index")
            process = subprocess.Popen("find "+self.params["stream"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            out = out.split('\n')
            
            sys.stdout.write(str(out))

            for streamfile in out:
                if not os.path.isfile(streamfile):
                    continue
                sys.stdout.write(streamfile)
                print "##### with pdb? ", bool(self.params["pdb"].lower() in ["true", "yes", '1'])
                score = ei.evaluateIndexing(streamfile, withpdb=bool(self.params["pdb"].lower() in ["true", "yes", '1']))
                print "##### score: ", score, "\n\n" #, np.sum(score[3:]), np.sum(score), score,'\n\n'
            
            output["out"] = str(out)
            output["err"] = str(err) 
            output["score"] = score
            self.params["output"] = output.copy()
            self.params["status"] = "complete"
            process = None
            
        except Exception as err:
            sys.stdout.write(str(err))
            self.params["output"] = {"out":"", "err":str(err)}
            self.params["status"] = "exit"
        return


class FindNiggli:
    def __init__(self, actionParams):
        self.params = actionParams
    def start(self):
        self.params["status"] = "running"
        output = {}
        try:
            
            cmd = "source /reg/g/cctbx/conda_build/build/setpaths.sh && python " + thisPath + "/back/run-07-findNiggli.py "+ \
                        utils.argsToCommand(self.params, item=["stream", "pdb"], _iter=["stream", "pdb"])
            
            sys.stdout.write(cmd)
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = process.communicate()
            sys.stdout.write(out)
            
            if len(out) == 0:
                cell = None
            elif len(out.split("niggli cell:")) == 1:
                cell = None
            else:
                cell = out.split("niggli cell:")[1]
            
            output["out"] = str(out)
            output["err"] = str(err)
            output["cell"] = cell
            self.params["output"] = output.copy()
            self.params["status"] = "complete"
            process = None
            
        except Exception as err:
            sys.stdout.write(str(err))
            self.params["output"] = {"out":"", "err":str(err)}
            self.params["status"] = "exit"
        return