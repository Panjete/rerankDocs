import json

def read_text_json(filename):
    with open(filename, "r") as json_file:
        data = json.load(json_file)

    title_text = data["metadata"]["title"]
    authors = data["metadata"]["authors"]
    abst_text = data["abstract"]["text"]

    texts = ""
    for bts in data["body_text"]:
        texts += bts["text"]

   
        

    return texts


        
