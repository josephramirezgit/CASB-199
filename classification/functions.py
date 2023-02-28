import requests
import json
import csv
import threading
import time

def extract_functions(protein_list: list, path: str) -> None:
    with open(path, 'a') as f:
        for protein in protein_list:
            # extract request
            url = "https://rest.uniprot.org/uniprotkb/" + protein + ".json"
            r = requests.get(url)
            request = r.json()

            # extract functions
            try:
                comment = request["comments"]
                for idx, content in enumerate(comment):
                    if comment[idx]['commentType'] == 'FUNCTION':
                        for j in range(len(comment[idx]['texts'])):
                            to_add = str(protein + '|' + comment[idx]['texts'][j]['value'])
                            f.write(to_add)
                            f.write('\n')
            except:
                pass

def extract_proteins(path: str) -> list:
    proteins = []

    # read in text file
    with open(path, 'r') as f:
        lines = f.readlines()

    # take the first value from text file
    for line in lines:
        proteins.append(line.split('|')[0])

    # return list
    return proteins

def main():
    proteins = extract_proteins("data/protein_aliases.txt")
    res_path = "results/functions.txt"

    t1 = threading.Thread(target=extract_functions, args=(proteins[:5000], res_path, ))
    t2 = threading.Thread(target=extract_functions, args=(proteins[5000:10000], res_path, ))
    t3 = threading.Thread(target=extract_functions, args=(proteins[10000:15000], res_path, ))
    t4 = threading.Thread(target=extract_functions, args=(proteins[15000:20000], res_path, ))
    t5 = threading.Thread(target=extract_functions, args=(proteins[20000:25000], res_path, ))
    t6 = threading.Thread(target=extract_functions, args=(proteins[25000:], res_path, ))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

main()

























# extract_functions(["O89090", "Q9ULI3", "P98064"])


# r = requests.get("https://rest.uniprot.org/uniprotkb/O89090.json")
# request = r.json()
# keys = request.keys()
# # for key in keys:
# #     print(f"{key}")
# #     print(request[key])
# #     print()
# #     print()

# for i, value in enumerate(request["comments"]):
#     if request["comments"][i]['commentType'] == 'FUNCTION':
#         print(i)
#         print(request["comments"][i])
#         for j in range(len(request["comments"][i]['commentType'])):
#             print(request["comments"][i]["texts"][j])




    
