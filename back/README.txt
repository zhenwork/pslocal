==============================================================================
## set up a new run
python run-01-expSetup.py --exp cxic0415 --run 99 --det DscCsPad 



==============================================================================
## run powder sum
bsub -q psanaq -n 12 -o ./.%J.out -J powerSum mpirun python run-02-powderSum.py --exp cxic0415 --run 100 --det "DscCsPad" --noe 1000



==============================================================================
## finder center with powder sum
python run-03-findCenter.py --img /path/to/r0100/cxic0415_0100_DscCsPad_mean_assem.npy --mask /path/to/r0100/psanaMask.npy



==============================================================================
## deploy center or not
python run-03-deployCenter.py --exp cxic0415 --run 100 --det DscCsPad --cx 873 --cy 881



==============================================================================
## run peak finder
python run-04-peakFinder.py --exp cxic0415 --run 100 --det DscCsPad --pkTag test2000-newparams --noe 2000




==============================================================================
## run indexer
@@ distance can be set to "-8,-6,-4,-2,0,2,4,6,8" in milimeter referring to raw distance

python run-05-indexer.py --exp cxic0415 --run 100 --det DscCsPad --pdb /path/to/strep_more.cell  --pkTag test2000-newparams --distance " -4,-2,0,2,4 "




==============================================================================
## optimize distance with indexing result
@@ use cxic0415_*.stream to evaluate all stream files

source /reg/g/cctbx/conda_build/build/setpaths.sh 
python run-06-optimizeDistance.py --stream " /path/to/r0100/cxic0415_0100_index-distance-*.stream-psocake " 





==============================================================================
## find niggli unit cell from stream file
source /reg/g/cctbx/conda_build/build/setpaths.sh
python run-07-findNiggli.py --stream " /path/to/r0100/cxic0415_0100_index-distance-*.stream-psocake "

