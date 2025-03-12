import pandas as pd
import streamlit as st
import plotly.express as px
import pymysql
import html
from pages.sidebar import load_sidebar


# ---- Streamlit Layout ----
st.set_page_config(page_title="Keyword Search", layout="wide")
st.title("Keyword Search in Community Notes")
load_sidebar()

def create_connection():
    try:
        return pymysql.connect(
            host=st.secrets["database"]["host"],
            port=st.secrets["database"]["port"],
            user=st.secrets["database"]["user"],
            password=st.secrets["database"]["password"],
            database=st.secrets["database"]["database"]
        )
    except pymysql.MySQLError as e:
        st.error(f"Error connecting to MySQL/MariaDB: {e}")
        return None


# ---- Sidebar for Language Selection ----
language = st.radio("Language", ["English", "German"],index=1, horizontal=True)
table_name = "df_X_Eng_preprocessed" if "English" in language else "df_X_German_preprocessed"

# ---- Database Connection ----
with st.spinner("Connecting to Database..."):
    conn = create_connection()

# ---- Combined Data Retrieval Query ----
@st.cache_data
def fetch_dates_and_keyword_range(_conn, keyword, table_name):
    query = f"""
        SELECT 
            MIN(date), MAX(date),
            MIN(CASE WHEN summary LIKE %s THEN date ELSE NULL END),
            MAX(CASE WHEN summary LIKE %s THEN date ELSE NULL END)
        FROM {table_name}
    """
    with _conn.cursor() as cursor:
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        global_min_date, global_max_date, keyword_min_date, keyword_max_date = cursor.fetchone()
    
    keyword_min_date = keyword_min_date or global_min_date
    keyword_max_date = keyword_max_date or global_max_date

    return pd.to_datetime(global_min_date).date(), pd.to_datetime(global_max_date).date(), \
           pd.to_datetime(keyword_min_date).date(), pd.to_datetime(keyword_max_date).date()

# ---- Keyword Search ----
keyword_searched = st.text_input(label='Type your keyword', value='twitter')
st.markdown("Note: Add spaces before/after the keyword for exact word matches.")

# ---- Fetch Data from Cache ----
global_min_date, global_max_date, keyword_min_date, keyword_max_date = fetch_dates_and_keyword_range(conn, keyword_searched, table_name)

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
def fetch_data_counts(_conn, keyword, start_date, end_date, table_name):
    query = f"""
        SELECT date, COUNT(*) 
        FROM {table_name} 
        WHERE summary LIKE %s AND date BETWEEN %s AND %s 
        GROUP BY date
    """
    with _conn.cursor() as cursor:
        cursor.execute(query, (f"%{keyword}%", start_date, end_date))
        return pd.DataFrame(cursor.fetchall(), columns=['Date', 'Number of Notes'])

# ---- Data Plotting ----
data_counts = fetch_data_counts(conn, keyword_searched, start_date, end_date, table_name)
if not data_counts.empty:
    fig = px.line(
        data_counts, 
        x='Date', 
        y='Number of Notes',
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
def fetch_display_data(_conn, keyword, start_date, end_date, table_name):
    query = f"""
        SELECT CAST(noteID AS CHAR), date, summary, tweetId 
        FROM {table_name} 
        WHERE summary LIKE %s AND date BETWEEN %s AND %s
        ORDER BY date
    """
    with _conn.cursor() as cursor:
        cursor.execute(query, (f"%{keyword}%", start_date, end_date))
        data = cursor.fetchall()
    
    headers = ['Note ID', 'Date', 'Note Content', 'Tweet ID']
    display_df = pd.DataFrame(data, columns=headers)
    
    # Decode HTML entities in the 'Note Content' column
    display_df['Note Content'] = display_df['Note Content'].apply(html.unescape)
    
    display_df['Tweet URL'] = 'https://twitter.com/notesense/status/' + display_df['Tweet ID'].astype(str)
    return display_df

# ---- Show Filtered Data Table ----
display_df = fetch_display_data(conn, keyword_searched, start_date, end_date, table_name)
st.subheader(f"Notes containing '{keyword_searched}' between {start_date} and {end_date} ({language})")
st.subheader(f"Total Notes Found: {len(display_df)}")
st.dataframe(display_df[['Note ID', 'Date', 'Note Content', 'Tweet ID', 'Tweet URL']], height=400, use_container_width=True)

# ---- Download Button ----
csv_data = display_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label=f"Download as CSV ({language})",
    data=csv_data,
    file_name=f"filtered_notes_{keyword_searched}_{language}.csv",
    mime="text/csv",
)
