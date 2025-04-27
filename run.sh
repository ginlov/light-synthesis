#/bin/bash

# Ensure start and end variables are provided
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <start> <end>"
  exit 1
fi

start=$1
end=$2

export INPUT_PATH="/data/org"
export OUTPUT_PATH="cropped"

python ic_light.py --input_dir $INPUT_PATH --out_path $OUTPUT_PATH --start $start --end $end