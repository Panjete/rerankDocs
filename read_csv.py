import csv

## Returns a mapping from cord_id -> (pdf_file, pmc_file) 
def rcsv(filename):
    mapping_to_files = {}
    with open(filename, mode='r') as f:
        reader = csv.DictReader(f)
        #relv_columns = ['cord_uid', 'pdf_json_files', 'pmc_json_files']
        for row in reader:
            cord_uid = row.get('cord_uid', '')
            pdf_file = row.get('pdf_json_files', '')
            pmc_file = row.get('pmc_json_files', '')
            if(cord_uid == ''):
                print("oops, row without CORD_uid")
            mapping_to_files[cord_uid] = (pdf_file, pmc_file)
    return mapping_to_files


# mpf = rcsv("/Users/gsp/Downloads/2020-07-16/metadata.csv")
# print("total files = ", len(mpf.keys()))
# print("entries for file = 8qnrcgnk" , mpf["8qnrcgnk"])
