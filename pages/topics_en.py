import streamlit as st
from pages.sidebar import load_sidebar  # Import the sidebar function


# Display the Dash app using an iframe
st.components.v1.iframe("https://network-vis.onrender.com/", height=850, scrolling=True)

load_sidebar()




