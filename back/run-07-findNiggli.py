import os
import numpy as np
import subprocess
import evaluateIndexing as ei 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-stream", "--stream", help="stream file", default=None, type=str)
parser.add_argument("-pdb", "--pdb", help="indexed with pdb or not", default="True", type=str)
args = parser.parse_args()

process = subprocess.Popen("find "+args.stream, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out, err = process.communicate()
out = out.split('\n')

args.pdb = args.pdb in ["true", "yes", '1']

for streamfile in out:
    if not os.path.isfile(streamfile):
        continue
    indexHistogram = ei.getIndexHistogram(streamfile)
    lattice = indexHistogram[:,9:15].copy() 

    print "##### streamfile: ", streamfile
    print "##### with pdb? ", args.pdb
    print "##### numIndex: ", len(lattice) 
    if args.pdb:
        lattice = ei.convert2niggli(lattice)
        [lattice, Volume] = volumeFilter(lattice)
        print "##### numIndex after filter: ", len(lattice)

    nuc = np.nanmean(lattice,axis=0).reshape((1,6))
    nuc = convert2niggli(nuc).ravel()
    print "##### niggli cell: ", nuc

