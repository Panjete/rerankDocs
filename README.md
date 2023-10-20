# rerankDocs
Psuedo Relevance Feedback using Query Expansion and Reranking

## To Handle :- 

1. Considering COVID-19 to be one word currently
2. Is it guarenteed we'll have only 40 topics?
3. I am lowercasing queries, text and  -- actually, should I?

4. Assuming that all queries have a number, and non-empty fields in query, question, and narrrative

5. metedata.csv sould have 192510 but has 191175 entries - Duplicates, resolved

6. Use os library to join directories instead

7. Guarentees on json documents?
8. Add matadata to json reads. Include Bibrefs?

9. What happens when there is neither pdf and pmc - happens for 8l411r1w -- Handled, read from .csv

10. Updated word2vec implementations by changing malloc.h ->stdlib.h -- make patch file

11. When multiple documents available, I just choose the first

12. remove \use{amspackage} latex tags

13. Issue with CSV reader --updated

14. PMC documents don't have abstract in them

15. What happens when word given to find closest meaning of, doesn't exist?

- Baseline Task 1 scores, mu = 200, questions :  0.1393, 0.5870, 0.5641, 0.4896
- Baseline Task 1 scores, mu = 100, questions :  0.1391, 0.5961, 0.5617, 0.4866
- Baseline Task 1 scores, mu = 50, questions :  0.1384, 0.5892, 0.5503, 0.4832
- Baseline Task 1 scores, mu = 20, questions :  0.1377, 0.5858, 0.5337, 0.4781
- Baseline Task 1 scores, mu = 10, questions :  0.1370, 0.5621, 0.5308, 0.4732
- Baseline Task 1 scores, mu =  1, questions :  0.1357, 0.5590, 0.5155, 0.4641

- Baseline Task 1 scores, mu = 50, narratives :  0.1384, 0.5892, 0.5503, 0.4832
- Baseline Task 1 scores, mu = 20, narratives :  0.1377, 0.5858, 0.5337, 0.4781

- Baseline Task 1 scores, mu = 1000, query :  0.1379, 0.6042, 0.5665, 0.4883
- Baseline Task 1 scores, mu = 200, query :  0.1380, 0.5986, 0.5609, 0.4889
- Baseline Task 1 scores, mu = 100, query :  0.1389, 0.6126, 0.5715, 0.4908
- Baseline Task 1 scores, mu = 50, query :  0.1389, 0.6181, 0.5734, 0.4921



* w2v_paper, q_narrative, mu = 100, top 10 : 0.1272, 0.4253, 0.4075, 0.3865
* w2v_paper, q_narrative, mu = 100, top 5 : 0.1383, 0.6066, 0.5827, 0.4873
* w2v_paper, q_narrative, mu = 100, top 2 : 0.1417, 0.6271, 0.6145, 0.5166  

* w2v_paper, q_question, mu = 100, top 10 : 0.1272, 0.4253, 0.4075, 0.3865
* w2v_paper, q_question, mu = 100, top 5 : 0.1383, 0.6066, 0.5827, 0.4873
* w2v_paper, q_question, mu = 100, top 2 : 0.1417, 0.6271, 0.6145, 0.5166  

* w2v_paper, q_question, mu = 50, top 10 : 0.1272, 0.4253, 0.4075, 0.3865
* w2v_paper, q_question, mu = 50, top 5 : 0.1384, 0.6207, 0.5797, 0.4886
* w2v_paper, q_question, mu = 50, top 2 : 0.1415, 0.6370, 0.5996, 0.5150

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



### FILE STRUCTURE 

#### To call the RM1 model - 

1. Call `lm_rerank.sh` with the apt arguments. The arguments expected by this file (in order) are called as `bash lm_rerank.sh [query-file] [top-100-file] [collection-dir] [output-file] [expansions-file]`

2. The script calls `top_rerank_rm1.py`, and passes the same arguments as above to it. This file is the flow-control of the entire task.

3. `top_rerank_rm1.py` calls a series of healper files for reading some of the data. These are :- 
    * `read_csv.py` :- Houses functionality to read the `metadata.csv` in the `[collection-dir]`
    * `read_qfile.py` :- Houses functionality to read and parse the `[query-file]`
    * `read_top100.py` :- Houses functionality to read and parse the `[top-100-file]`
    * `read_tjson.py` :- To read and parse a json file (pmc\_json/pdf\_json)

4. `rm1.py` is where the algorithmic implementations of the *RM1* model are housed. These include computing the per-document LM, the global-collection LM, and functionality for calculating the _query-document_ score. This score can now be used to re-rank the documents for a given query.

5. `top_rerank.py` iterates over the queries. For each query, it computes a score for the top100 documents that have been retrieved . Arranging these is a descending order, these results are written to the `[output-file]`.

6. Call `./getndcg.sh` to get nDCG and nDCG@{5,10,50} scores.
  
#### To call the Query Exmapnsion model - 

1. Call `w2v_rerank.sh` with the apt arguments. The arguments expected by this file (in order) are called as `bash w2v_rerank.sh [query-file] [top-100-file] [collection-dir] [output-file] [expansions-file]`

2. The script calls `top_rerank_w2v.py`, and passes the same arguments as above to it. This file is the flow-control of the entire task.

3. `top_rerank_w2v.py` calls a series of healper files for reading some of the data. These are :- 
    * `read_csv.py` :- Houses functionality to read the `metadata.csv` in the `[collection-dir]`
    * `read_qfile.py` :- Houses functionality to read and parse the `[query-file]`
    * `read_top100.py` :- Houses functionality to read and parse the `[top-100-file]`
    * `read_tjson.py` :- To read and parse a json file (pmc\_json/pdf\_json)

4. `word2vec.c` learns the local embeddings from a text file and stores them in a binary file. and `distance.c` houses the functions for computing the nearest words, when the input-word and binary file of the vector model are passed to it. `build.sh` compiles these files into executables `word2vec` and `distance`, which are called by the `top_rerank_w2v.py` using python's subprocess module; these executables can be called standalone using 
    * `time ./word2vec -train  <text_file_location> -output <vector_file> -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15` - stores vector embeddings in the [vector\_file]

    * `./distance <vector_file> <dest_file> <word>` - computes the top 40 nearest words for [word] and appends them to [dest\_file]

5. Call `./getndcg.sh` to get nDCG and nDCG@{5,10,50} scores.
