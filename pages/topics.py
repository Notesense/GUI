import streamlit as st

#change the name of tabs in the sidebar
st.sidebar.page_link(page="home.py", label="Keyword Search", icon="🔍")
#st.sidebar.page_link(page="pages/topics.py", label="Topic Search", icon="📊")
st.sidebar.page_link(page="pages/about-data.py", label="About Data", icon="ℹ️")


path_to_html = "pages/nmf_topic_visualization.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Groups of Topics")
st.components.v1.html(html_data,height=2000)

