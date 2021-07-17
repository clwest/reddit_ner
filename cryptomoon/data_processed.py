import spacy
import pandas as pd
import flair 
from collections import  Counter

nlp = spacy.load('en_core_web_sm')
data = pd.read_csv('./data/cryptomoonshots.csv', sep='|')
model = flair.models.TextClassifier.load('en-sentiment')

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




def get_sentiment(text):
    sentence = flair.data.Sentence(text)
    model.predict(sentence)
    sentiment = sentence.labels[0]
    return sentiment

data['sentiment'] = data['selftext'].apply(get_sentiment)


sentiment = {}

for  i, row in data.iterrows():
    direction = row['sentiment'].value
    score = row['sentiment'].score
    for org in row['organizations']:
        if org not in sentiment.keys():
            sentiment[org] = {'POSITIVE': [], 'NEGATIVE': []}
        sentiment[org][direction].append(score)


avg_sentiment = []

for org in sentiment.keys():
    freq_pos = len(sentiment[org]['POSITIVE'])
    freq_neg = len(sentiment[org]['NEGATIVE'])
    for direction in ['POSITIVE', 'NEGATIVE']:
        score = sentiment[org][direction]
        if len(score) == 0:
            sentiment[org][direction] = 0.0
        else:
            sentiment[org][direction] = sum(score)/len(score)
    avg = sentiment[org]['POSITIVE'] - sentiment[org]['NEGATIVE']
    avg_sentiment.append({
        'enity': org,
        'positive': sentiment[org]['POSITIVE'],
        'negative': sentiment[org]['NEGATIVE'],
        'freq': freq_pos + freq_neg,
        'score': avg
    })

sentiment_df = pd.DataFrame(avg_sentiment)
sentiment_df = sentiment_df[sentiment_df['freq'] > 3]
sentiment_df.sort_values('score', ascending=False).head(10)
sentiment_df.head()
