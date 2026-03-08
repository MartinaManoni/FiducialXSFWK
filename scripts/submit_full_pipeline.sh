#!/bin/bash

mkdir -p logs

############################################
# GLOBAL YEARS
############################################
YEARS_ALL='["2022","2022EE","2023preBPix","2023postBPix","2024"]'
YEARS_RUN3='["Run3"]'
############################################
# OBSERVABLES
############################################
#OBS_ALL='["mass4l","pT4l", "rapidity4l", "massZ1", "massZ2","phi", "phi1", "costhetaZ1", "costhetaZ2", "costhetastar"]'
OBS_ALL='["pTj2", "mjj", "absdetajj", "dphijj", "pTHjj","Nj","pTHj", "mHj"]'
#"massZ1_massZ2", "rapidity4l_pT4l", "pTj1_pTj2", "Nj_pT4l", "pT4l_pTHj", "absdetajj_mjj"
#"TCjmax", "TBjmax"
#"TCjmax_pT4l"
#"pTj1"
############################################
# FUNCTION TO RUN A STEP
############################################
run_step () {

STEP_NAME=$1
OBS=$2
YEARS=$3
DO_SPLIT=$4

echo "======================================"
echo " Running $STEP_NAME"
echo "======================================"

python3 gen_inputs_pipeline.py "$OBS" "$YEARS" "$DO_SPLIT"

SUBMIT_OUTPUT=$(condor_submit sub_${STEP_NAME}.sub)

echo "$SUBMIT_OUTPUT"

CLUSTER_ID=$(echo "$SUBMIT_OUTPUT" | grep -oE 'cluster [0-9]+' | awk '{print $2}')

echo "Cluster ID: $CLUSTER_ID"
echo "Waiting for jobs to finish..."

while condor_q ${CLUSTER_ID} | grep ${CLUSTER_ID} > /dev/null; do
    sleep 60
done

echo "$STEP_NAME finished."
}

###########################################################
# STEP 1 (coefficients, split)
###########################################################

#run_step step1 "$OBS_ALL" "$YEARS_ALL" True
#run_step step1_124 "$OBS_ALL" "$YEARS_ALL" True
#run_step step1_126 "$OBS_ALL" "$YEARS_ALL" True

###########################################################
# STEP 2 (no split)
###########################################################

#run_step step2 "$OBS_ALL" "$YEARS_ALL" False

###########################################################
# STEP JES (only jet observables, no split)
###########################################################
# Automatically filter observables containing "j" or "J"

#OBS_JES=$(python3 - <<EOF
#import json
#obs = json.loads('$OBS_ALL')
#jet_obs = [o for o in obs if 'j' in o.lower()]
#print(json.dumps(jet_obs))
#EOF
#)
#
#if [ "$OBS_JES" != "[]" ]; then
#    run_step JES  "$OBS_JES" "$YEARS_ALL" False
#else
#    echo "No jet observables found → skipping JES step"
#fi

###########################################################
# STEP 3 (Run3 combination)
###########################################################

#run_step step3 "$OBS_ALL" "$YEARS_RUN3" False

###########################################################
# STEP IMPACTS
###########################################################

run_step impacts "$OBS_ALL" "$YEARS_RUN3" False

###########################################################
# STEP 4 - Acceptance uncertainties (split)
###########################################################

#run_step step4 "$OBS_ALL" "$YEARS_ALL" True

###########################################################
# STEP 5 - Merge acceptance uncertainties
###########################################################

#run_step step5 "$OBS_ALL" "$YEARS_ALL" False

###########################################################
# STEP 6 - Final plots
###########################################################

#run_step step6 "$OBS_ALL" "$YEARS_RUN3" False

echo "======================================"
echo " FULL PIPELINE SUBMITTED SUCCESSFULLY"
echo "======================================"
