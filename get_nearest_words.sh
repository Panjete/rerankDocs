#!/bin/bash

## called using ./get_nearest_words.sh vector_qnum.bin word
## calls ./distance vector_qnum.bin word
## Appends nearest words to nw_qnum.txt

input_filename="$1"
word="$2"

./distance $input_filename $word

