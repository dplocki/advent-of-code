#!/bin/bash

year=$(date +%Y)
day=$(date +%d)

script_path="${year}/${year}_${day}.py"

if [[ -f "$script_path" ]]; then
    time python3 "$script_path"
else
    echo "Error: Script $script_path does not exist."
    exit 1
fi
