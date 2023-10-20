from read_tjson import read_text_json
import os
from math import log2, isclose

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


## Pass in the text, get freq mapping and size
def get_text_stats(text):
    words = text.split()
    freq = {}
    for word in words:
        word = word.lower()
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    return freq, len(words)

## from all the documents that have a pdf/pmc, and the text of docs that don't
## return the freq map and size as the general background
def generate_background(list_paths, text):
    ## Generate background from the top100 documents per query
    ## Some of these documents have a pdf/pmc, while some have just the text extracted from metadata.csv
    glob_freq = {}
    vocab_size = 0
    for filename in list_paths:
        loc_freq, loc_siz = get_document_stats(filename)
        vocab_size += loc_siz
        for key in loc_freq.keys():
            if key in glob_freq:
                glob_freq[key] += loc_freq[key]
            else:
                glob_freq[key] = loc_freq[key]

    text_f, text_s = get_text_stats(text)
    vocab_size += text_s
    for key in text_f.keys():
        if key in glob_freq:
            glob_freq[key] += text_f[key]
        else:
            glob_freq[key] = text_f[key]

    return glob_freq, vocab_size



## Calculated p(w|M) -> dirichlet smoothened distribution of model yielding the word w
## requires the document distribution (dfi) and the background distbn (global_vocab)
def score_word(word, corduid, mu, local_vocabs, global_vocab, global_size):
    local_freq, local_siz = local_vocabs[corduid]
    numerator = local_freq.get(word, 0) + mu * (global_vocab.get(word, 0)/global_size)
    denominator = local_siz + mu
    return numerator/denominator

## Not using functions beyond this point
## Get background stats and size
def get_collection_stats(dirname1, dirname2):
    glob_freq = {}
    vocab_size = 0
    dirs = [dirname1, dirname2]
    for dirname in dirs:
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
        numerator = local_freq.get(word, 0) + mu * (global_vocab.get(word, 0)/gvs)
        denominator = local_siz + mu
        if not isclose(numerator, 0):
            score += (log2(numerator/denominator))
    return score

## Calculate score given words, text, global vocab and mu (hyper-parameter)
def score_text(words, text, global_vocab, gvs,  mu):
    local_freq, local_siz = get_text_stats(text)
    score = 0.0
    for word in words:
        numerator = local_freq.get(word, 0) + mu * (global_vocab.get(word, 0)/gvs)
        denominator = local_siz + mu
        #print(word, "num = ", numerator, "den =", denominator)
        if not isclose(numerator, 0):
            score += (log2(numerator/denominator))
        #score += (log2(numerator/denominator))
    return score

#print(get_document_stats("/Users/gsp/Downloads/2020-07-16/document_parses/pdf_json/0a0afb5dc02afa81689e0e75afe2f9a21ce09e70.json")["pharmacological"])