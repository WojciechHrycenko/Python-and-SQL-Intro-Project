import streamlit as st
import pandas as pd
import plotly_express as px
import sqlite3
from Database_Preparation import q_ids, region_llist
import statistics as stat
import plotly.graph_objects as go

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
page = st.sidebar.radio("Choose a page", ("Home", "Data Overview", "Questions-Answers distribution across the world", "Radar Chart of Five Personality Factors"))

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

# Radar / Pentagram Chart - Wojtek ****************************************************
elif page == "Radar Chart of Five Personality Factors":

    # Grouping data by Region and Country
    grouped_data = factors.groupby(["Region", "Country"]).agg({
        'Extroversion': 'mean',
        'Emotional Stability': 'mean',
        'Agreeablness': 'mean',
        'Conscientiousness': 'mean',
        'Intellect/Imagination': 'mean'
    }).reset_index()

    # Filtering data based on user selection
    region_list = grouped_data['Region'].unique()
    selected_region = st.selectbox("Choose region", options=["All Regions"] + list(region_list))

    if selected_region == "All Regions":
        country_list = grouped_data['Country'].unique()
    else:
        country_list = grouped_data[grouped_data['Region'] == selected_region]['Country'].unique()
    selected_country = st.selectbox("Choose country", options=["All Countries"] + list(country_list))

    if selected_region == "All Regions" and selected_country == "All Countries":
        filtered_data = grouped_data
    elif selected_region != "All Regions" and selected_country == "All Countries":
        filtered_data = grouped_data[grouped_data['Region'] == selected_region]
    elif selected_region == "All Regions" and selected_country != "All Countries":
        filtered_data = grouped_data[grouped_data['Country'] == selected_country]
    else:
        filtered_data = grouped_data[(grouped_data['Region'] == selected_region) & (grouped_data['Country'] == selected_country)]

# If "All Regions" and "All Countries" is selected, plot all countries
    if selected_region == "All Regions" and selected_country == "All Countries":
        fig = go.Figure()

        # Loop through all rows of filtered data and plot each country's radar chart
        for index, row in filtered_data.iterrows():
            personality_values = [
                row['Extroversion'],
                row['Emotional Stability'],
                row['Agreeablness'],
                row['Conscientiousness'],
                row['Intellect/Imagination']
            ]
            personality_labels = ['Extroversion', 'Emotional Stability', 'Agreeablness', 'Conscientiousness', 'Intellect/Imagination']

            fig.add_trace(go.Scatterpolar(
                r=personality_values,
                theta=personality_labels,
                fill='toself',
                name=f"{row['Country']} ({row['Region']})"
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            title="Radar Chart for All Countries and Regions",
            showlegend=True
        )

    else:
        # Selecting just the first row if region and country are specific
        selected_row = filtered_data.iloc[0]

        # Personalities values
        personality_values = [
            selected_row['Extroversion'],
            selected_row['Emotional Stability'],
            selected_row['Agreeablness'],
            selected_row['Conscientiousness'],
            selected_row['Intellect/Imagination']
        ]

        # Personalities labels for the radar chart
        personality_labels = ['Extroversion', 'Emotional Stability', 'Agreeablness', 'Conscientiousness', 'Intellect/Imagination']

        # Create a radar chart for the selected data
        fig = go.Figure(data=go.Scatterpolar(
            r=personality_values,
            theta=personality_labels,
            fill='toself',
            name=selected_row['Country']
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            title=f"Radar Chart for {selected_row['Country']} in {selected_row['Region']}",
            showlegend=False
        )

    st.plotly_chart(fig)
# ***********************************************

# Close the SQLite connection
conn.close()
