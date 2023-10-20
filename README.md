# reRankDocs
Psuedo Relevance Feedback using Query Expansion and Reranking

## To call the RM1 model - 

1. Call `lm_rerank.sh` with the apt arguments. The arguments expected by this file (in order) are called as `bash lm_rerank.sh [query-file] [top-100-file] [collection-dir] [output-file] [expansions-file]`

2. The script calls `top_rerank_rm1.py`, and passes the same arguments as above to it. This file is the flow-control of the entire task.

3. `top_rerank_rm1.py` calls a series of healper files for reading some of the data. These are :- 
    * `read_csv.py` :- Houses functionality to read the `metadata.csv` in the `[collection-dir]`
    * `read_qfile.py` :- Houses functionality to read and parse the `[query-file]`
    * `read_top100.py` :- Houses functionality to read and parse the `[top-100-file]`
    * `read_tjson.py` :- To read and parse a json file (pmc\_json/pdf\_json)

4. `rm1.py` is where the algorithmic implementations of the *RM1* model are housed. These include computing the per-document LM, the global-collection LM, and functionality for calculating the _query-document_ score. This score can now be used to re-rank the documents for a given query.

5. `top_rerank.py` iterates over the queries. For each query, it computes a score for the top100 documents that have been retrieved . Arranging these is a descending order, these results are written to the `[output-file]`.


  
## To call the Query Expansion model - 

1. Call `w2v_rerank.sh` with the apt arguments. The arguments expected by this file (in order) are called as `bash w2v_rerank.sh [query-file] [top-100-file] [collection-dir] [output-file] [expansion-file]`

2. The script calls `top_rerank_w2v.py`, and passes the same arguments as above to it. This file is the flow-control of the entire task.

3. `top_rerank_w2v.py` calls a series of healper files for reading some of the data. These are :- 
    * `read_csv.py` :- Houses functionality to read the `metadata.csv` in the `[collection-dir]`
    * `read_qfile.py` :- Houses functionality to read and parse the `[query-file]`
    * `read_top100.py` :- Houses functionality to read and parse the `[top-100-file]`
    * `read_tjson.py` :- To read and parse a json file (pmc\_json/pdf\_json)

4. `word2vec` trains on the `intm_data/i.txt` for the ith query, and yields a `intm_data/vector_i.bin`, from which the embedding matrix U can be extracted for this query. This is then used to calculate a per-term score for terms in the vocabulary via `U* U^T * q`, and the top-k terms thus appearing are selected as expansion terms.

5. These expansion terms are appended to the original query terms, and the RM1 model above is then applied for re-ranking the scores.

7. The re-ranked results are written to the `[output-file]` and the expansions to `[expansions-file]`

#### Getting nDCG scores :

1. Copy the `[output-file]` and the `[t40-qrels.txt]` (the relevance scores file) into `trec_eval-9.0.7/`. 
2. Ensure that the `trec_eval-9.0.7/` has been compiled. Else run `make`.
3. Run `./trec_eval -m ndcg -m ndcg_cut.5,10,50 [t40-qrels.txt] [output-file]` to obtain the nDCG values!

## Results and Scores 

- RM1 scores, mu = 200, questions :  0.1415, 0.6028, 0.6089, 0.5139
- RM1 scores, mu = 100, questions :  0.1421, 0.6249, 0.6094, 0.5159
- RM1 scores, mu = 50, questions :  0.1416, 0.6300, 0.5932, 0.5122
- RM1 scores, mu = 20, questions :  0.1407, 0.6026, 0.5800, 0.5056
- RM1 scores, mu = 10, questions :  0.1399, 0.5745, 0.5680, 0.4965
- RM1 scores, mu =  1, questions :  0.1363, 0.5207, 0.5297, 0.4700
--
- RM1 scores, mu = 200, narratives :  0.1415, 0.6028, 0.6089, 0.5139
- RM1 scores, mu = 100, narratives :  0.1421, 0.6249, 0.6094, 0.5159
- RM1 scores, mu = 50, narratives :  0.1416, 0.6300, 0.5932, 0.5122
- RM1 scores, mu = 10, narratives :  0.1399, 0.5745, 0.5680, 0.4965
--
- RM1 scores, mu = 1000, query :  0.1388, 0.6152, 0.5378, 0.4899
- RM1 scores, mu = 200, query :  0.1404, 0.6174, 0.5894, 0.5121
- RM1 scores, mu = 100, query :  0.1417, 0.6303, 0.6055, 0.5193
- RM1 scores, mu = 50, query :  0.1417, 0.6252, 0.6091, 0.5197
- RM1 scores, mu = 10, query :  0.1399, 0.5991, 0.5618, 0.5082

----

* w2v_paper, q_narrative, mu = 100, top 10 : 0.1272, 0.4253, 0.4075, 0.3865
* w2v_paper, q_narrative, mu = 100, top 5 : 0.1383, 0.6066, 0.5827, 0.4873
* w2v_paper, q_narrative, mu = 100, top 2 : 0.1417, 0.6271, 0.6145, 0.5166  
--
* w2v_paper, q_question, mu = 100, top 10 : 0.1272, 0.4253, 0.4075, 0.3865
* w2v_paper, q_question, mu = 100, top 5 : 0.1383, 0.6066, 0.5827, 0.4873
* w2v_paper, q_question, mu = 100, top 2 : 0.1417, 0.6271, 0.6145, 0.5166  

* w2v_paper, q_question, mu = 50, top 10 : 0.1272, 0.4253, 0.4075, 0.3865
* w2v_paper, q_question, mu = 50, top 5 : 0.1384, 0.6207, 0.5797, 0.4886
* w2v_paper, q_question, mu = 50, top 2 : 0.1415, 0.6370, 0.5996, 0.5150
--
* w2v_paper, q_query, mu = 50, top 20 : 0.1272, 0.4253, 0.4075, 0.3865
* w2v_paper, q_query, mu = 50, top 10 : 0.1372, 0.5729, 0.5469, 0.4913
* w2v_paper, q_query, mu = 50, top 5 : 0.1400, 0.6029, 0.5725, 0.5056
* w2v_paper, q_query, mu = 50, top 2 : 0.1398, 0.6089, 0.5925, 0.5123
* w2v_paper, q_query, mu = 50, top 1 : 0.1409, 0.6224, 0.6036, 0.5191

* w2v_paper, q_query, mu = 100, top 20 : 0.1272, 0.4253, 0.4075, 0.3865
* w2v_paper, q_query, mu = 100, top 10 : 0.1399, 0.6014, 0.5833, 0.5010
* w2v_paper, q_query, mu = 100, top 5 : 0.1399, 0.5964, 0.5784, 0.5057
* w2v_paper, q_query, mu = 100, top 2 : 0.1401, 0.6104, 0.5937, 0.5123
* w2v_paper, q_query, mu = 100, top 1 : 0.1407, 0.6268, 0.5998, 0.5160