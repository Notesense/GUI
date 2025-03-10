import streamlit as st
from pages.sidebar import load_sidebar  # Import the sidebar function
import uuid

# Unique session key to prevent conflicts
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

# Improved iframe display with dynamic height, width, and styling
st.markdown(
    """
    <style>
    .iframe-container {
        width: 100%;             /* Full width for responsiveness */
        height: 85vh;            /* Dynamic height relative to viewport */
        border: 2px solid #ddd;  /* Clean border */
        border-radius: 12px;     /* Rounded corners for aesthetics */
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); /* Soft shadow */
        background-color: white; /* Ensures clear display in dark mode */
        overflow: hidden;        /* Prevents inner scrollbars */
    }
    </style>
    <div class="iframe-container">
        <iframe src="https://network-vis.onrender.com/" 
                width="100%" 
                height="100%" 
                style="border:none;">
        </iframe>
    </div>
    """,
    unsafe_allow_html=True
)

# Optional: Add a "View Full Screen" link
st.markdown("[🔍 View Full Screen](https://network-vis.onrender.com/)", unsafe_allow_html=True)

# Load the sidebar
load_sidebar()
