import requests
import json
import pandas as pd

# Load in PMIDs 
pmids = '34806902,33998164,34098726,31670476,29484645,29133944'
PMIDS = ['34806902','33998164','34098726','31670476','29484645','29133944']
url = f'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids={pmids}'#&concepts=gene,protein'
response = requests.get(url)
responses = response.text.split('\n')

# Using Dylan's code (this block), we can extract most of the keywords
def extract_annotations(annotation):
    entity_type = annotation['infons']['type']
    start_index = annotation['locations'][0]['offset']
    end_index = start_index+annotation['locations'][0]['length']
    
    return entity_type, [start_index, end_index]

pmid_to_entity_type_to_indices = dict()
pmid_to_indices_to_entity_type = dict()
abstracts = []
titles = []

for entry_txt in responses:
    if entry_txt == '':
        continue
    entry = json.loads(entry_txt)
    
    # PMID
    pmid = str(entry['id'])
    
    # Title
    title_section = entry['passages'][0]
    title = title_section['text']
    titles += [title]
    title_annotations = title_section['annotations']
    # print(title)
    # Abstract
    abstract_section = entry['passages'][1]
    abstract = abstract_section['text']
    abstract_annotations = abstract_section['annotations']
    abstracts += [abstract]

    # Title Annotations
    entity_type_to_title_indices = dict()
    title_indices_to_entity_type = dict()
    for annotation in title_annotations:    
        entity_type, indices = extract_annotations(annotation)
        entity_type_to_title_indices.setdefault(entity_type,list()).append(indices)
        title_indices_to_entity_type[tuple(indices)] = entity_type
        
    # Abstract Annotations
    entity_type_to_abstract_indices = dict() 
    abstract_indices_to_entity_type = dict()
    for annotation in abstract_annotations:
        entity_type, indices = extract_annotations(annotation)
        entity_type_to_abstract_indices.setdefault(entity_type, list()).append(indices)
        abstract_indices_to_entity_type[tuple(indices)] = entity_type

        print(annotation['text'], annotation['infons']['type'], pmid, sep=";")
    
    # PMID->Entities->Indices
    pmid_to_entity_type_to_indices[pmid] = dict()
    pmid_to_entity_type_to_indices[pmid]['title'] = entity_type_to_title_indices
    pmid_to_entity_type_to_indices[pmid]['abstract'] = entity_type_to_abstract_indices
    
    # PMID->Indices->Entity Type
    pmid_to_indices_to_entity_type[pmid] = dict()
    pmid_to_indices_to_entity_type[pmid]['title'] = title_indices_to_entity_type
    pmid_to_indices_to_entity_type[pmid]['abstract'] = abstract_indices_to_entity_type
    
    # PMID->Indices->Entity Type->Entity


title_dict = {}
title_df_spacy = pd.DataFrame()
title_ents = []
title_entity_labels = []
title_pmid = []

abstract_dict = {}
abstract_df_spacy = pd.DataFrame()
abstract_ents = []
abstract_ents_labels = []
abstract_pmid = []


NUMBER_OF_PMIDS = len(pmid_to_indices_to_entity_type)

for i in range(NUMBER_OF_PMIDS):
    temp_indices_to_entity_type = list(pmid_to_indices_to_entity_type.values())[i]
    # Save title
    title_keys = temp_indices_to_entity_type["title"]
    # Save abstract
    abstract_keys = temp_indices_to_entity_type["abstract"]

    # Save title keys using PubTator
    for key in title_keys:
        title_attrib_dict = {}
        start, end = key[0], key[1]
        entity = title_keys[key]
        entity_text = titles[i][start:end]
        title_attrib_dict["start"] = int(start)
        title_attrib_dict["end"] = int(end)
        title_attrib_dict["entity-type"] = entity
        title_attrib_dict["PMID"] = PMIDS[i]
        title_dict[entity_text] = title_attrib_dict

    # Title keys using spacy
    # text = titles[i]
    # text_doc = nlp(text)
    # title_ents += [*text_doc.ents]
    # for idx, ent in enumerate(text_doc.ents):
    #     title_entity_labels.append(ent.label_)
    #     title_pmid.append(PMIDS[i])
    

    # Save abstract keys
    for key in abstract_keys:
        abstract_attrib_dict = {}
        start, end = key[0], key[1]
        entity = abstract_keys[key]
        entity_text = abstracts[i][start:end]
        abstract_attrib_dict["start"] = int(start)
        abstract_attrib_dict["end"] = int(end)
        abstract_attrib_dict["entity-type"] = entity
        abstract_attrib_dict["PMID"] = PMIDS[i]
        abstract_dict[entity_text] = abstract_attrib_dict

    # Title keys using spacy
    # text = titles[i]
    # text_doc = nlp(text)
    # title_ents += [*text_doc.ents]
    # for idx, ent in enumerate(text_doc.ents):
    #     title_entity_labels.append(ent.label_)
    #     title_pmid.append(PMIDS[i])
    
    # examine abstracts
    # text = abstracts[i]
    # abstract_doc = nlp(text)
    # abstract_ents += [*abstract_doc.ents]
    # for idx, ent in enumerate(abstract_doc.ents):
    #     abstract_ents_labels.append(ent.label_)
    #     abstract_pmid.append(PMIDS[i])

abstract_df = pd.DataFrame(abstract_dict)
abstract_df = abstract_df.transpose()
abstract_df = abstract_df.reset_index()
abstract_df = abstract_df.rename(columns={"index": "entity"})
print(abstract_df)