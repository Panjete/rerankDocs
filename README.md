# rerankDocs
Psuedo Relevance Feedback using Query Expansion and Reranking

Considering COVID-19 to be one word currently
Is it guarenteed we'll have only 40 topics?
I am NOT lowercasing queries -- actually, should I?

Assuming that all queries have a number, and non-empty fields in query, question, and narrrative

metedata.csv sould have 192510 but has 191175 entries?

Use os library to join directories instead

Guarentees on json documents?
Add matadata to json reads. Include Bibrefs?

What happens when there is neither pdf and pmc - happens for 8l411r1w

Updated word2vec implementations by changing malloc.h ->stdlib.h

When multiple documents available, I just choose the first

remove \use{amspackage} latex tags

Issue with CSV reader

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
  