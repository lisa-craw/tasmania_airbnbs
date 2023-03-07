
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cmocean

## import data 
data_file = './listings.csv'
airbnbs = pd.read_csv(data_file)
# remove some errors (I'm assuming >$5,000/night for an AirBnb is not a real value, but I may be underestimating the ultra-rich)
airbnbs = airbnbs.drop(airbnbs[airbnbs.price>5000].index)

## show all locations in Tasmania on map, colour by price
lat = pd.DataFrame(airbnbs, columns=['latitude'])
lon = pd.DataFrame(airbnbs, columns=['longitude'])
price = pd.DataFrame(airbnbs, columns=['price'])

simple_map = plt.figure(figsize = (10,10))
basemap = Basemap(projection='cyl',
                 llcrnrlat=lat.min(axis=0)-0.2,
                 llcrnrlon=lon.min(axis=0)-0.2,
                 urcrnrlat=lat.max(axis=0)+0.2,
                 urcrnrlon=lon.max(axis=0)+0.2,
                 resolution='i'
                 )
basemap.drawcoastlines(color='#77a68d')
#basemap.fillcontinents(color='#dae7e0')

basemap.scatter(np.array(lon.longitude), np.array(lat.latitude), marker='o', c='#c86341')

## histogram of price data


