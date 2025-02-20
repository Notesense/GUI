import pandas as pd
import streamlit as st
import plotly.express as px

# Sidebar setup
#st.sidebar.title("Navigation")
st.sidebar.page_link(page="home.py", label="Keyword Search", icon="🔍")
st.sidebar.page_link(page="pages/about-data.py", label="About Data", icon="ℹ️")
#st.sidebar.page_link(page="pages/topics.py", label="Topic Search", icon="📊")

# Main title of the app
st.title("Keyword Search in German Notes")

# Load and preprocess data
df_prep_notes_de = pd.read_csv("data/df_X_German_preprocessed.csv")

# Sidebar input for keyword search
#keyword_searched = st.sidebar.text_input(label='Type your keyword', value='')
keyword_searched = st.text_input(label='Type your keyword', value='twitter')
plot = st.empty()
#download_button=st.download_button("Download the filtered data",data="data/df_X_German_preprocessed.csv",file_name="unfiltered_data.csv",)




#keyword_searched.visibility = "hidden"

# When a keyword is entered, filter and display data
if keyword_searched != '':
    # Filter the dataframe for the entered keyword
    filtered_df = df_prep_notes_de[df_prep_notes_de['cleaned_summary'].str.contains(keyword_searched, case=False, na=False)]
    
    # Convert 'date' to datetime and group by date to get counts
    filtered_df['date'] = pd.to_datetime(filtered_df['date'])
    date_counts = filtered_df.groupby('date').size()

    # Plotly line chart for date counts
    fig = px.line(date_counts, 
                  title=f'Notes per Date for keyword: "{keyword_searched}"', 
                  markers=True, height=400)
    
    # Customizing the plot
    fig.update_xaxes(title_text='Date', showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(title_text='Number of Notes', showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_layout(showlegend=False, 
                      plot_bgcolor='white', 
                      title_x=0.5,  # Center the title
                      title_font=dict(size=16, color='black'),
                      xaxis_title_font=dict(size=12, color='black'),
                      yaxis_title_font=dict(size=12, color='black'))

    # Show interactive Plotly chart
    #st.plotly_chart(fig)
    plot.plotly_chart(fig)
else:
    st.write("Please enter a keyword in the textbar to search for it in the German notes. You have access to the preprocessed dataset at the moment where URLs are excluded.")

# if download_button:
#     print("download here")

