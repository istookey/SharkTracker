import json
import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sklearn
import sys
from sklearn.linear_model import LogisticRegression as lr
from sklearn.tree import DecisionTreeClassifier as dt
from sklearn.model_selection import train_test_split as tts
from sklearn.model_selection import cross_val_score as cvs
from sklearn.preprocessing import MultiLabelBinarizer

req_string = "http://mapotic.com/api/v1/maps/3413/pois/{}/motion/with-meta/?format=json"

db_string = "http://mapotic.com/api/v1/maps/3413/pois.geojson/?format=json"

req = urllib.request.Request(db_string,
data=None, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    })

response = urllib.request.urlopen(req)

json_data = json.loads(response.read())

count = 0

ids = []

for item in json_data['features']:
    # Check if 'White Shark' is in the name of the species
    if item['properties']['species'] is not None and 'White Shark' in item['properties']['species']:
        count += 1

        # append the id to the list
        ids.append(item['properties']['id'])

print(f'Number of Sharks: {count}')

lats = []
longs = []
times = []

count = 0

# Get the data for every Shark
for id in ids:
    req = urllib.request.Request(req_string.format(id),
    data=None, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })

    response = urllib.request.urlopen(req)

    json_data = json.loads(response.read())

    point_objs = json_data['motion']

    for obj in point_objs:
        coord = obj['point']['coordinates']
        times.append(obj['dt_move'])
        lats.append(coord[0])
        longs.append(coord[1])

    if (count % 10 == 0):
        print(count)
    count += 1
    
print(count)

df = pd.DataFrame()

df['lat'] = lats
df['long'] = longs
df['time'] = times
df['time'] = pd.to_datetime(df['time'])

df['month'] = df['time'].dt.month
#df.head()

americas = df.loc[df['lat'] < 0]

africa = df.loc[df['lat'] > 0]

tree = dt(random_state=42)
lr_model = lr(random_state=42)

americas['coord'] = americas[['lat', 'long']].apply(tuple, axis=1)

print("Processing...")

coords = MultiLabelBinarizer().fit_transform(americas['coord'])

print("Training Tree...")

cvs(tree, np.array(americas['month']).reshape(-1,1), coords, cv=5, verbose=1, n_jobs=-1)

print("Training Logistic Regression...")

cvs(lr_model, np.array(americas['month']).reshape(-1,1), coords, cv=5, verbose=1, n_jobs=-1)