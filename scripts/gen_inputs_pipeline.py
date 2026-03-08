#!/usr/bin/env python3
import sys
import json
sys.path.append('../helperstuff/')
from split import split

# -----------------------------
# Read input arguments
# -----------------------------
# Expecting:
#   1. obsNames as JSON list
#   2. YEARS as JSON list
#   3. DO_SPLIT as string "True" or "False"

if len(sys.argv) != 4:
    print("Usage: python3 gen_inputs.py '<obsNames_json>' '<YEARS_json>' <DO_SPLIT>")
    sys.exit(1)

obsNames = json.loads(sys.argv[1])
YEARS = json.loads(sys.argv[2])
DO_SPLIT = sys.argv[3] == "True"

# -----------------------------
# Generate years list
# -----------------------------
years = []

if DO_SPLIT:
    for YEAR in YEARS:
        if YEAR in split and split[YEAR]:
            nSplit = split[YEAR]
            for i in range(nSplit):
                years.append(f"{YEAR}_{i+1}")
        else:
            years.append(YEAR)
else:
    years = YEARS

# -----------------------------
# Write input_args.txt
# -----------------------------
with open("input_args.txt", "w") as f:
    for obs in obsNames:
        for year in years:
            f.write(f"{obs} {year}\n")

# Optional: print for debugging
#print(f"Generated {len(obsNames) * len(years)} jobs in input_args.txt")