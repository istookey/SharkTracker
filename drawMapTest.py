from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

m = Basemap(projection='lcc', resolution='c', lat_0=0, lon_0=0, lat_1=20, lon_1=-60, width=8E6, height=8E6)

m.drawcoastlines()

m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral', lake_color='aqua')
m.drawrivers(color='blue')

plt.savefig('test.pdf')