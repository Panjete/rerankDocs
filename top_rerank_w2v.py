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

already_learnt = True ## TODO: set to false in the start

t40t100 = rt100(top_100_file) ## contains an dictionary of Qnum -> array of tuples, (CORDid, Rank, Score)
qmapping = qfile(query_file)  ## mapping TopicNum -> (TopicNum, Query, Question, Narrative)
file_locs_mapping = rcsv(metadata_file) ## mapping from cord_id -> (0, pmc_file) | (1, pdf_file) | (2, text) | (3, "") 
x = 0
## Collecting symbols for w2v collection
## This loop is able to write 40 documents, each containing text from top100 of that query
## These 40 interim documents will be used to train w2v binary file, later
out_ranks = {}
qnums_sorted = sorted(qmapping.keys())
for qnum in qnums_sorted:
    top100 = t40t100[qnum] # top 100 for this topic
    qqnum, q_query, q_question, q_narr = qmapping[qnum] # get all data of this topic
    words = q_question ### TODO: Analyse choice
    this_q = ""
    for (corduid, _, _) in top100:
        data_type, data_entry = file_locs_mapping[corduid]
        doc_path = ""  # For storing the preferred source
        x+= 1
        if(data_type <2): ## Happens when pmc or pdf available, prefers pmc
            doc_path = collection_dir + data_entry
            this_q += read_text_json(doc_path) + " "
        else: ## Happens when only metadata available
            this_q += data_entry + " "

    out_ranks[qnum] = this_q
    with open("intm_data/"+str(qnum)+".txt", "w") as f:
        f.write(this_q)
    print("x = ", x)


## Learning Local embeddings
if not already_learnt:
    for qnum in qnums_sorted:
        text_file_location = "intm_data/"+str(qnum)+".txt"
        vector_file = "intm_data/vector_" + str(qnum) + ".bin"
        command = "time ./word2vec -train " + text_file_location + " -output " + vector_file + " -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15"
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout_output = process.stdout.decode('utf-8')
        stderr_output = process.stderr.decode('utf-8')

        # Print the standard output and standard error
        if stdout_output:
            print("Standard Output:")
            print(stdout_output)

        if stderr_output:
            print("Standard Error:")
            print(stderr_output)

        if process.returncode != 0:
            print("Error creating local w2v for qnum = ", qnum)
        else:
            print("Created local w2v for qnum = ", qnum)


## finding nearest words for all query terms
for qnum in qnums_sorted:
    vector_file = "intm_data/vector_" + str(qnum) + ".bin"
    dest_file = "intm_data/nw_" + str(qnum) + ".txt"
    qqnum, q_query, q_question, q_narr = qmapping[qnum] # get all data of this topic
    words = q_question ### TODO: Analyse choice

    for word in words:
        with open(dest_file, "a") as f:
            f.write("word = " + word + "    ")
        command = "./distance " + vector_file + " " + dest_file + " " + word
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_output = process.stdout.decode('utf-8')
        stderr_output = process.stderr.decode('utf-8')

        # Print the standard output and standard error
        if stdout_output:
            print("Standard Output:")
            print(stdout_output)
        if stderr_output:
            print("Standard Error:")
            print(stderr_output)
        if process.returncode != 0:
            print("Error creating nearest words for word,  qnum = ", word, qnum)




