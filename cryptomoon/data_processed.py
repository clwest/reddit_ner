import spacy
import pandas as pd
import flair 
from collections import  Counter

nlp = spacy.load('en_core_web_sm')

data = pd.read_csv('./data/cryptomoonshots.csv', sep='|')

def get_orgs(text):
    try:

        doc = nlp(text)
        org_list = []

        for ent in doc.ents:
            if ent.label_ == 'ORG':
                org_list.append(ent.text)
        org_list = list(set(org_list))
        return org_list
    except TypeError:
        raise TypeError("bad text: {text}")
data['organizations'] = data['selftext'].apply(get_orgs)


orgs = data['organizations'].to_list()
orgs_flat = [org for sublist in orgs for org in sublist]
orgs_flat[:5]
org_freq = Counter(orgs_flat)
org_freq.most_common(10)

