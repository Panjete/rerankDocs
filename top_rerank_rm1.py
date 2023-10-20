import argparse
from read_top100 import rt100
from read_qfile import qfile
from read_csv import rcsv
import os
from math import log
from rm1 import generate_background, get_text_stats, get_document_stats, score_word

aparser = argparse.ArgumentParser(description="Process filenames")
aparser.add_argument("query_file", nargs=1)
aparser.add_argument("top_100_file", nargs=1)
aparser.add_argument("collection_dir", nargs=1)
aparser.add_argument("output_file", nargs=1)
args = aparser.parse_args()

query_file = args.query_file[0]
top_100_file = args.top_100_file[0]
collection_dir = args.collection_dir[0]
output_file = args.output_file[0]

## Initialise parameters for local runs
# query_file = "covid19-topics.xml"
# top_100_file = "t40-top-100.txt"
# collection_dir = "/Users/gsp/Downloads/2020-07-16"
# output_file = "out.txt"
## Call script using ./lm_rerank.sh covid19-topics.xml t40-top-100.txt /Users/gsp/Downloads/2020-07-16 out.txt

metadata_file = os.path.join(collection_dir, "metadata.csv")
pdf_json = os.path.join(collection_dir, "document_parses/pdf_json")
pmc_json = os.path.join(collection_dir, "document_parses/pmc_json")

t40t100 = rt100(top_100_file) ## contains an dictionary of Qnum -> array of tuples, (CORDid, Rank, Score)
qmapping = qfile(query_file)  ## mapping TopicNum -> (TopicNum, Query, Question, Narrative)
file_locs_mapping = rcsv(metadata_file) ## mapping from cord_id -> (pdf_file, pmc_file) 

mu = 100 ## Hyper-Parameter

## this loop saves the re-ranked results in a qnum -> ranks map (out_ranks)
out_ranks = {}
qnums_sorted = sorted(qmapping.keys())
for qnum in qnums_sorted:
    print("Processing qnum =", qnum)
    top100 = t40t100[qnum] # top 100 for this topic
    topic_num, q_query, q_question, q_narr = qmapping[qnum] # get all data of this topic
    queryterms = q_query ### TODO: Analyse choice
    this_q = {} 

    ## Instead of completely global, choosing background to be the top 100 instead
    text_from_non_link_files = ""
    links_of_link_avb_files = []
    local_vocabs = {} ## Houses mapping from corduid -> (docSize, docVocabulary)
    for (corduid, _, _) in top100:
        data_type, data_entry = file_locs_mapping[corduid]
        doc_path = ""  # For storing the preferred source

        if(data_type<2): ## Happens when pmc or pdf available, prefers pmc
            doc_path = os.path.join(collection_dir, data_entry)
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
        
    '''
    ## Compute the score for each of the top 100 docs
    for (corduid, _, _) in top100:

        data_type, data_entry = file_locs_mapping[corduid]
        doc_path = ""  # For storing the preferred source

        if(data_type<2): ## Happens when pmc or pdf available, prefers pmc
            doc_path = collection_dir+ data_entry
            this_q[corduid] = score_topic(queryterms, doc_path, global_vocab, global_size, mu) # score calculated for this corduid
        else:
            this_q[corduid] = score_text(queryterms, data_entry, global_vocab, global_size, mu) # score calculated for this corduid
        
    ## After scores computed, re-rank
    ranked_docs = sorted(this_q, key=lambda k: this_q[k], reverse=True)
    rkds = []
    for key in ranked_docs:
        rkds.append((key, str(this_q[key]))) # store re-ranked results for printing later
    
    out_ranks[qnum] = rkds
    '''
with open(output_file, 'w') as f:
    for qnum in qnums_sorted:
        i = 0
        for (corduid, val) in out_ranks[qnum]:
            f.write(str(qnum) + " Q0 " + corduid + " " + str(i) + " " + val + " " + "runid1\n")
            i += 1

'''
for query q:
    for w in (the set of all words in the vocabulary of the top 100 for q)
        score_document i = sum_over_w( P(w|R)*log(P(w|D)) ) ## KL divergence
        where, p(w|R) ~ p(w, q1, q2, .... qk) = sum_over_all_M( p(M) * p(w|M) * prod_allqueryterms( p(qi|M)))
            where, p(M) = 1/100
                   p(w|M) is dirichlet-smoothened, uses global statistics and stats of the document that makes M
                   p(qi|M), same as above, but for all query terms
        and log(P(w|D) is the same as log(p(w|M))
'''