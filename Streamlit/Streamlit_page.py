import streamlit as st
import pandas as pd
import plotly_express as px
import sqlite3
from Database_Preparation import q_ids, region_llist
import statistics as stat

# Connect to SQLite database
conn = sqlite3.connect('personality_database.db')

# Fetch necessary data from SQLite tables
questions = pd.read_sql_query("SELECT * FROM Questions;", conn)
factors = pd.read_sql_query("SELECT * FROM Factors;", conn)

# **************************WEB CREATION***************************

# Set the title of the main page
st.title("Big Personalities Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation - select the data visualisation you want to see")
page = st.sidebar.radio("Choose a page", ("Home", "Data Overview", "Questions-Answers distribution across the world"))

# Logic to display content based on the sidebar selection
if page == "Home":
    st.write("Welcome to the Big Personalities Analysis Tool. Select a page from the sidebar to begin.")
    st.write("Tutaj chatbot xd")
elif page == "Data Overview":
    st.write("Here you can see an overview of the dataset.")
    st.write("Description of the dataset, let's put link to .ipynb files with data cleaning, our github(?),"
             "link to Kaggle?")

# Place to add content to different pages:
# Histogram - Dawid ****************************************************
elif page == "Questions-Answers distribution across the world":
    selected_option = st.selectbox(
        "Which question's distribution would you like to see?",
        options=q_ids,
        index=0)

    selected_region = st.selectbox(
        "Which region would you like to see?",
        options=region_llist,
        index=0
    )

    # Extract question id from selected_option variable
    id_extracted = selected_option.split(":")[0]

    # Let's establish the filter for the selected region
    region_questions = questions[questions["Region"] == selected_region]

    # Filter the data based on selected region
    if selected_region == "All Regions":
        score_counts = questions[id_extracted].value_counts(normalize=True).sort_index()
    else:
        score_counts = region_questions[id_extracted].value_counts(normalize=True).sort_index()

    # Create the bar plot using Plotly Express
    fig = px.bar(
        x=score_counts.index,  # x-axis is the score values (1, 2, 3, 4, 5)
        y=score_counts.values,  # y-axis is the frequency of each score
        labels={'x': 'Score', 'y': 'Frequency'},  # axis labels
        title=f'Distribution of Scores for Question {id_extracted}'
    )

    # Show the bar plot inside the Streamlit app
    st.plotly_chart(fig)
# ***********************************************


# Close the SQLite connection
conn.close()
