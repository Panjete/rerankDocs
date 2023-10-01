from read_tjson import read_text_json
import os
from math import log2

## Pass in the full path of the file, get freq mapping and size
def get_document_stats(filename):
    text = read_text_json(filename)
    words = text.split()
    freq = {}
    for word in words:
        word = word.lower()
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    return freq, len(words)

## Get background stats and size
def get_collection_stats(dirname):
    glob_freq = {}
    vocab_size = 0
    for file_only_name in os.listdir(dirname):
        filename = os.path.join(dirname, file_only_name)
        loc_freq, loc_siz = get_document_stats(filename)
        vocab_size += loc_siz

        for key in loc_freq.keys():
            if key in glob_freq:
                glob_freq[key] += loc_freq[key]
            else:
                glob_freq[key] = loc_freq[key]
            
    return glob_freq, vocab_size

## Calculate score given words, doc path, global vocab and mu (hyper-parameter)
def score_topic(words, doc, global_vocab, gvs,  mu):
    local_freq, local_siz = get_document_stats(doc)
    score = 0.0
    for word in words:
        numerator = local_freq[word] + mu * (global_vocab[word]/gvs)
        denominator = local_siz + mu
        score += (log2(numerator/denominator))
    return score


#print(get_document_stats("/Users/gsp/Downloads/2020-07-16/document_parses/pdf_json/0a0afb5dc02afa81689e0e75afe2f9a21ce09e70.json")["pharmacological"])