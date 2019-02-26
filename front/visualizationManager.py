"""
1. process actions
"""
import time
import shlex
import datetime
from fileManager import *
import subprocess as sp
fm = fileManager()


class visualizationManager(object):

    def __init__(self, experimentName, directory=None):
        self.status = 'running'
        self.experimentName = experimentName
        self.timeStamp = {utils.getTime() : self.status}
        self.setDefault(experimentName, directory)
        self.thisfile = "%s/visualizationManager.pickle" % self.logDir
        

    def start(self):
        return
        

    def to_dict(self):
        return self.__dict__


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

