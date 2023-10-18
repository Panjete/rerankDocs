#!/bin/bash

echo "Processing started!" 
args=()
while [ "$1" != "" ]; do
    args+=("$1")
    shift
done
mkdir intm_data
rm intm_data/nw_*
python top_rerank_w2v.py "${args[@]}"

echo "Shell script successfully terminated!"
