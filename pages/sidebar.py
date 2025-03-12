import streamlit as st
import base64

# Define a function to load the sidebar
def load_sidebar():
    st.sidebar.title("Notesense Project")
    st.sidebar.page_link(page="home.py", label="Keyword Search")
    # st.sidebar.page_link(page="pages/keywords-de.py", label="Keyword Search German")
    # st.sidebar.page_link(page="pages/keywords-en.py", label="Keyword Search English")
    # st.sidebar.page_link(page="pages/topics_en.py", label="Topics Network English")
    # st.sidebar.page_link(page="pages/topics_de.py", label="Topics Network German")
    st.sidebar.page_link(page="pages/topic_info_de.py", label="Topics Info German")
    st.sidebar.page_link(page="pages/about-data.py", label="About Data")
    st.sidebar.page_link(page="pages/about-us.py", label="About Us")

    # ---- Footer Message ----
    st.sidebar.markdown("---")
    st.sidebar.markdown('By [Notesense](https://github.com/Notesense) team.', unsafe_allow_html=True)

    # ---- Add the logo at the bottom of the sidebar ----
    logo_path = "NotesenseLogo.png"  # Adjust the path if needed

    # Function to encode the image to base64
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    logo_base64 = get_base64_image(logo_path)


    st.sidebar.markdown(
        f"""
        <style>
            /* Ensure sidebar content fills space and aligns the logo at the bottom */
            .sidebar-content {{
                display: flex;
                flex-direction: column;
                height: 100vh;
                justify-content: space-between;
            }}

            /* Center the logo */
            .sidebar-footer {{
                text-align: center;
                padding-bottom: 10px;
            }}
        </style>
        
        <div class="sidebar-content">
            <div class="sidebar-footer">
                <img src="data:image/png;base64,{logo_base64}" width="50">
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
