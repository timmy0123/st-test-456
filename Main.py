import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Git: <https://github.com/timmy0123/st-test-456/tree/opendata-demo>\n
氣象資料: <https://opendata.cwb.gov.tw/dataset/observation/O-A0001-001>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)

# Customize page title
st.title("氣象資料展示")

st.markdown(
    """
    這是一隻用來展示開放資料的網頁
    """
)

st.header("介紹")

markdown = """
1. 這是用來展示氣象站資料的網頁
2. 氣象資料是透過api從氣象局網站取得 (氣象資料: https://opendata.cwb.gov.tw/dataset/observation/O-A0001-001)
3. 資料將會以熱點圖的形式展示於下方地圖上
"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)