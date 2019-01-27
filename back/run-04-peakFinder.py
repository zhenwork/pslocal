import peakfinderHelper as pfHelper
import subprocess 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-exp", "--exp", help="experiment name", default="", type=str)
parser.add_argument("-run", "--run", help="run number", default=-1, type=int)
parser.add_argument("-det", "--det", help="detector alias (e.g. DscCsPad)", default="DscCsPad", type=str) 
parser.add_argument("-pkTag", "--pkTag", help="tag of cxi file", default="", type=str) 
parser.add_argument("-noe", "--noe", help="number of images", default=-1, type=int)
args = parser.parse_args()


pf = pfHelper.peakFinderHelper(args.exp, args.run, args.det)
pf.setDefaultParams()
pf.setAdaptiveMode()
pf.pkTag = args.pkTag
pf.noe = args.noe

command = pf.getCommand()
print " #####\n", command, "\n ######"

process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out, err = process.communicate()
