import numpy as np
import pandas as pd
import matplotlib.colors as colors 
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cmocean
import folium

#%% import data 
data_file = './listings.csv'
airbnbs = pd.read_csv(data_file)
# remove some errors (I'm assuming >$5,000/night for an AirBnb is not a real value, but I may be underestimating the ultra-rich)
airbnbs = airbnbs.drop(airbnbs[airbnbs.price>5000].index)

#%% show all locations in Tasmania on map
#lat = pd.DataFrame(airbnbs, columns=['latitude'])
lat = airbnbs.latitude
lon = airbnbs.longitude
price = airbnbs.price
listings_count = airbnbs.calculated_host_listings_count
#lon = pd.DataFrame(airbnbs, columns=['longitude'])
#price = pd.DataFrame(airbnbs, columns=['price'])

plt.figure(figsize = (10,10))
all_tasmania = Basemap(projection='merc',
                 llcrnrlat=min(lat)-0.2,
                 llcrnrlon=min(lon)-0.2,
                 urcrnrlat=max(lat)+0.2,
                 urcrnrlon=max(lon)+0.2,
                 lat_ts = (max(lat)-min(lat))/2,
                 resolution='i'
                 )

mercator_x, mercator_y = all_tasmania(lon, lat)   # convert locations into mercator co-ordinates
#all_tasmania.drawmapboundary(color='k', linewidth=1, zorder=1)
all_tasmania.fillcontinents(color='#dae7e0', zorder=1)
parallels = np.arange(round(min(lat)), round(max(lat)+1), 1)
meridians = np.arange(round(min(lon)), round(max(lon)+1), 1)
all_tasmania.drawmeridians(meridians, labels=[False, True, True, False])
all_tasmania.drawparallels(parallels, labels=[True, False, False, True])
all_tasmania.drawcoastlines(color='#77a68d', zorder=2)
all_tasmania.scatter(mercator_x, mercator_y, marker='o', c='#c86341', edgecolors="#9e4a2e", zorder=3)
plt.savefig('all_tasmania.png')
#plt.show()


#%% show all locations in Hobart on interactive map, colour by price

# make map centred on Hobart, specify zoom level
fig = folium.Figure(width=500, height = 500)
hobart = folium.Map([-42.86, 147.33], 
#                    width=500,
#                    height=500,
                    zoom_start=10, 
                    control_scale=True,
                    tiles='CartoDb dark_matter').add_to(fig) 
#options for tilesets include 'CartoDb positron', 'CartoDb dark_matter', 'Stamen Toner', 'Stamen Watercolor', 'OpenStreetMap'

# set colour range
cheapest = (1.0, 1.0, 0.0) # yellow
expensivest = (1.0, 0.0, 0.0) # red


for index in airbnbs.index:
    if price[index]<1000:                       # max out the colour scale at $1000, to avoid skewing with high values
        n = 1-((price[index]-min(price))/(1000 - min(price)))   #get n for colour and alpha based on where the price sits in the range
    else: 
        n = 0
    folium.Circle(location=[lat[index], lon[index]],
                  radius=500*((price[index]-min(price))/(max(price)-min(price))), 
                  color=colors.to_hex((1.0, n, 0.0, (1-n)*0.8), keep_alpha=True),
                  fill= True,
                  fill_color = colors.to_hex((1.0, n, 0.0, (1-n)*0.8), keep_alpha=True), 
                  fill_opacity = 1,
                  tooltip=('$' + str(price[index]) + '/night')).add_to(hobart)

hobart

#save as html
hobart.save("hobart_airbnbs.html")




