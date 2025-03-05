import pandas as pd
import streamlit as st
import plotly.express as px
import html  
import base64
import mariadb
import sys
from pages.sidebar import load_sidebar  # Import the sidebar function


def create_connection():
    try:
        host = "communitynotes.c3ui44m26pgw.eu-west-1.rds.amazonaws.com"
        port = 3306
        user = "communitynotes"
        password = "noted"
        database = "communitynotes"
        return mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None

# ---- Set up Streamlit Layout ----
st.set_page_config(page_title="Keyword Search", layout="wide")  # Optional: wide layout

# ---- Main Title ----
st.title("Keyword Search in German Notes")

load_sidebar()

with st.spinner("Connecting to Database..."):
    conn = create_connection()
    cursor = conn.cursor()


# Execute the query to get the oldest and newest dates
with st.spinner("Fetching Data..."):  
    cursor.execute("SELECT MIN(date), MAX(date) FROM df_X_German_preprocessed")
    global_min_date, global_max_date = cursor.fetchone()

# Convert to datetime and format as YYYY-MM-DD
global_min_date = pd.to_datetime(global_min_date).strftime('%Y-%m-%d')
global_max_date = pd.to_datetime(global_max_date).strftime('%Y-%m-%d')
# convert to datetime.date
global_min_date = pd.to_datetime(global_min_date).date()
global_max_date = pd.to_datetime(global_max_date).date()




# ---- Sidebar input for keyword search ----
keyword_searched = st.text_input(label='Type your keyword', value='birdwatch')



# query: find the minium and maximum date in the dataset where 'cleaned_summary' contains the keyword
query= f"SELECT MIN(date), MAX(date) FROM df_X_German_preprocessed WHERE cleaned_summary LIKE '%{keyword_searched}%'"
with st.spinner("Fetching Data..."):
    cursor.execute(query)
    keyword_min_date, keyword_max_date = cursor.fetchone()

# print(keyword_min_date,keyword_max_date)
if(keyword_min_date == None):
    keyword_min_date = global_min_date
else:
    keyword_min_date = pd.to_datetime(keyword_min_date).date()

if(keyword_max_date == None):
    keyword_max_date = global_max_date
else:
    keyword_max_date = pd.to_datetime(keyword_max_date).date()

# print(keyword_min_date,keyword_max_date)



# ---- Bar: Keep Full Range but Highlight Keyword's Data Range ----
st.subheader("Select Date Range")

start_date, end_date = st.slider(
    "Date Range",
    min_value=global_min_date,  # Keep full dataset range visible
    max_value=global_max_date,  # Allow full dataset range selection
    value=(keyword_min_date, keyword_max_date),  # Highlight keyword's range
    format="YYYY-MM-DD"
)



query = f"SELECT date, COUNT(*) FROM df_X_German_preprocessed WHERE cleaned_summary LIKE '%{keyword_searched}%' AND date >= '{start_date}' AND date <= '{end_date}' GROUP BY date"
with st.spinner("Fetching Data..."):
    cursor.execute(query)
    data_counts = pd.DataFrame(cursor.fetchall(), columns=['Date', 'Number of Notes'])

# ---- Show Interactive Plot (Centered & Responsive) ----
if not len(data_counts) == 0:
    fig = px.line(
        data_counts, 
        x='Date', 
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

query = f"SELECT CAST(noteID AS CHAR),date,summary,tweetId FROM df_X_German_preprocessed WHERE cleaned_summary LIKE '%{keyword_searched}%' AND date >= '{start_date}' AND date <= '{end_date}' ORDER BY date"
with st.spinner("Fetching Data..."):
    cursor.execute(query)
    display_df = cursor.fetchall()


# add headers
headers = ['Note ID', 'Date', 'Note Content', 'Tweet ID']
display_df = pd.DataFrame(display_df, columns=headers, index=None)


# ---- Show Filtered Data Table (Below the Plot) ----
st.subheader(f"Notes containing '{keyword_searched}' between {start_date} and {end_date}")
st.markdown(
    "Note that the search is done on preprocessed text (which contains changes like lemmatization and removal of URLs while the printed rows below are the original Community Notes with minor HTML display corrections.)"
) 

# ---- Show Total Number of Notes ----
total_notes = len(display_df)
st.subheader(f"Total Notes Found: {total_notes}")
# Reset index to remove the index column from display
display_df = display_df.reset_index(drop=True)

# add column Tweet URL that gets created from Tweet ID in the form of https://twitter.com/notesense/status/{tweet_id}
display_df['Tweet URL'] = 'https://twitter.com/notesense/status/' + display_df['Tweet ID'].astype(str)

# ---- Display the Data Table Without the Index Column ----
st.dataframe(display_df[['Note ID', 'Date', 'Note Content','Tweet ID','Tweet URL']], height=400, use_container_width=True)


# ---- Add Download Button for CSV ----


# Save to CSV
df = pd.DataFrame(display_df)
csv_data = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download as CSV",
    data=csv_data,
    file_name=f"filtered_notes_{keyword_searched}.csv",
    mime="text/csv",
)
