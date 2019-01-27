import findCenter as fc 
import numpy as np 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-img", "--img", help="image used to find center", default="", type=str) 
parser.add_argument("-mask", "--mask", help="mask", default=None, type=str) 
parser.add_argument("-mode", "--mode", help="modes (ps, sb)", default="ps", type=str) 
args = parser.parse_args()

image = np.load(args.img)

if args.mask is not None and os.path.isfile(args.mask):
	mask = np.load(args.mask)
else: mask = 1.


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