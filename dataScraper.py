import json
import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
names = []

for item in json_data['features']:
    # Get the name of the shark
    name = item['properties']['name']
    # Check if 'White Shark' is in the name of the species
    if item['properties']['species'] is not None and 'White Shark' in item['properties']['species']:
        count += 1

        # append the id to the list
        ids.append(item['properties']['id'])
        names.append(item['properties']['name'])

print(f'Number of Sharks: {count}')

lats = []
longs = []
times = []
df_names = []
df_ids = []

count = 0

# Get the data for every Shark
for i in range(len(ids)):
    req = urllib.request.Request(req_string.format(ids[i]),
    data=None, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })

    response = urllib.request.urlopen(req)
    count += 1

    json_data = json.loads(response.read())

    point_objs = json_data['motion']

    for obj in point_objs:
        coord = obj['point']['coordinates']
        times.append(obj['dt_move'])
        lats.append(coord[1])
        longs.append(coord[0])
        df_ids.append(ids[i])
        df_names.append(names[i])

    print(f'Sharks Retrieved: {count}\r', end='')

print(f'Sharks Retrieved: {count}')
    
df = pd.DataFrame()

df['lat'] = lats
df['long'] = longs
df['time'] = times
df['time'] = pd.to_datetime(df['time'])
df['id'] = df_ids
df['name'] = df_names

df['month'] = df['time'].dt.month

americas = df.loc[df['lat'] > 0]

africa = df.loc[df['lat'] < 0]

plt.scatter(americas['long'], americas['lat'], c=americas['month'], cmap='twilight_shifted', alpha=0.2, s=5)
plt.gcf().set_size_inches(20, 20)
plt.title('Sharks in the Americas')
plt.savefig('americas.pdf')

print("Americas Graph Created")

# clear the graph
plt.clf()

plt.scatter(africa['long'], africa['lat'], c=africa['month'], cmap='twilight_shifted', alpha=0.2, s=5)
plt.gcf().set_size_inches(20, 20)
plt.title('Sharks in Africa')
plt.savefig('africa.pdf')

print("Africa Graph Created")

americas.to_csv('americas.csv', index=False)
africa.to_csv('africa.csv', index=False)

print("Output pings to americas.csv and africa.csv")

print(f'Shark pings in the Americas: {americas.shape[0]}')
print(f'Sharks pings in Africa: {africa.shape[0]}')