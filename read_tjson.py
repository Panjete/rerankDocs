import json

def read_text_json(filename):
    with open(filename, "r") as json_file:
        data = json.load(json_file)

    title_text = ""
    authors = []
    if data.get("metadata", "null") != "null":
        title_text = data["metadata"].get("title", "unknown")
        authors = data["metadata"].get("authors", "unknown")

    abst_text = ""
    if data.get("abstract", "null") != "null":
        abst_text = data["abstract"][0].get("text", "unknown")

    texts = ""
    for bts in data.get("body_text", {}):
        texts += bts.get("text", "unknown")

    return texts

#print(read_text_json("/Users/gsp/Downloads/2020-07-16/document_parses/pmc_json/PMC59549.xml.json"))
#print(read_text_json("/Users/gsp/Downloads/2020-07-16/document_parses/pdf_json/0a0afb5dc02afa81689e0e75afe2f9a21ce09e70.json"))


        
