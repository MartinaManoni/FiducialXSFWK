#!/bin/bash

# Base paths
INPUT_BASE="/eos/cms/store/group/phys_higgs/cmshzz4l/cjlst/HIG-25-015/RunIII_byZ1Z2/031125/2024_MC/DYJetsTo2E"
OUTPUT_BASE="/eos/user/m/mmanoni/ScaleSmearingSyst_skimmed_rootfiles/2024DY"

# Loop over DYJetsTo2Tau_1 to DYJetsTo2Tau_14
for i in {2..13}; do
    INPUT_DIR="$INPUT_BASE/DYJetsTo2E_$i/DYJetsTo2E"
    INPUT_FILE="$INPUT_DIR/ZZ4lAnalysis.root"

    OUTPUT_DIR="$OUTPUT_BASE/DYJetsTo2E_$i"
    OUTPUT_FILE="$OUTPUT_DIR/ZZ4lAnalysis_SKIMMED.root"

    # Create output directory if it doesn't exist
    mkdir -p "$OUTPUT_DIR"

    # Run the skimmer
    echo "Processing DYJetsTo2E_$i..."
    python3 Run3Skimmer_SS.py --input "$INPUT_FILE" --output "$OUTPUT_FILE" --mc
done

echo "All jobs finished!"