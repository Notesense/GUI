from supabase import create_client, Client
import pandas as pd
import streamlit as st
import plotly.express as px
import html
from pages.sidebar import load_sidebar


# ---- Streamlit Layout ----
st.set_page_config(page_title="Keyword Search", layout="wide")
st.title("Keyword Search in Community Notes")
load_sidebar()

# Supabase Credentials
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

# Initialize Supabase client
supabase: Client = create_client(url, key)

# ---- Sidebar for Language Selection ----
language = st.radio("Language", ["English", "German"], index=1, horizontal=True)
table_name = "Eng-lean" if "English" in language else "German-lean"

# ---- Combined Data Retrieval Query ----
@st.cache_data
def fetch_dates_and_keyword_range(keyword, table_name):
    response = supabase.table(table_name) \
        .select("date, summary") \
        #.filter("summary", "ilike", f"%{keyword}%") \
        .filter("summary", "ilike", f"{keyword}") \ # no wildcards for efficiency
        .execute()

    df = pd.DataFrame(response.data)
    
    if df.empty:
        return None, None, None, None

    global_min_date = df['date'].min()
    global_max_date = df['date'].max()

    keyword_min_date = df[df['summary'].str.contains(keyword, case=False)]['date'].min()
    keyword_max_date = df[df['summary'].str.contains(keyword, case=False)]['date'].max()

    return pd.to_datetime(global_min_date).date(), pd.to_datetime(global_max_date).date(), \
           pd.to_datetime(keyword_min_date).date(), pd.to_datetime(keyword_max_date).date()

# ---- Keyword Search ----
keyword_searched = st.text_input(label='Type your keyword', value='twitter')
st.markdown("Note: Add spaces before/after the keyword for exact word matches.")

# ---- Fetch Data from Cache ----
global_min_date, global_max_date, keyword_min_date, keyword_max_date = fetch_dates_and_keyword_range(keyword_searched, table_name)

# ---- Date Range Selection ----
st.subheader("Select Date Range")
start_date, end_date = st.slider(
    "Date Range",
    min_value=global_min_date,
    max_value=global_max_date,
    value=(keyword_min_date, keyword_max_date),
    format="YYYY-MM-DD"
)

# ---- Optimized Data Fetching ----
@st.cache_data
def fetch_data_counts(keyword, start_date, end_date, table_name):
    response = supabase.table(table_name) \
        .select("date") \
        .filter("summary", "ilike", f"%{keyword}%") \
        .filter("date", "gte", start_date) \
        .filter("date", "lte", end_date) \
        .execute()

    df = pd.DataFrame(response.data)
    return df.groupby('date').size().reset_index(name='count')

# ---- Data Plotting ----
data_counts = fetch_data_counts(keyword_searched, start_date, end_date, table_name)
if not data_counts.empty:
    fig = px.line(
        data_counts, 
        x='date', 
        y='count',
        title=f"Notes per Date for keyword: '{keyword_searched}' ({language})",
        markers=True, 
        height=450, 
        width=1000
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f"No data found for the selected keyword and date range in {language}.")

# ---- Optimized Display Data Fetching ----
@st.cache_data
def fetch_display_data(keyword, start_date, end_date, table_name):
    
    BATCH_SIZE = 100000
    all_data = []
    offset = 0
    while True:
        response = supabase.table(table_name) \
            .select("noteId, date, summary, tweetId") \
            .ilike("summary", f"%{keyword}%") \
            .gte("date", start_date) \
            .lte("date", end_date) \
            .order("date", desc=False) \
            .range(offset, offset + BATCH_SIZE - 1) \
            .execute()
 
        batch = response.data
        if not batch:
            break

        all_data.extend(batch)
        offset += BATCH_SIZE

        if len(batch) < BATCH_SIZE:
            break

    if all_data:
        df = pd.DataFrame(all_data)
        df['summary'] = df['summary'].apply(html.unescape)
        df['Tweet URL'] = 'https://x.com/notesense/status/' + df['tweetId'].astype(str)
        return df
    else:
        return pd.DataFrame()

# ---- Show Filtered Data Table ----
with st.spinner("Loading notes..."):
    display_df = fetch_display_data(keyword_searched, start_date, end_date, table_name)

st.subheader(f"Notes containing '{keyword_searched}' between {start_date} and {end_date} ({language})")
st.subheader(f"Total Notes Found: {len(display_df)}")
st.dataframe(display_df[['noteId', 'date', 'summary', 'tweetId', 'Tweet URL']], height=400, use_container_width=True)

# ---- Download Button ----
csv_data = display_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label=f"Download as CSV ({language})",
    data=csv_data,
    file_name=f"filtered_notes_{keyword_searched}_{language}.csv",
    mime="text/csv",
)


