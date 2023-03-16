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

# convert price from string to float
price_list = []
for price in airbnbs.price:
    price_number = price.partition('$')[-1]
    if ',' in price_number:
        price_number = price_number.partition(',')[0] + price_number.partition(',')[2]
    price_float = float(price_number)
    price_list.append(price_float)
airbnbs['price'] = price_list

airbnbs['price_per_person'] = airbnbs.price/airbnbs.bedrooms

# remove nans and unrealistic values (I'm assuming >$3,000/night for an AirBnb is not a real value, but I may be underestimating the ultra-rich)
airbnbs = airbnbs.dropna(subset=['price_per_person'])
airbnbs = airbnbs.drop(airbnbs[airbnbs.price_per_person>3000].index)
airbnbs = airbnbs.drop(airbnbs[airbnbs.price_per_person<10].index)

#%% show all locations in Tasmania on map
#lat = pd.DataFrame(airbnbs, columns=['latitude'])
lat = airbnbs.latitude
lon = airbnbs.longitude
price = airbnbs.price_per_person
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
all_tasmania.drawmapboundary(color='k', linewidth=1, zorder=1)
all_tasmania.fillcontinents(color='#dae7e0', zorder=2)
all_tasmania.drawcoastlines(color='#77a68d', zorder=3)
all_tasmania.scatter(mercator_x, mercator_y, marker='o', c='#c86341', edgecolors="#9e4a2e", zorder=3)

# save as .png
plt.savefig('all_tasmania.png')

#%% show all locations in Hobart on interactive map, colour by price

# make map centred on Hobart, specify zoom level
fig = folium.Figure(width=500, height = 500)
hobart = folium.Map([-42.86, 147.33], 
                    zoom_start=10, 
                    control_scale=True,
                    tiles='CartoDb dark_matter').add_to(fig) 
#options for tilesets include 'CartoDb positron', 'CartoDb dark_matter', 'Stamen Toner', 'Stamen Watercolor', 'OpenStreetMap'

# set colour range
cheapest = (1.0, 1.0, 0.0) # yellow
expensivest = (1.0, 0.0, 0.0) # red

for index in airbnbs.index:
    if price[index]<500:                       # max out the colour scale and radius at $500, to avoid skewing with high values
        n = (1-(price[index]-min(price))/(500-min(price))) # get n for color and radius based on where price sits in the range
        radius = (1-n)*150
    else: 
        n = 0.
        radius = 150
    circle_color=colors.to_hex((1.0, n, 0.0, 0.7), keep_alpha=True)
    folium.Circle(location=[lat[index], lon[index]],
                  color=circle_color,
                  radius = radius,
                  fill= True,
                  fill_color = circle_color,
                  fill_opacity = 1,
                  tooltip=('$' + str(round(price[index])) + ' per person')).add_to(hobart)

hobart

#save as html
hobart.save("hobart_airbnbs.html")





