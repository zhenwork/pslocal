

class ExpManager:
    def __init__(self, mode="one", experimentName=None, runList=[]):
        self.mode = mode
        self.experimentName = experimentName
        self.runList = runList

    def start(self):
        if self.mode.lower() == "one":
            self.ModeOne()
        elif self.mode.lower() == "two":
            self.


    def ModeOne(self):
        ## Known distance and known unit cell

        ## setup

        ## powderSum

        ## Find center

        ## peakFinder

        ## indexer

    def ModeTwo(self):
        ## Unknown distance and known unit cell 


    def ModeThree(self):
        ## Known distance and unknown unit cell

