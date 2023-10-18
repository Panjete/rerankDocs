#!/bin/bash

rm trec_eval-9.0.7/out.txt
cp out.txt trec_eval-9.0.7/out.txt
cd trec_eval-9.0.7
./trec_eval -m ndcg -m ndcg_cut.5,10,50 t40-qrels.txt out.txt
cd ..