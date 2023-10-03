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
