import pandas as pd
import streamlit as st
import plotly.express as px
import html  
import base64

# Define the function to access logo
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# ---- Set up Streamlit Layout ----
st.set_page_config(page_title="Keyword Search", layout="wide")  # Optional: wide layout

# ---- Sidebar Setup ----
st.sidebar.title("Navigation")
st.sidebar.page_link(page="home.py", label="Keyword Search")
st.sidebar.page_link(page="pages/about-data.py", label="About Data")

# ---- Main Title ----
st.title("Keyword Search in German Notes")

# ---- Load CSV Data ----
# German preprocessed notes data: 
# https://drive.google.com/file/d/1tRkEstaVejJaeL_l6O0NU20jaQc9A2zW/view?usp=sharing

# English preprocessed notes data:
# https://drive.google.com/file/d/1ti9DKXx1bsR4LwoUOg3LHq2JehD0lZnN/view?usp=sharing

@st.cache_data
def load_data():
    file_id = "1tRkEstaVejJaeL_l6O0NU20jaQc9A2zW"  
    gdrive_url = f"https://drive.google.com/uc?id={file_id}"

    dtype_map = {
        "noteId": "string",
        "cleaned_summary": "string",
        "summary": "string",
        "date": "string",  # Will convert to datetime later
        "tweetId": "string"
    }

    return pd.read_csv(gdrive_url, low_memory=False, dtype=dtype_map)

with st.spinner("Loading data... Please wait ⏳"):
    df_prep_notes_de = load_data()
# st.success("Data successfully loaded! 🎉")


# Convert 'date' safely and drop NaT
df_prep_notes_de['date'] = pd.to_datetime(df_prep_notes_de['date'], errors='coerce')
df_prep_notes_de = df_prep_notes_de.dropna(subset=['date'])

# ---- Sidebar input for keyword search ----
keyword_searched = st.text_input(label='Type your keyword', value='twitter')

# ---- Filter Data Based on Keyword ----
filtered_df = df_prep_notes_de[
    df_prep_notes_de['cleaned_summary'].str.contains(keyword_searched, case=False, na=False)
].copy()

# ---- Determine Global Min & Max Date Across All Data ----
global_min_date = df_prep_notes_de['date'].min().date()  # Earliest date in full dataset
global_max_date = df_prep_notes_de['date'].max().date()  # Latest date in full dataset

# ---- Determine Min Date Based on the Selected Keyword ----
if not filtered_df.empty:
    keyword_min_date = filtered_df['date'].min().date()  # Earliest date when keyword appears
else:
    keyword_min_date = global_min_date  # If no data, default to global min

# ---- Bar: Keep Full Range but Highlight Keyword's Data Range ----
st.subheader("Select Date Range")

start_date, end_date = st.slider(
    "Date Range",
    min_value=global_min_date,  # Keep full dataset range visible
    max_value=global_max_date,  # Allow full dataset range selection
    value=(keyword_min_date, global_max_date),  # Highlight keyword's range
    format="YYYY-MM-DD"
)

# Convert selected dates back to `datetime` for filtering
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# ---- Apply Date Range Filter ----
filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

# ---- Group by Date for Plot ----
date_counts = filtered_df.groupby('date').size().reset_index(name="Number of Notes")

# ---- Show Interactive Plot (Centered & Responsive) ----
if not date_counts.empty:
    fig = px.line(
        date_counts, 
        x='date', 
        y='Number of Notes',
        title=f"Notes per Date for keyword: '{keyword_searched}'",
        markers=True, 
        height=450,  # Keep a balanced height
        width=1000,  # Make it longer horizontally
    )
    fig.update_layout(
        autosize=True,  # Allow automatic scaling
        height=450,  
        margin=dict(l=40, r=40, t=50, b=50),  # Balanced margins
        title_x=0.5,  # Center title
        plot_bgcolor='white'
    )
    fig.update_xaxes(title_text='Date', showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(title_text='Number of Notes', showgrid=True, gridwidth=1, gridcolor='lightgray')

    # ---- Centering with Responsive Layout ----
    col1, col2, col3 = st.columns([0.5, 8, 0.5])  # Wider middle column for a longer plot
    with col2:
        with st.container():
            st.plotly_chart(fig, use_container_width=True)  # Ensures responsiveness

else:
    st.warning("No data found for the selected keyword and date range.")

# ---- Rename Columns for Display & Fix Date Format ----
display_df = filtered_df.rename(columns={'date': 'Date', 'summary': 'Note Content', 'noteId': 'Note ID', 'tweetId': 'Tweet ID'}).copy()

# ---- Convert Large Note IDs to Strings to Avoid Precision Issues ----
if 'Note ID' in display_df.columns:
    display_df['Note ID'] = display_df['Note ID'].astype(str)

# ---- Clean HTML entities in "Note Content" column ----
display_df['Note Content'] = display_df['Note Content'].apply(html.unescape)

# ---- Convert "Date" column to string format YYYY-MM-DD
display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
 
 # ---- Convert "Tweet ID" column to string format
display_df['Tweet ID'] = display_df['Tweet ID'].astype(str)

# ---- Show Filtered Data Table (Below the Plot) ----
st.subheader(f"Notes containing '{keyword_searched}' between {start_date.date()} and {end_date.date()}")
st.markdown(
    "Note that the search is done on preprocessed text (which contains changes like lemmatization and removal of URLs while the printed rows below are the original Community Notes with minor HTML display corrections.)"
) 

# ---- Show Total Number of Notes ----
total_notes = len(display_df)
st.subheader(f"Total Notes Found: {total_notes}")

# ---- Display the Data Table Without the Index Column ----
st.dataframe(display_df[['Note ID', 'Date', 'Note Content','Tweet ID']], height=400, use_container_width=True)

# ---- Add Download Button for CSV ----
csv_data = display_df[['Note ID', 'Date', 'Note Content', 'Tweet ID']].to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download as CSV",
    data=csv_data,
    file_name=f"filtered_notes_{keyword_searched}.csv",
    mime="text/csv",
)

# ---- Footer Message ----
st.sidebar.markdown("---")
st.sidebar.markdown('By [Notesense](https://github.com/Notesense/CommunityNotes) team.', unsafe_allow_html=True)
# ---- Add the logo at the bottom of the sidebar ----
logo_path = "data/NotesenseLogo.png"  # Adjust the path if needed
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
