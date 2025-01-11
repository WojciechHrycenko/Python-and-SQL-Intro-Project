import streamlit as st
import pandas as pd
import plotly_express as px
import sqlite3
from Database_Preparation import q_ids, region_llist
import statistics as stat
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

# Funkcja do generowania odcieni w razie potrzeby - FILIP with help of AI
# To be cleaned & and translated to english and verified
def generate_shades(base_colors, n_questions):
    if len(base_colors) >= n_questions:
        return base_colors[:n_questions]
    else:
        # Interpolacja kolorów, jeśli brakuje odcieni
        color_array = np.linspace(0, 1, n_questions)
        return px.colors.sample_colorscale(base_colors, color_array)


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
page = st.sidebar.radio("Choose a page", ("Home", "Data Overview", "Questions-Answers distribution across the world", "Radar Chart of Five Personality Factors", "General Comparison"))


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

# GENERAL COMPARISON - Filip ****************************************************
# Code written with help of AI - chatgpt precisely
# To be cleaned & and translated to english and verified
# GENERAL COMPARISON - Filip ****************************************************
elif page == "General Comparison":
    st.header("General Comparison of Personality Traits Across Countries and Regions")

    # Pobranie danych z bazy (na początku)
    questions = pd.read_sql_query("SELECT * FROM Questions;", conn)
    factors = pd.read_sql_query("SELECT * FROM Factors;", conn)

    # Wybór regionu i kraju
    region_list = ["All Regions"] + sorted(questions["Region"].fillna("Unknown").unique())
    selected_region = st.selectbox("Choose a Region", options=region_list)

    if selected_region == "All Regions":
        country_list = ["All Countries"] + sorted(questions["Country"].fillna("Unknown").unique())
    else:
        country_list = ["All Countries"] + sorted(
            questions[questions["Region"] == selected_region]["Country"].fillna("Unknown").unique()
        )
    selected_country = st.selectbox("Choose a Country", options=country_list)

    # Filtrowanie danych w Pythonie
    if selected_region == "All Regions" and selected_country == "All Countries":
        filtered_questions = questions
        filtered_factors = factors
    elif selected_region != "All Regions" and selected_country == "All Countries":
        filtered_questions = questions[questions["Region"] == selected_region]
        filtered_factors = factors[factors["Region"] == selected_region]
    elif selected_region == "All Regions" and selected_country != "All Countries":
        filtered_questions = questions[questions["Country"] == selected_country]
        filtered_factors = factors[factors["Country"] == selected_country]
    else:
        filtered_questions = questions[
            (questions["Region"] == selected_region) & (questions["Country"] == selected_country)
        ]
        filtered_factors = factors[
            (factors["Region"] == selected_region) & (factors["Country"] == selected_country)
        ]

    # Sprawdzenie, czy mamy dane po filtrowaniu
    if filtered_questions.empty or filtered_factors.empty:
        st.error("No data available for the selected region or country. Please choose different filters.")
    else:
        # Obliczanie średnich odpowiedzi na pytania
        question_columns = [col for col in filtered_questions.columns if col.startswith(("EXT", "AGR", "CSN", "EST", "OPN"))]
        question_means = filtered_questions[question_columns].mean().reset_index()
        question_means.columns = ["Question", "Mean_Response"]
        question_means["Trait"] = question_means["Question"].str[:3]

        # Obliczanie średnich wartości cech osobowości
        trait_means = filtered_factors[[
            "Extroversion", "Emotional Stability", "Agreeablness", 
            "Conscientiousness", "Intellect/Imagination"
        ]].mean().reset_index()
        trait_means.columns = ["Trait", "Trait_Level"]

        trait_map = {
            "Extroversion": "EXT",
            "Emotional Stability": "EST",
            "Agreeablness": "AGR",
            "Conscientiousness": "CSN",
            "Intellect/Imagination": "OPN"
        }
        trait_means["Trait"] = trait_means["Trait"].map(trait_map)

        # Łączenie cech z pytaniami
        merged_data = question_means.merge(trait_means, on="Trait")

        # Skalowanie odpowiedzi na pytania w ramach danej cechy
        merged_data["Scaled_Response"] = (
            merged_data["Mean_Response"] / merged_data.groupby("Trait")["Mean_Response"].transform("sum")
        ) * merged_data["Trait_Level"]

        # Dodanie dodatkowej metryki: Mean_Response podzielone przez sumę odpowiedzi dla cechy
        merged_data["Contribution"] = (merged_data["Mean_Response"] / merged_data.groupby("Trait")["Mean_Response"].transform("sum")) * merged_data["Trait_Level"]


        # Dodanie pełnej treści pytań do danych
        question_map = {q.split(": ")[0]: q.split(": ")[1] for q in q_ids}  # Mapowanie kodów pytań na pełne opisy
        merged_data["Full_Question"] = merged_data["Question"].map(question_map)  # Mapowanie pełnych treści pytań

        # Przygotowanie jednolitych kolorów dla cech
        trait_colors = {
            "EXT": "blue",
            "AGR": "green",
            "CSN": "orange",
            "EST": "red",
            "OPN": "purple"
        }

        # Generowanie danych do wykresu stacked bar plot
        stacked_bar_data = []
        annotations = []  # Lista na wartości cech nad słupkami
        for trait, group in merged_data.groupby("Trait"):
            for i, (index, row) in enumerate(group.iterrows()):
                # Dodawanie barów do wykresu
                stacked_bar_data.append(
                    go.Bar(
                        x=[trait],
                        y=[row["Scaled_Response"]],
                        text=row["Question"],  # Kod pytania w słupku
                        textposition="inside",  # Kod pytania wyświetlany w środku słupka
                        textfont=dict(size=10, color="black"),  # Jednolity styl dla wszystkich kodów pytań
                        marker_color=trait_colors[trait],  # Ujednolicony kolor dla cechy
                        marker_line=dict(width=1, color="black"),  # Dodanie linii rozdzielających poziomy
                        hovertemplate=f"<b>Trait:</b> {trait}<br>"  # Wyświetlenie nazwy cechy
                                      f"<b>Question Code:</b> {row['Question']}<br>"  # Kod pytania
                                      f"<b>Full Question:</b> {row['Full_Question']}<br>"  # Pełna treść pytania
                                      f"<b>Mean Response:</b> {row['Mean_Response']:.2f}<br>"  # Średnia odpowiedź
                                      f"<b>Contribution:</b> {row['Contribution']:.2f}<extra></extra>",  # Normalizowany udział
                    )
                )

            # Dodanie wartości cechy nad słupkiem
            trait_level = group["Trait_Level"].iloc[0]  # Wartość cechy
            annotations.append(
                dict(
                    x=trait,  # Pozycja na osi X
                    y=group["Scaled_Response"].sum() + 0.05,  # Pozycja wyżej nad słupkiem
                    text=f"{trait_level:.3f}",  # Wartość cechy (3 miejsca po przecinku)
                    showarrow=False,
                    font=dict(size=12, color="white"),  # Styl tekstu: biały kolor
                )
            )

        # Tworzenie wykresu
        fig = go.Figure(data=stacked_bar_data)
        fig.update_layout(
            barmode="stack",
            title="Comparison of Personality Traits",
            xaxis_title="Personality Traits",
            yaxis_title="Trait Level",
            annotations=annotations,  # Dodanie wartości nad słupkami
            hovermode="closest",
            showlegend=False
        )

        # Wyświetlenie wykresu
        st.plotly_chart(fig)





# ***********************************************


# ***********************************************

# Close the SQLite connection
conn.close()

