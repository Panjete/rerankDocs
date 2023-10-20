import json
import re

## returns pruned text after parsing the json file passed in
def read_text_json(filename):
    with open(filename, "r") as json_file:
        data = json.load(json_file)

    title_text = ""
    authors_names = ""
    meta_data = data.get("metadata", "null")
    if  meta_data != "null":
        title_text = meta_data.get("title", "title")
        authors   = meta_data.get("authors", [])
        for author in authors:
            authors_names += author.get("first", "fname") + " " + author.get("last", "lname") + " "
            if len(author.get("middle", []))!= 0:
                authors_names += author.get("middle", [])[0] + " "

    abst_text = ""
    abs_entries = data.get("abstract", [])
    if  len(abs_entries) != 0:
        for entry in abs_entries:
            abst_text += entry.get("text", "abstract") + " "

    texts = ""
    for bts in data.get("body_text", {}):
        texts += bts.get("text", "unknown") + " "

    total_texts = re.sub(r'[^a-zA-Z0-9\s\-]', '', title_text + " " + authors_names + " " + abst_text + " " + texts).lower()
    return total_texts

#print(read_text_json("/Users/gsp/Downloads/2020-07-16/document_parses/pmc_json/PMC59549.xml.json"))
#print(read_text_json("/Users/gsp/Downloads/2020-07-16/document_parses/pdf_json/0a0afb5dc02afa81689e0e75afe2f9a21ce09e70.json"))


        
