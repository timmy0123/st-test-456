import streamlit as st
from collections import defaultdict
import branca.colormap
import leafmap.foliumap as leafmap
from folium.plugins import HeatMap
import requests   
from typing import DefaultDict
import pandas as pd
import geopandas
import numpy as np

st.set_page_config(layout="wide")

markdown = """
Web App URL: <https://template.streamlitapp.com>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("降雨資料")

url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization=CWB-2D9A3820-D547-4A45-AEF9-1636F2744FF4'
data = requests.get(url)  
data_json = data.json()    
location = data_json['records']['location']
dic_data = DefaultDict(list)
for i in location:
    dic_data['lat'] += [i['lat']] 
    dic_data['lon'] += [i['lon']]      
    dic_data['One_day_Rain'] += [i['weatherElement'][-3]['elementValue']]
    dic_data['City'] += [i['parameter'][0]['parameterValue']]   

data = pd.DataFrame(dic_data)
citys = data['City'].to_list()
citys = list(set(citys))

col1, col2 = st.columns([4, 1])

with col2:

    select_city = st.selectbox("Select a City:", citys)


with col1:
    raindata = data[data['City'] == select_city]
    geodata = geopandas.GeoDataFrame(raindata, crs='epsg:4326', geometry=geopandas.points_from_xy(raindata.lon, raindata.lat))
    heat_data = raindata[['lat','lon','One_day_Rain']].values
    heat_data = heat_data.astype(float)
    heat_data = np.array(heat_data)
    maxrain = 300
    heat_data[:,2] = heat_data[:,2] / maxrain
    lat = np.mean(heat_data[:,0])
    lon = np.mean(heat_data[:,1])
    heat_data[np.where(heat_data[:,2] > 1)[0],2] = 1
    steps=20
    colormap = branca.colormap.linear.YlOrRd_09.scale(0, 1).to_step(steps)
    gradient_map=defaultdict(dict)
    for i in range(steps):
        gradient_map[1/steps*i] = colormap.rgb_hex_str(1/steps*i)
    
    m = leafmap.Map(center=(lat, lon),zoom=9,locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
    HeatMap(heat_data.tolist(),name='降雨',gradient = gradient_map,radius=15).add_to(m)
    colormap.add_to(m)
    m.add_basemap("OpenStreetMap")
    m.to_streamlit(height=700)
