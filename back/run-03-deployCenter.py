import findCenter as fc 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-exp", "--exp", help="experiment name", default="", type=str)
parser.add_argument("-run", "--run", help="run number", default=-1, type=int)
parser.add_argument("-det", "--det", help="detector alias (e.g. DscCsPad)", default="DscCsPad", type=str) 
parser.add_argument("-cx", "--cx", help="center x", default=None, type=float) 
parser.add_argument("-cy", "--cy", help="center y", default=None, type=float) 
args = parser.parse_args()

if args.cx is None or args.cy is None:
    print "##### No input new center"

fc.deployCenter(experimentName=args.exp, runNumber=args.run, detectorName=args.det, newCx=args.cx, newCy=args.cy)
