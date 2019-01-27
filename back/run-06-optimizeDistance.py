import evaluateIndexing as ei 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-stream", "--stream", help="stream file", default=None, type=str)
args = parser.parse_args()

score = ei.evaluateIndexing(args.stream)
print score, np.sum(score[:3])