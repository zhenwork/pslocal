from expSetup import setupNewRun
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-exp", "--exp", help="experiment name", default="", type=str)
parser.add_argument("-run", "--run", help="run number", default=-1, type=int)
parser.add_argument("-det", "--det", help="detector alias (e.g. DscCsPad)", default="DscCsPad", type=str) 
parser.add_argument("-copyRun", "--copyRun", help="copy setup from runNumber", default=None, type=int) 
args = parser.parse_args()

setupNewRun(experimentName = args.exp, runNumber = args.run, detectorName=args.det, copyRun=args.copyRun)
