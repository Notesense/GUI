import streamlit as st
from pages.sidebar import load_sidebar  # Import the sidebar function
import dash
import dash_cytoscape as cyto
import pandas as pd
from dash import html, dcc, Output, Input, dash_table
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pickle

from flask import Flask
import threading
import time



## Show in webpage
st.header("Topics Network")

load_sidebar()

# Define Cytoscape styles
stylesheet = [
    {
        "selector": "node",
        "style": {
            "label": "data(label)",
            "background-color": "data(background_color)",
            "width": "data(size)",
            "height": "data(size)",
            "text-valign": "center",
            "text-halign": "center",
            "font-size": "mapData(size, 15, 150, 10, 20)",  
            "font-family": "Arial, sans-serif",
            "color": "black",
        }
    },
    {
        "selector": "edge",
        "style": {
            "width": "data(weight)",
            "line-color": "#888",
            "curve-style": "bezier",
        }
    }
]
# Load the data
with open("data/graph_data_en.pkl", "rb") as f:
    elements, node_sizes, topic_to_notes, = pickle.load(f)
unique_topics = list(node_sizes.keys())  
color_map = plt.get_cmap("Set3")  # Discrete colormap for distinct colors
topic_colors = {topic: color_map(i / len(unique_topics)) for i, topic in enumerate(unique_topics)}
# Load extra layouts
cyto.load_extra_layouts()

# Build Dash App
app = dash.Dash(__name__)
app.layout = html.Div(style={"display": "flex", "height": "90vh", "font-family": "Arial, sans-serif"}, children=[
    html.Div([
        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            layout={
                "name": "fcose", 
                "nodeSeparation": 200,  
                "nodeRepulsion": 10000,  
                "idealEdgeLength": 200,  
                "edgeElasticity": 0.05,  
                "numIter": 3000  
            },
            style={"width": "75vw", "height": "100%", "background-color": "white", "position": "relative"},
            stylesheet=stylesheet
        )
    ], style={"flex": "3", "position": "relative"}),

    # ** Sidebar **
    html.Div([
        html.H3("Click on a Topic", style={"font-family": "Arial, sans-serif"}),
        html.Div(id="topic-details", style={"margin-bottom": "10px"}),  # Topic Name
        html.Div(id="topic-words", style={"margin-bottom": "10px", "font-style": "italic"}),  # Topic Words
        dash_table.DataTable(
            id="topic-table", 
            columns=[{"name": "Note ID", "id": "noteId"}], 
            page_size=10,
            style_table={"font-family": "Arial, sans-serif"}
        ),
        html.Button("Download Notes", id="download-button", n_clicks=0, style={"margin-top": "10px"}),
        dcc.Download(id="download-component")
    ], style={"flex": "1", "padding": "10px", "background": "#f9f9f9", "overflow": "auto"})


])

# Callback to display full topic name and notes

@app.callback(
    [Output("topic-details", "children"), 
     Output("topic-words", "children"),
     Output("topic-table", "data")],
    [Input("cytoscape", "tapNode")]
)
def display_topic_details(node_data):
    if node_data is None:
        return "Click a topic node to see details.", "", []

    try:
        topic_id = int(float(node_data["data"]["id"]))  # Convert safely from float-string to int
    except ValueError:
        return "Invalid topic selection.", "", []

    # Get topic name
    full_label = node_data["data"].get("full_label", str(topic_id))
    
    # Get associated note IDs
    notes = topic_to_notes.get(topic_id, [])

    # Get topic words from the dataframe
    topic_words_row = topic_representation_words[topic_representation_words["Topic"] == topic_id]

    if not topic_words_row.empty:
        raw_words = topic_words_row.iloc[0]["Representation"]
        try:
            # Convert stringified list to a real list
            word_list = ast.literal_eval(raw_words)
            cleaned_words = ", ".join(word_list[:10])  # Show first 10 words nicely
        except (ValueError, SyntaxError):
            cleaned_words = "Error parsing topic words."
    else:
        cleaned_words = "No representative words found."

    return f"Topic: {full_label}", f"Top Words: {cleaned_words}", [{"noteId": note} for note in notes]


# ---------------------- #
# Function to Run Dash
# ---------------------- #
def run_dash():
    app.run_server(port=8050, debug=False, use_reloader=False)

# Start Dash in a background thread
if "dash_thread" not in st.session_state:
    st.session_state.dash_thread = threading.Thread(target=run_dash, daemon=True)
    st.session_state.dash_thread.start()
    time.sleep(2)  # Give Dash some time to start

# Display the Dash app using an iframe
st.components.v1.iframe("http://127.0.0.1:8050/dash/", height=700, scrolling=True)