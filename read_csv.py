import csv
import re

## Returns a mapping from cord_id -> (0, pmc_json_file) if found
## Else, cord_id -> (1, pdf_json_file) if found
## Else, when both loxations are empty, gives  cord_id -> (2, text_details)
## If nothing found, gives cord_id -> (3, "")
def rcsv(filename):
    mapping_to_files = {}
    with open(filename, mode='r') as f:
        reader = csv.DictReader(f)
        #relv_columns = ['cord_uid', 'pdf_json_files', 'pmc_json_files']
        for row in reader:
            cord_uid = row.get('cord_uid', '')
            pdf_file = row.get('pdf_json_files', '')
            pmc_file = row.get('pmc_json_files', '')

            if(pdf_file!= ""):
                pdf_file = pdf_file.split(";")[0]
            if(pmc_file != ""):
                pmc_file = pmc_file.split(";")[0] ## Handles multiple locations

            title = row.get('title', '')
            abstract = row.get('abstract', '') 
            authors = " ".join(row.get("authors", '').split(";"))
            textual_details = re.sub(r'[^a-zA-Z0-9\s\-]', '', title + " " + abstract + " " + authors).lower()

            if(cord_uid == ''): 
                print("oops, row without CORD_uid") ## None so far.

            if(cord_uid in mapping_to_files): ## When already found, update if upgrade available
    
                type_data, data = mapping_to_files[cord_uid]
                if(type_data == 1 and pmc_file != ""):
                    mapping_to_files[cord_uid] = (0, pmc_file)
                elif(type_data == 2 or type_data == 3):
                    if(pmc_file != ""):
                        mapping_to_files[cord_uid] = (0, pmc_file)
                    elif(pdf_file != ""):
                        mapping_to_files[cord_uid] = (1, pdf_file)
                elif(type_data == 3 and (title!= "" or abstract != "" or authors!= "")):
                    mapping_to_files[cord_uid] = (2, textual_details)

            else:
                if(pmc_file != ""):
                    mapping_to_files[cord_uid] = (0, pmc_file)
                elif(pdf_file != ""):
                    mapping_to_files[cord_uid] = (1, pdf_file)
                elif(title!= "" or abstract != "" or authors!= ""):
                    mapping_to_files[cord_uid] = (2, textual_details)
                else:
                    mapping_to_files[cord_uid] = (3, "")

    return mapping_to_files


# mpf = rcsv("/Users/gsp/Downloads/2020-07-16/metadata.csv")
# print("total files = ", len(mpf.keys()))
# print("entries for file = 8qnrcgnk" , mpf["8qnrcgnk"])
# print("entries for file = wt2gctys" , mpf["wt2gctys"])
# print("entries for file = 3js467lu" , mpf["3js467lu"])
# print("entries for file = ornjq3o9" , mpf["ornjq3o9"])
