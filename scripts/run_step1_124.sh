#!/bin/bash

cd /afs/cern.ch/user/m/mmanoni/FiducialXS/CMSSW_14_1_0_pre4/src
source setup.sh
cmsenv
cd FiducialXSFWK/coefficients

obsName="${1//_/' vs '}"
year="$2"

python3 RunCoefficients.py --obsName "$obsName" --year "$year" --split --interpolation --hypothesis "24"

