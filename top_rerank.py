import argparse
from read_top100 import rt100
from read_qfile import qfile
from read_csv import rcsv
import os

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



t40t100 = rt100(top_100_file) ## contains an array of tuples. Tuple entries being (Qnum, CORDid, Rank, Score)
qmapping = qfile(query_file)  ## mapping TopicNum -> (TopicNum, Query, Question, Narrative)
file_locs_mapping = rcsv(metadata_file) ## mapping from cord_id -> (pdf_file, pmc_file) 

print(len(file_locs_mapping.keys()))













