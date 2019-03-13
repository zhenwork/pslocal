import os
import findCenter as fc 
import numpy as np 
from expParams import experiparams
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-img", "--img", help="image used to find center", default=None, type=str) 
parser.add_argument("-mask", "--mask", help="mask", default=None, type=str) 
parser.add_argument("-mode", "--mode", help="modes (ps, sb)", default="ps", type=str) 
parser.add_argument("-exp", "--exp", help="experiment name", default=None, type=str)
parser.add_argument("-run", "--run", help="run number", default=None, type=int)
parser.add_argument("-det", "--det", help="detector alias (e.g. DscCsPad)", default=None, type=str)
args = parser.parse_args()

if args.img is None and args.mask is None:
    params = experiparams(experimentName=args.exp, runNumber=args.run)
    args.img = params.cxiDir+"/"+args.exp+"_"+str(args.run).zfill(4)+"_"+str(args.det)+"_mean_assem.npy"
    args.mask = params.cxiDir+"/psanaMask.npy"
    
image = np.load(args.img)

if args.mask is not None and os.path.isfile(args.mask):
    mask = np.load(args.mask)
else: 
    mask = np.ones(image.shape)


if args.mode == "ps":
    fc.findCenterPowderSum(image, _mask=mask)
elif args.mode == "sb":
    """
    not implemented
    """
    print "@@@@@ Not implemented"
    #fc.findCenterSilverBehenate(silverBehenateImage, pixelSize, waveLength, _mask=mask)
else:
    print "@@@@@ No such method"