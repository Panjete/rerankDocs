#!/bin/bash

rm trec_eval-9.0.7/out.txt
rm trec_eval-9.0.7/out_w2v.txt
cp out.txt trec_eval-9.0.7/out.txt
cp out_w2v.txt trec_eval-9.0.7/out_w2v.txt
cd trec_eval-9.0.7
echo "rm1 accuracies\n"
./trec_eval -m ndcg -m ndcg_cut.5,10,50 t40-qrels.txt out.txt
echo "w2v accuracies\n"
./trec_eval -m ndcg -m ndcg_cut.5,10,50 t40-qrels.txt out_w2v.txt
cd ..