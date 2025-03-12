import streamlit as st
import pandas as pd
from pages.sidebar import load_sidebar  # Import the sidebar function


st.title("Topics Visualization")
# Load and display the saved HTML file
st.markdown("The following 16 topics are found using the [BERTopic](https://maartengr.github.io/BERTopic/index.html) model with min_topic_size set to the rounded 1 percent of the total number of valid notes after preprocessing (45934 total notes --> 459 minimum size of topic) in German language. You can download the note ids together with their topics as a .csv file if you click on the download button below.")
load_sidebar()
csv_data = pd.read_csv("data/noteId_Topic_Keywords_de.csv")

# # Display the CSV table
# st.write("### CSV Data Preview")
# st.dataframe(csv_data)

# Create a CSV download link
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv_bytes = convert_df(csv_data)

st.download_button(
    label="Download Note IDs and Topics as a CSV",
    data=csv_bytes,
    file_name="topics_data.csv",
    mime="text/csv",
)

# Load the HTML content
with open("data/barchart_de.html", "r") as f:
    html_content = f.read()

# Wrap the HTML content with a responsive `<div>`
html_wrapper = f"""
<div style="width:100%; max-width:100%; height:auto; overflow:hidden; box-sizing:border-box;">
    <div style="transform: scale(0.7); transform-origin: top left; width: 125%; height: 100%;">
        {html_content}
    </div>
</div>
"""


load_sidebar()
st.components.v1.html(html_wrapper, height=900, scrolling=False)

st.markdown("""
---
<p style='font-size:11px'>
<b> Topic Word Scores in BERTopic: </b><br>
The topic word scores in BERTopic refer to the <b>c-TF-IDF scores</b> (<a href='https://maartengr.github.io/BERTopic/api/ctfidf.html' target='_blank'>Class-based Term Frequency-Inverse Document Frequency scores</a>).
A <b>higher score</b> means the word is <b>more important</b> or <b>more representative</b> for that topic.

</p>

---
""", unsafe_allow_html=True)