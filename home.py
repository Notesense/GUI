import pandas as pd
import streamlit as st
import plotly.express as px

# Sidebar setup
st.sidebar.page_link(page="home.py", label="Keyword Search", icon="🔍")
st.sidebar.page_link(page="pages/about-data.py", label="About Data", icon="ℹ️")

# Main title of the app
st.title("Keyword Search in German Notes")

# Fix DtypeWarning: Read CSV safely and inspect types
df_prep_notes_de = pd.read_csv("data/df_X_German_preprocessed.csv", low_memory=False)

# Check problematic columns and convert to strings
cols_to_fix = ['col_5_name', 'col_6_name', 'col_7_name']  # Replace with actual column names
for col in cols_to_fix:
    if col in df_prep_notes_de.columns:
        df_prep_notes_de[col] = df_prep_notes_de[col].astype(str)

# Sidebar input for keyword search
keyword_searched = st.text_input(label='Type your keyword', value='twitter')

# Placeholder for plot
plot = st.empty()

# If a keyword is entered, filter and display data
if keyword_searched.strip():
    # Fix SettingWithCopyWarning: Use .copy()
    filtered_df = df_prep_notes_de[
        df_prep_notes_de['cleaned_summary'].str.contains(keyword_searched, case=False, na=False)
    ].copy()

    # Convert 'date' safely, handle errors
    filtered_df['date'] = pd.to_datetime(filtered_df['date'], errors='coerce')  

    # Drop NaT (invalid dates)
    filtered_df = filtered_df.dropna(subset=['date'])

    # Group by date and count occurrences
    date_counts = filtered_df.groupby('date').size().reset_index(name="Number of Notes")

    # Plotly line chart with proper labels
    fig = px.line(
        date_counts, 
        x='date', 
        y='Number of Notes',
        title=f"Notes per Date for keyword: '{keyword_searched}'",  # Fixed unterminated string issue
        markers=True, 
        height=400
    )

    # Update axes and layout
    fig.update_xaxes(title_text='Date', showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(title_text='Number of Notes', showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_layout(
        showlegend=False, 
        plot_bgcolor='white', 
        title_x=0.5,  
        title_font=dict(size=16, color='black'),
        xaxis_title_font=dict(size=12, color='black'),
        yaxis_title_font=dict(size=12, color='black')
    )

    # Display interactive Plotly chart
    plot.plotly_chart(fig)
else:
    st.write("Please enter a keyword in the textbar to search for it in the German notes. You have access to the preprocessed dataset at the moment where URLs are excluded.")
