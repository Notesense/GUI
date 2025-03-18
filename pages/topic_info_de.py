import streamlit as st
import pandas as pd
from pages.sidebar import load_sidebar  # Import the sidebar function


st.title("Topics Visualization")
# Load and display the saved HTML file
st.markdown("The following 16 topics are found using the [BERTopic](https://maartengr.github.io/BERTopic/index.html) model with min_topic_size set to the rounded 1 percent of the total number of valid notes after preprocessing (45934 total notes --> 459 minimum size of topic) in German language. You can download the note ids associated to each topic in the dropdown below. The data will be downloaded as a .csv file.")
load_sidebar()

csv_data = pd.read_csv("data/noteId_Topic_Keywords_de.csv")
# Filter out Topic -1
csv_data = csv_data[csv_data['Topic'] >= 0]

# Add a dropdown for topic selection
unique_topics = sorted(csv_data['Topic'].unique())
selected_topic = st.selectbox("Select a Topic to Download", unique_topics)

# Filter data by selected topic
filtered_data = csv_data[csv_data['Topic'] == selected_topic]

# Create CSV download link for filtered data
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

filtered_csv_bytes = convert_df(filtered_data)

st.download_button(
    label=f"Download Topic {selected_topic} Data as CSV",
    data=filtered_csv_bytes,
    file_name=f"topic_{selected_topic}_data.csv",
    mime="text/csv",
)



# # Display the CSV table
# st.write("### CSV Data Preview")
# st.dataframe(csv_data)
# st.download_button(
#     label="Download Note IDs and Topics as a CSV",
#     data=csv_bytes,
#     file_name="topics_data.csv",
#     mime="text/csv",
# )

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