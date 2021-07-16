import requests
import time
import pandas as pd

client_id = 'Bz40yQZ_bqx92Q'
secret_token = 'HtO5GNrspC_HaldP76SmBel0erv66Q'

with open('pass.txt', 'r') as fp:
    pwd = fp.read()

user = 'photo-dad2017'

auth = requests.auth.HTTPBasicAuth(client_id, secret_token)

data = {
    'grant_type': 'password',
    'username': user,
    'password': pwd
    }

headers = {'User-Agent': 'MyBot/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token', 
                    auth=auth,
                    data=data,
                    headers=headers)

token = res.json()['access_token']
headers['Authorization'] = f'bearer {token}'


res = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

res = requests.get('https://oauth.reddit.com/r/cryptomoonshots/hot',
                    headers=headers, params={'limit': 100, 'after': 't3_8eor4a'})
res.json()['data']['children']

# for post in res.json()['data']['children']:
#     print(post['data']['title'])

df = pd.DataFrame()
params = {'limit': 100}

for post in res.json()['data']['children']:
    df = df.append({
        'id': post['data']['name'],
        'created_at': int(post['data']['created_utc']), 
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'upvote_ratio': post['data']['upvote_ratio'],
        'ups': post['data']['ups'],
        'downs': post['data']['downs'],
        'score': post['data']['score']
    }, ignore_index=True)

while True:
    res = requests.get('https://oauth.reddit.com/r/cryptomoonshots/hot', 
                        headers=headers, params=params)
    if len(res.json()['data']['children']) == 0:
        break

    for post in res.json()['data']['children']:
        df = df.append({
        'id': post['data']['name'],
        'created_at': int(post['data']['created_utc']), 
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'upvote_ratio': post['data']['upvote_ratio'],
        'ups': post['data']['ups'],
        'downs': post['data']['downs'],
        'score': post['data']['score']
    }, ignore_index=True)

    oldest_id = df['id'].iloc[-1]
    params['after'] = oldest_id

df = df.replace({'|':''}, regex=True)
df.to_csv('./data/cryptomoonshots.csv', sep='|', index=False)

print(len(df))
