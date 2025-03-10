import streamlit as st
from pages.sidebar import load_sidebar  # Import the sidebar function



## Show in webpage
#st.header("Topics Network")

# Display the Dash app using an iframe
st.components.v1.iframe("", height=850, scrolling=True)

load_sidebar()




