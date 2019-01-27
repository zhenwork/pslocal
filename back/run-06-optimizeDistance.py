import os
import numpy as np
import subprocess
import evaluateIndexing as ei 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-stream", "--stream", help="stream file", default=None, type=str)
args = parser.parse_args()

process = subprocess.Popen("find "+args.stream, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out, err = process.communicate()
out = out.split('\n')

for streamfile in out:
	if not os.path.isfile(streamfile):
		continue
	score = ei.evaluateIndexing(streamfile)
	print "streamfile: ", streamfile
	print "score: ", np.sum(score[:3]), np.sum(score[3:]), np.sum(score), score