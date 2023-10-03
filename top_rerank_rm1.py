import argparse
from read_top100 import rt100
from read_qfile import qfile
from read_csv import rcsv
import os
from rm1 import get_collection_stats, score_topic, score_text

aparser = argparse.ArgumentParser(description="Process filenames")
aparser.add_argument("query_file", nargs=1)
aparser.add_argument("top_100_file", nargs=1)
aparser.add_argument("collection_dir", nargs=1)
aparser.add_argument("output_file", nargs=1)
aparser.add_argument("expansions_file", nargs=1)
args = aparser.parse_args()

# query_file = args.query_file[0]
# top_100_file = args.top_100_file[0]
# collection_dir = args.collection_dir[0]
# output_file = args.output_file[0]
# expansions_file = args.expansions_file[0]

## Initialise parameters for local runs
query_file = "covid19-topics.xml"
top_100_file = "t40-top-100.txt"
collection_dir = "/Users/gsp/Downloads/2020-07-16/"
output_file = "out.txt"
expansions_file = "exp.txt"

metadata_file = collection_dir + "metadata.csv"
pdf_json = collection_dir + "document_parses/pdf_json"
pmc_json = collection_dir + "document_parses/pmc_json"



t40t100 = rt100(top_100_file) ## contains an dictionary of Qnum -> array of tuples, (CORDid, Rank, Score)
qmapping = qfile(query_file)  ## mapping TopicNum -> (TopicNum, Query, Question, Narrative)
file_locs_mapping = rcsv(metadata_file) ## mapping from cord_id -> (pdf_file, pmc_file) 



global_vocab, global_size = get_collection_stats(pdf_json, pmc_json) ## Include Both dirs
mu = 50 ## Hyper-Parameter

## this loop saves the re-ranked results in a qnum -> ranks map (out_ranks)
out_ranks = {}
qnums_sorted = sorted(qmapping.keys())
for qnum in qnums_sorted:
    top100 = t40t100[qnum] # top 100 for this topic
    q_query, q_question, q_narr = qmapping[qnum] # get all data of this topic
    words = q_question ### TODO: Analyse choice
    this_q = {} 
    ## Compute the score for each of the top 100 docs
    for (corduid, _, _) in top100:

        data_type, data_entry = file_locs_mapping[corduid]
        doc_path = ""  # For storing the preferred source

        if(data_type<2): ## Happens when pmc or pdf available, prefers pmc
            doc_path = collection_dir+ data_entry
            this_q[corduid] = score_topic(words, doc_path, global_vocab, global_size, mu) # score calculated for this corduid
        else:
            this_q[corduid] = score_text(words, data_entry, global_vocab, global_size, mu) # score calculated for this corduid
        
    ## After scores computed, re-rank
    ranked_docs = sorted(this_q, key=lambda k: this_q[k], reverse=True)
    rkds = []
    for key in ranked_docs:
        rkds.append((key, str(this_q[key]))) # store re-ranked results for printing later
    
    out_ranks[qnum] = rkds

with open(output_file, 'w') as f:
    for qnum in qnums_sorted:
        i = 0
        for (corduid, val) in out_ranks[qnum]:
            f.write(str(qnum) + " Q0 " + corduid + " " + str(i) + " " + val + " " + "runid1")
            i += 1

