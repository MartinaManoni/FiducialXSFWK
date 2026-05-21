#!/usr/bin/env bash

LOG_DIR="${1:-logs}"

found=0

if [[ ! -d "$LOG_DIR" ]]; then
    echo "Directory not found: $LOG_DIR"
    exit 1
fi

while IFS= read -r -d '' file; do
    if [[ -s "$file" ]]; then
        found=1
        echo "========================================"
        echo "ERROR FILE: $file"
        echo "========================================"
        cat "$file"
        echo
    fi
done < <(find "$LOG_DIR" -type f -name "*.err" -print0)

if [[ $found -eq 0 ]]; then
    echo "No non-empty .err files found in $LOG_DIR"
fi