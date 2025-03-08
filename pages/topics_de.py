import streamlit as st
from pages.sidebar import load_sidebar  # Import the sidebar function



## Show in webpage
st.header("Topics Network")

load_sidebar()
# Display the Dash app using an iframe
st.components.v1.iframe("", height=700, scrolling=True)




