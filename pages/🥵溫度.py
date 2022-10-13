import streamlit as st
from collections import defaultdict
import branca.colormap
import leafmap.foliumap as leafmap
from folium.plugins import HeatMap
from folium import Choropleth
import requests   
from typing import DefaultDict
import pandas as pd
import geopandas
import numpy as np

st.set_page_config(layout="wide")

markdown = """
Git: <https://github.com/timmy0123/st-test-456>\n
氣象資料: <https://opendata.cwb.gov.tw/dataset/observation/O-A0001-001>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)

st.title("溫度資料")

contnet = """
        溫度為氣象站最新測得的溫度，與降雨相同將其以熱點圖的形式繪製在地圖上，不同顏色代表不同的氣溫。
        """
st.markdown(contnet)

url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-2D9A3820-D547-4A45-AEF9-1636F2744FF4&elementName=TEMP'
data = requests.get(url)  
data_json = data.json()    
location = data_json['records']['location']
dic_data = DefaultDict(list)
for i in location:
    dic_data['lat'] += [i['lat']] 
    dic_data['lon'] += [i['lon']]      
    dic_data['Temp'] += [i['weatherElement'][0]['elementValue']]
    dic_data['City'] += [i['parameter'][0]['parameterValue']]   

data = pd.DataFrame(dic_data)
citys = data['City'].to_list()
citys = list(set(citys))

col1, col2 = st.columns([4, 1])

with col2:
    select_city = st.selectbox("Select a City:", citys)
    show = data[data['City'] == select_city]
    show = show.rename({'Temp': 'Temperature'}, axis=1)
    st.dataframe(show)



with col1:
    raindata = data[data['City'] == select_city]
    geodata = geopandas.GeoDataFrame(raindata, crs='epsg:4326', geometry=geopandas.points_from_xy(raindata.lon, raindata.lat))
    heat_data = raindata[['lat','lon','Temp']].values
    heat_data = heat_data.astype(float)
    heat_data = np.array(heat_data)
    lat = np.mean(heat_data[:,0])
    lon = np.mean(heat_data[:,1])
    heat_data[:,2] = heat_data[:,2] / 40
    steps=5
    colormap = branca.colormap.linear.YlOrRd_09.scale(0, 40).to_step(steps)
    gradient_map=defaultdict(dict)
    for i in range(steps):
        gradient_map[1/steps*i] = colormap.rgb_hex_str(40/steps*i)
    m = leafmap.Map(center=(lat, lon),zoom=10,locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
    HeatMap(heat_data.tolist(),name='溫度',gradient = gradient_map,blur=10,min_opacity=0.01,max_opacity=0.99,radius=25).add_to(m)
    colormap.add_to(m)
    m.add_basemap("OpenStreetMap")
    m.to_streamlit(height=700)
