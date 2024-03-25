# HOTVRProducer
From MINI to NANO - HOTVR production.
The core of the MiniToNano production is the .cc plugin in `PhysicsTools/NanoAOD/plugins/HOTVRProducer.cc` (developed by UHH -> https://github.com/UHH2/UHH2/blob/RunII_106X_v2/core/plugins/HOTVRProducer.cc)

## CMSSW Versions
Suggested CMSSW version:
* Run 2: `CMSSW_10_6_28`
* Run 3: `CMSSW_13_0_3` (*N.B.:* HOTVR production for Run 3 is still under development!)

## Running standalone (or testing)
To run the MiniToNano HOTVR producer, the correct environment setup is needed. To clone and compile this repository in the CMSSW area:
```
cd CMSSW_*_*_*/src
cmsenv
git clone git@github.com:ttXcubed/HOTVRProducer.git
scram b -j 4
```
An example is given to test the producer for 20 events of 2018 ttbar (dilepton) MC sample:
```
cmsRun mini_to_nano_producer/MiniToNano_producer_2018.py
```
This will create a ROOT output in which HOTVR variables are saved as TBranch. 


## Running CRAB 
The crab submission files are in `crab_mini_to_nano`. The submission files fetch the input files given in `crab_mini_to_nano/input_files.yaml`.
To run the submission:

```
python crab_mini_to_nano/crab_submission.py --year YEAR
```
where YEAR has to be specified. 
For signal samples, use crab_submission_sgn.py. 

N.B.: to test the submission is helpful to specify the option `configTmpl.Data.totalUnits = 1` in the configuration file.
