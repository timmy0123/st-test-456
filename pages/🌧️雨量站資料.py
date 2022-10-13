import streamlit as st
import leafmap.foliumap as leafmap
from folium.plugins import HeatMap
import requests   
from typing import DefaultDict
import pandas as pd
import geopandas
import numpy as np
import statistics

st.set_page_config(layout="wide")

markdown = """
Git: <https://github.com/timmy0123/st-test-456>\n
氣象資料: <https://opendata.cwb.gov.tw/dataset/observation/O-A0001-001>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)

st.title("雨量站資訊")

url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization=CWB-2D9A3820-D547-4A45-AEF9-1636F2744FF4'
data = requests.get(url)  
data_json = data.json()    
location = data_json['records']['location']
dic_data = DefaultDict(list)
for i in location:
    dic_data['lat'] += [i['lat']] 
    dic_data['lon'] += [i['lon']]   
    dic_data['locationName'] += [i['locationName']]   
    dic_data['stationId'] += [i['stationId']]
    dic_data['obsTime'] += [i['time']['obsTime']]
    dic_data['ELEV'] += [i['weatherElement'][0]['elementValue']]
    dic_data['City'] += [i['parameter'][0]['parameterValue']]   

data = pd.DataFrame(dic_data)
citys = data['City'].to_list()
citys = list(set(citys))
cc1,cc2,cc3 = st.columns([2,2,1])
with cc1:
    contnet = """
        從最右邊來選擇縣市，來查看各縣市的雨量站資料，並可從下方地圖來了解其確切位置。\n
        雨量站資訊包含：經緯座標、地點、測站名稱、觀測時間、海拔、及所在縣市。
        """
    st.markdown(contnet)

with cc3:
    select_city = st.selectbox("Select a City:", citys)

with cc2:
    st.write(data[data['City'] == select_city],width='100%')


raindata = data[data['City'] == select_city]
lats = raindata['lat'].values
lats = lats.astype(float)
lons = raindata['lon'].values
lons = lons.astype(float)
geodata = geopandas.GeoDataFrame(raindata, crs='epsg:4326', geometry=geopandas.points_from_xy(raindata.lon, raindata.lat))
lat = statistics.mean(lats)
lon = statistics.mean(lons)
m = leafmap.Map(center=(lat, lon),zoom=9,locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
m.add_gdf(geodata)
m.add_basemap("OpenStreetMap")
m.to_streamlit(height=700)
