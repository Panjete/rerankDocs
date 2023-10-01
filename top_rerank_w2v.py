import argparse
from read_top100 import rt100
from read_qfile import qfile
from read_csv import rcsv
from read_tjson import read_text_json
import subprocess

aparser = argparse.ArgumentParser(description="Process filenames")
aparser.add_argument("query_file", nargs=1)
aparser.add_argument("top_100_file", nargs=1)
aparser.add_argument("collection_dir", nargs=1)
aparser.add_argument("output_file", nargs=1)
aparser.add_argument("expansions_file", nargs=1)
args = aparser.parse_args()


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

## Collecting symbols for w2v collection
out_ranks = {}
qnums_sorted = sorted(qmapping.keys())
for qnum in qnums_sorted:
    top100 = t40t100[qnum] # top 100 for this topic
    q_query, q_question, q_narr = qmapping(qnum) # get all data of this topic
    words = q_question ### TODO: Analyse choice
    this_q = ""

    for (corduid, _, _) in top100:
        pdf_path, pmc_path = file_locs_mapping(corduid)
        doc_path = ""  # For storing the preffered source
        if(pmc_path != ""):
            doc_path = pmc_path
        else:
            doc_path = pdf_path
        
        this_q += read_text_json(doc_path)
        ## Don't know if neither found
    out_ranks[qnum] = this_q
    with open("intm_data/"+str(qnum)+".txt", "w") as f:
        f.write(this_q)

for qnum in qnums_sorted:
    text_file_location = "intm_data/"+str(qnum)+".txt"
    vector_file = "intm/vector_" + str(qnum) + ".bin"
    subprocess.call([])




