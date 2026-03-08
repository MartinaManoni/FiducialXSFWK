#!/bin/bash

# Base directory
BASE_DIR="/eos/user/m/mmanoni/www/HIG25015_PLOTS/UNBLINDED/TRY/IMPACTS"

# Loop over all Run3 directories
for dir in "$BASE_DIR"/*/Run3/; do
    echo "Processing directory: $dir"

    # Loop over all PDF files matching pattern
    for pdf in "$dir"/impacts_Run3_*_data.pdf; do
        # Skip if no match
        [ -e "$pdf" ] || continue

        # Get filename without extension
        filename=$(basename "$pdf" .pdf)

        # Output PNG path
        png="$dir/${filename}.png"

        echo "Converting $pdf -> $png"

        # Convert first page of PDF to PNG with higher resolution (600 dpi)
        pdftoppm -png -f 1 -singlefile -r 600 "$pdf" "$dir/$filename"
    done
done