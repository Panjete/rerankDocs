#!/bin/bash

echo "Processing started!" 
args=()
while [ "$1" != "" ]; do
    args+=("$1")
    shift
done
python top_rerank_rm1.py "${args[@]}"
echo "Shell script successfully terminated!"
