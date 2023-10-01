#!/bin/bash

## Learns from a text file, and writes it to .bin
## Use to learn the top 100 docs for each query
if [ $# -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

input_filename="$1"
if [ ! -f "$input_filename" ]; then
    echo "Input file '$input_filename' does not exist."
    exit 1
fi



output_filename="vector_${input_filename%.*}.bin"

time ./word2vec -train $input_filename -output $output_filename -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15
