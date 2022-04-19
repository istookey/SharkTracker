from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('africa.csv')

min_lat = df['lat'].min()
min_lon = df['long'].min()

max_lon = df['long'].max()
max_lat = df['lat'].max()

m = Basemap(llcrnrlat=min_lat - 3, urcrnrlat=max_lat + 3,
    llcrnrlon=min_lon - 3, urcrnrlon=max_lon + 3, resolution='c')

m.drawcoastlines()

m.drawmapboundary(fill_color='lightgreen')
m.fillcontinents(color='forestgreen', lake_color='lightgreen')
m.drawcoastlines()
m.drawcountries()
m.drawstates()
# m.drawrivers(color='blue')

m.scatter(df['long'], df['lat'], c=df['month'], cmap='twilight_shifted', latlon=True, alpha=0.25, s=3)

plt.gcf().set_size_inches(20, 20)
plt.savefig('africa_mapped.pdf')
# plt.show()