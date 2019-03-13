import indexerHelper as indexerHelper
import subprocess 
import shlex
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-exp", "--exp", help="experiment name", default="", type=str)
parser.add_argument("-run", "--run", help="run number", default=-1, type=int)
parser.add_argument("-det", "--det", help="detector alias (e.g. DscCsPad)", default="DscCsPad", type=str) 
parser.add_argument("-pkTag", "--pkTag", help="tag of cxi file", default="", type=str) 
parser.add_argument("-noe", "--noe", help="number of images", default=-1, type=int)
parser.add_argument("-distance", "--distance", help="distance + or - in mm", default=None, type=str)
parser.add_argument("-pdb", "--pdb", help="pdb", default=None, type=str)
parser.add_argument("-tag", "--tag", help="index tag", default="", type=str)
args = parser.parse_args()


if args.distance is not None:
    detectorDistanceList = args.distance.split(',')
    for detectorDistanceString in detectorDistanceList:
        geoM = indexerHelper.GeoFileManager(experimentName=args.exp,runNumber=args.run,detectorName=args.det)
        detectorDistance = geoM.detectorDistance + float(detectorDistanceString)*1.0e-3
        geoM.changeDistance(detectorDistance)
        indH = indexerHelper.IndexHelper(args.exp, args.run, args.det)
        indH.pkTag = args.pkTag
        indH.indexnoe = args.noe 
        indH.pdbfile = args.pdb 
        indH.tag = args.tag
        command = indH.indexCommand(geoM)
        print " #####\n", command, "\n ######"
        geoM = None
        indH = None

        process = subprocess.Popen(shlex.split(command))
        """
        Submit without waiting
        """
else:
    geoM = indexerHelper.GeoFileManager(experimentName=args.exp,runNumber=args.run,detectorName=args.det)
    geoM.changeDistance(geoM.detectorDistance)
    indH = indexerHelper.IndexHelper(args.exp, args.run, args.det)
    indH.pkTag = args.pkTag 
    indH.indexnoe = args.noe 
    indH.pdbfile = args.pdb 
    indH.tag = args.tag
    command = indH.indexCommand(geoM)
    print " #####\n", command, "\n ######"
    geoM = None
    indH = None

    process = subprocess.Popen(shlex.split(command))
    #process.communicate()
    #jobname = params.experimentName + "_" + str(params.runNumber) + "*" + params.tag
