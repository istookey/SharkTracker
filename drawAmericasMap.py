from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('americas.csv')

mean_long = df['lat'].median()
mean_lat = df['long'].median()

print(mean_lat, mean_long)

m = Basemap(projection='lcc', lon_0=mean_long, lat_0=mean_lat,
    width=8E6, height=8E6, resolution='c')

m.drawcoastlines()

m.drawmapboundary(fill_color='lightgreen')
m.fillcontinents(color='forestgreen', lake_color='lightgreen')
m.drawcoastlines()
m.drawcountries()
m.drawstates()
# m.drawrivers(color='blue')

m.scatter(df['lat'], df['long'], c=df['month'], cmap='twilight_shifted', latlon=True, alpha=0.2, s=5)

plt.gcf().set_size_inches(20, 20)
plt.savefig('americas_mapped.pdf')
# plt.show()