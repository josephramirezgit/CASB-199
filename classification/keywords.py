import requests
import json
import csv
import threading
import time
import pandas as pd


main_keyword_list = {}
def extract_functions(protein_list: list) -> None:
    for protein in protein_list:
        # create words dict
        words = {}

        # extract request
        url = "https://rest.uniprot.org/uniprotkb/" + protein + ".json"
        r = requests.get(url)
        request = r.json()
        
        # input 1 if avaliable
        for i, val in enumerate(request["keywords"]):
            words[request["keywords"][i]["name"]] = 1
            
        # append dict to main dict
        main_keyword_list[protein] = words

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

def explore_json(protein: str) -> None:
    url = "https://rest.uniprot.org/uniprotkb/" + protein + ".json"
    r = requests.get(url)
    request = r.json()
    for key in request.keys():
        print(key)
        print(request[key])
        print()


def main():
    proteins = extract_proteins("data/protein_aliases.txt")
    res_path = "results/functions.txt"

    extract_functions(proteins[:10])

    # t1 = threading.Thread(target=extract_functions, args=(proteins[:10],))
    # t2 = threading.Thread(target=extract_functions, args=(proteins[10:20],))
    # t3 = threading.Thread(target=extract_functions, args=(proteins[20:30],))
    # t1.start()
    # t2.start()
    # t3.start()

    #  turn dict into csv 
    df = pd.DataFrame(main_keyword_list)
    df = df.transpose()
    print(main_keyword_list)

main()


# import requests
# import json
# import csv
# import threading
# import time
# import pandas as pd

# main_keyword_list = {}

# def extract_functions(protein_list: list) -> None:
#     for protein in protein_list:
#         # create words dict
#         words = {}

#         # extract request
#         url = "https://rest.uniprot.org/uniprotkb/" + protein + ".json"
#         r = requests.get(url)
#         request = r.json()

#         for i, val in enumerate(request["keywords"]):
#             words[request["keywords"][i]["name"]] = 1

#         main_keyword_list[protein] = words

# def extract_proteins(path: str) -> list:
#     proteins = []

#     # read in text file
#     with open(path, 'r') as f:
#         lines = f.readlines()

#     # take the first value from text file
#     for line in lines:
#         proteins.append(line.split('|')[0])

#     # return list
#     return proteins

# def explore_json(protein: str) -> None:
#     url = "https://rest.uniprot.org/uniprotkb/" + protein + ".json"
#     r = requests.get(url)
#     request = r.json()
#     for key in request.keys():
#         print(key)
#         print(request[key])
#         print()


# def main():
#     proteins = extract_proteins("data/protein_aliases.txt")
#     res_path = "results/functions.txt"

#     extract_functions(proteins[:10])

#     df = pd.DataFrame(main_keyword_list)
#     df = df.transpose()
#     # print(df.head())
#     print(df.count())

# main()

# """
# dict of dict
# d = {
# protA: {Cytoplasm: 1}
# }
# d = {

# }
# """

# def main():
#     proteins = extract_proteins("data/protein_aliases.txt")
#     res_path = "results/functions.txt"

#     t1 = threading.Thread(target=extract_functions, args=(proteins[:5000], res_path, ))
#     t2 = threading.Thread(target=extract_functions, args=(proteins[5000:10000], res_path, ))
#     t3 = threading.Thread(target=extract_functions, args=(proteins[10000:15000], res_path, ))
#     t4 = threading.Thread(target=extract_functions, args=(proteins[15000:20000], res_path, ))
#     t5 = threading.Thread(target=extract_functions, args=(proteins[20000:25000], res_path, ))
#     t6 = threading.Thread(target=extract_functions, args=(proteins[25000:], res_path, ))

#     t1.start()
#     t2.start()
#     t3.start()
#     t4.start()
#     t5.start()
#     t6.start()


























    
