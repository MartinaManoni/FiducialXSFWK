#!/bin/bash

cd /afs/cern.ch/user/m/mmanoni/FiducialXS/CMSSW_14_1_0_pre4/src
source setup.sh
cmsenv
cd FiducialXSFWK

obsName="${1//_/' vs '}"
obsBins="$2"
year="$3"

python3 plotShapes.py --obsName "$obsName" --obsBins "$obsBins"--year "$year" --unblind