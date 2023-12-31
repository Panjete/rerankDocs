import argparse
from read_top100 import rt100
from read_qfile import qfile
from read_csv import rcsv
from read_tjson import read_text_json
import subprocess
from math import log
from rm1 import generate_background, get_text_stats, get_document_stats, score_word
import numpy as np
import os

aparser = argparse.ArgumentParser(description="Process filenames")
aparser.add_argument("query_file", nargs=1)
aparser.add_argument("top_100_file", nargs=1)
aparser.add_argument("collection_dir", nargs=1)
aparser.add_argument("output_file", nargs=1)
aparser.add_argument("expansions_file", nargs=1)

args = aparser.parse_args()
query_file = args.query_file[0]
top_100_file = args.top_100_file[0]
collection_dir = args.collection_dir[0]
output_file = args.output_file[0]
expansions_file = args.expansions_file[0]

## Initialise parameters for local runs
# query_file = "covid19-topics.xml"
# top_100_file = "t40-top-100.txt"
# collection_dir = "/Users/gsp/Downloads/2020-07-16/"
# output_file = "out_w2v.txt"
# expansions_file = "exp.txt"
## Call script using ./w2v_rerank.sh covid19-topics.xml t40-top-100.txt /Users/gsp/Downloads/2020-07-16 out_w2v.txt exp.txt



metadata_file = os.path.join(collection_dir, "metadata.csv")
pdf_json = os.path.join(collection_dir, "document_parses/pdf_json")
pmc_json = os.path.join(collection_dir, "document_parses/pmc_json")

already_learnt = False ## TODO: set to false in the start
expand_top_k = 5
mu = 100


t40t100 = rt100(top_100_file) ## contains an dictionary of Qnum -> array of tuples, (CORDid, Rank, Score)
qmapping = qfile(query_file)  ## mapping TopicNum -> (TopicNum, Query, Question, Narrative)
file_locs_mapping = rcsv(metadata_file) ## mapping from cord_id -> (0, pmc_file) | (1, pdf_file) | (2, text) | (3, "") 

## Collecting symbols for w2v collection
## This loop is able to write 40 documents, each containing text from top100 of that query
## These 40 interim documents will be used to train w2v binary file, later
out_ranks = {}
qnums_sorted = sorted(qmapping.keys())
for qnum in qnums_sorted:
    top100 = t40t100[qnum] # top 100 for this topic
    this_q = ""
    for (corduid, _, _) in top100:
        data_type, data_entry = file_locs_mapping[corduid]
        doc_path = ""  # For storing the preferred source
        if(data_type <2): ## Happens when pmc or pdf available, prefers pmc
            doc_path = os.path.join(collection_dir, data_entry)
            this_q += read_text_json(doc_path) + " "
        else: ## Happens when only metadata available
            this_q += data_entry + " "

    out_ranks[qnum] = this_q
    with open("intm_data/"+str(qnum)+".txt", "w") as f:
        f.write(this_q)

print("Data for learning local word embeddings collected!")

## Learning Local embeddings
if not already_learnt:
    for qnum in qnums_sorted:
        text_file_location = "intm_data/"+str(qnum)+".txt"
        vector_file = "intm_data/vector_" + str(qnum) + ".bin"
        command = "time ./word2vec -train " + text_file_location + " -output " + vector_file + " -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 0 -iter 15"
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

## Now finding query expansion terms per query
expanded_words = {}
extra_terms = ["of", "the", "is", "a", "an", "to"]
for qnum in qnums_sorted:
    vector_file = "intm_data/vector_" + str(qnum) + ".bin"
    qqnum, q_query, q_question, q_narr = qmapping[qnum] # get all data of this topic
    words = q_narr ### TODO: Analyse choice
    words_string = " ".join(words)
    expanded_words[qnum] = [] 
    with open(vector_file, 'r') as f:
        lines = f.readlines()

    map_index_word = {} ## stores words -> index mapping
    map_word_index = {} ## stores index -> words mapping
    u = []
    for i, line in enumerate(lines[1:]):
        vals = line.split()
        row = [float(vals[i]) for i in range(1, len(vals))]
        word = vals[0]
        map_index_word[word] = i
        map_word_index[i] = word
        u.append(row)

    U = np.array(u)
    U_mul_Ut = np.dot(U, U.transpose())

    v = U.shape[0]
    one_indices = [] ## to store those indices of terms which occur in the dictionary
    for word in words:
        if word in map_index_word.keys():
            one_indices.append(map_index_word[word])

    a = np.array(one_indices)
    query_vector = np.zeros((v,1), dtype=int)
    query_vector[a] = 1
    distance_scores = np.dot(U_mul_Ut, query_vector)

    ## multiply U * Ut * q
    sorted_indices = np.argsort(distance_scores.flatten())[::-1]
    top_k_indices = sorted_indices[:expand_top_k]
    top_k_words = [map_word_index[i] for i in top_k_indices]
    for word in top_k_words:
        if word not in extra_terms:
                expanded_words[qnum].append(word)
    print("Expansion words found for qnum =", qnum)

'''
## finding nearest words for all query terms
for qnum in qnums_sorted:
    vector_file = "intm_data/vector_" + str(qnum) + ".bin"
    dest_file = "intm_data/nw_" + str(qnum) + ".txt"
    qqnum, q_query, q_question, q_narr = qmapping[qnum] # get all data of this topic
    words = q_query ### TODO: Analyse choice

    for word in words:
        with open(dest_file, "a") as f:
            f.write("word = " + word + "    ")
        command = "./distance " + vector_file + " " + dest_file + " " + word
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_output = process.stdout.decode('utf-8')
        stderr_output = process.stderr.decode('utf-8')

        # Print the standard output and standard error
        # if stdout_output:
        #     print("Standard Output:")
        #     print(stdout_output)
        # if stderr_output:
        #     print("Standard Error:")
        #     print(stderr_output)
        # if process.returncode != 0:
        #     print("Error creating nearest words for word,  qnum = ", word, qnum)

extra_terms = ["of", "the", "is", "a", "an", "to"]
expanded_words = {}
for qnum in qnums_sorted:
    nw_file = "intm_data/nw_" + str(qnum) + ".txt"
    expanded_words[qnum] = [] 
    with open(nw_file, "r") as f:
        nw_lines= f.readlines()
        for line in nw_lines:
            if(len(line.split()) == 5):
                new_word = line.split()[3]
                if new_word not in extra_terms:
                    expanded_words[qnum].append(new_word)

'''
for qnum in qnums_sorted:
    print("Expanded words for qnum =", qnum, " = ", expanded_words[qnum])
## collected all expanded words , now rerank

for qnum in qnums_sorted:
    print("Processing qnum =", qnum)
    top100 = t40t100[qnum] # top 100 for this topic
    topic_num, q_query, q_question, q_narr = qmapping[qnum] # get all data of this topic
    queryterms = q_narr + expanded_words[qnum] ### TODO: Analyse choice
    this_q = {} 

    ## Instead of completely global, choosing background to be the top 100 instead
    text_from_non_link_files = ""
    links_of_link_avb_files = []
    local_vocabs = {} ## Houses mapping from corduid -> (docSize, docVocabulary)
    for (corduid, _, _) in top100:
        data_type, data_entry = file_locs_mapping[corduid]
        doc_path = ""  # For storing the preferred source

        if(data_type<2): ## Happens when pmc or pdf available, prefers pmc
            doc_path = collection_dir+ data_entry
            links_of_link_avb_files.append(doc_path)
            local_vocabs[corduid] = get_document_stats(doc_path)
        else:
            text_from_non_link_files += data_entry + " "
            local_vocabs[corduid] = get_text_stats(data_entry)

    global_vocab, global_size = generate_background(links_of_link_avb_files, text_from_non_link_files) ## Include Both dirs
    
    # '''
    this_q_scores = dict([(corduid, 0.0) for (corduid, _, _) in top100]) ## Initialises id->score dict
    for w in global_vocab:
        p_w_R = 0.0
        for d, _, _ in top100:
            this_entry = 1/100 * score_word(w, d, mu, local_vocabs, global_vocab, global_size)
            for qterm_ in queryterms:
                this_entry *= score_word(qterm_ , d, mu, local_vocabs, global_vocab, global_size)
            p_w_R += this_entry
        for d, _, _ in top100:
            this_q_scores[d] += (p_w_R * log(score_word(w, d, mu, local_vocabs, global_vocab, global_size)))

    ## After scores computed, re-rank
    ranked_docs = sorted(this_q_scores, key=lambda k: this_q_scores[k], reverse=True)
    rkds = []
    for key in ranked_docs:
        rkds.append((key, str(this_q_scores[key]))) # store re-ranked results for printing later
    out_ranks[qnum] = rkds
        
with open(output_file, 'w') as f:
    for qnum in qnums_sorted:
        i = 0
        for (corduid, val) in out_ranks[qnum]:
            f.write(str(qnum) + " Q0 " + corduid + " " + str(i) + " " + val + " " + "runid1\n")
            i += 1
        
with open(expansions_file, 'w') as f:
    for qnum in qnums_sorted:
        f.write(str(qnum) + " : ")
        for word in expanded_words[qnum]:
            f.write(str(word) + " ")
        f.write("\n")
            