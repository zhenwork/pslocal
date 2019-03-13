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
        
