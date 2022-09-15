import streamlit as st
import leafmap.foliumap as leafmap
import requests   
from typing import DefaultDict
import pandas as pd
import geopandas

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

url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-2D9A3820-D547-4A45-AEF9-1636F2744FF4'
data = requests.get(url)  
data_json = data.json()    
location = data_json['records']['location']
dic_data = DefaultDict(list)
for i in location:
    dic_data['lat'] += [i['lat']] 
    dic_data['lon'] += [i['lon']]      
    dic_data['PRES'] += [i['weatherElement'][5]['elementValue']]
    dic_data['City'] += [i['parameter'][0]['parameterValue']]   

data = pd.DataFrame(dic_data)
citys = data['City'].to_list()
citys = list(set(citys))

col1, col2 = st.columns([4, 1])

with col2:

    select_city = st.selectbox("Select a City:", citys)


with col1:

    m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
    raindata = data[data['City'] == select_city]
    m.add_basemap("OpenStreetMap")
    m.to_streamlit(height=700)
