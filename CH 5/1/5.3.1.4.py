import pandas as pd
import numpy as np
import folium
import json

# Read the data from the CSV file into a DataFrame
df = pd.read_csv('libyan_cities_data.csv')

# Read the JSON file into a dictionary
with open('libyan_cities_coordinates.json') as f:
    coordinates = json.load(f)

# Define a function to assign colors based on value ranges
def color_producer(val):
    if val < 20:
        return 'red'
    elif val < 40:
        return 'orange'
    elif val < 60:
        return 'yellow'
    else:
        return 'green'

# Create a map centered at a specific location
mymap = folium.Map(location=[25.0, 17.0], zoom_start=6)

# Add markers for each city
for index, row in df.iterrows():
    city = row['City']
    value = row['Value']
    if city in coordinates:
        lat = coordinates[city]['latitude']
        lon = coordinates[city]['longitude']
        color = color_producer(value)
        folium.CircleMarker(location=[lat, lon], radius=5, popup=f'{city}: {value}', color=color, fill=True).add_to(mymap)

# Display the map
mymap.save('intrnet_speed_map.html')
