#!/bin/bash

## called using ./get_nearest_words.sh vector_qnum.bin word
## calls ./distance vector_qnum.bin word
## Appends nearest words to nw_qnum.txt

## Currently unused

input_filename="$1"
output_filename="$2"
word="$3"

./distance $input_filename $output_filename $word

