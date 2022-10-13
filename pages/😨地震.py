import streamlit as st
import leafmap.foliumap as leafmap
from folium.plugins import HeatMap
import requests   
from typing import DefaultDict
import pandas as pd
import geopandas
import numpy as np
import statistics
import datetime

st.set_page_config(layout="wide")

markdown = """
Git: <https://github.com/timmy0123/st-test-456>\n
氣象資料: <https://opendata.cwb.gov.tw/dataset/observation/O-A0001-001>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)

st.title("本月有感地震資訊")
url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWB-2D9A3820-D547-4A45-AEF9-1636F2744FF4'
data = requests.get(url)  

data_json = data.json()    
location = data_json['records']['earthquake']  
dic_data = DefaultDict(list)
for i in location:
    dic_data['lat'] += [i['earthquakeInfo']['epiCenter']['epiCenterLat']['value']] 
    dic_data['lon'] += [i['earthquakeInfo']['epiCenter']['epiCenterLon']['value']]   
    dic_data['date'] += [i['earthquakeInfo']['originTime']]
    dic_data['Content'] += [i['reportContent']]    

data = pd.DataFrame(dic_data)

cc1,cc2 = st.columns(2)
with cc2:
    st.write(data,width='100%')

with cc1:
    contnet = """
        地震資料包含了地震發生的經緯度、發生日期、以及芮氏規模和最大震度。
        """
    st.markdown(contnet)

geodata = geopandas.GeoDataFrame(data[['lat','lon','date','Content']], crs='epsg:4326', geometry=geopandas.points_from_xy(data.lon, data.lat))
m = leafmap.Map(center=(23.5, 121.5),zoom=5,locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
m.add_gdf(geodata)
m.add_basemap("OpenStreetMap")
m.to_streamlit(height=700)
