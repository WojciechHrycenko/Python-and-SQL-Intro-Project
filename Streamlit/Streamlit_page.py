import streamlit as st
import pandas as pd
import plotly_express as px
import sqlite3
from Database_Preparation import q_ids, region_llist
import statistics as stat
import plotly.graph_objects as go
from plotly.colors import qualitative

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
page = st.sidebar.radio("Choose a page", ("Home", "Data Overview", "Region or country-based personalities", "Structure of answers", 
                                          "Questions-Answers distribution across the world", "Radar Chart of Five Personality Factors", "General Comparison", "Choropleth map"))


# Logic to display content based on the sidebar selection
if page == "Home":
    st.write("Welcome to the Big Personalities Analysis Tool. Select a page from the sidebar to begin.")
    st.write("Tutaj chatbot xd")
elif page == "Data Overview":
    st.write("Here you can see an overview of the dataset.")
    st.write("Description of the dataset, let's put link to .ipynb files with data cleaning, our github(?),"
             "link to Kaggle?")

# Place to add content to different pages:

# Region/country based personalities histogram - Weronika 
elif page == "Region or country-based personalities":
# First, we allow the user to choose whether they want to filter by region or country
    filter_by = st.radio("Select filter type", options=["Filter by Region", "Filter by Country"])
 # Showing region or country selection based on the user's choice
    if filter_by == "Filter by Region":
        region_options = factors['Region'].unique()
        selected_region = st.selectbox("Choose a region", options=["All regions"] + list(region_options))
        
        # Filtering data based on region selection
        if selected_region == "All regions":
            filtered_factors = factors
        else:
            filtered_factors = factors[factors['Region'] == selected_region]

        # Setting country options based on the region selected
        country_options = factors[factors['Region'] == selected_region]['Country'].unique()
        selected_country = None  # Reset country selection

    elif filter_by == "Filter by Country":
        country_options = factors['Country'].unique()
        selected_country = st.selectbox("Choose a country", options=["All countries"] + list(country_options))

        # Filtering data based on country selection
        if selected_country == "All countries":
            filtered_factors = factors
        else:
            filtered_factors = factors[factors['Country'] == selected_country]

        # Settting region options based on the country selected
        selected_region = None  # Reset region selection
        region_options = factors[factors['Country'] == selected_country]['Region'].unique()
            # Calculating the percentage of traits for the filtered data
    personality_traits = ['Extroversion', 'Emotional Stability', 'Agreeablness', 'Conscientiousness', 'Intellect/Imagination']
    trait_means = filtered_factors[personality_traits].mean()

    # Creating a bar chart
    fig = px.bar(
        x=personality_traits,
        y=trait_means.values,
        labels={'x': 'Personality trait', 'y': 'Average score'},
        title=f"Average personality traits for {selected_country if selected_country else 'all countries'} in {selected_region if selected_region else 'all regions'}"
    )

    # Showing the chart
    st.plotly_chart(fig)

# Structure of answers - Weronika
elif page == "Structure of answers":
    # Selecting a country
    country_options = factors['Country'].unique()
    selected_country = st.selectbox("Choose a country", options=["All countries"] + list(country_options))

    # Mapping features to their prefixes
    personality_features = {
        "Extroversion": "EXT",
        "Emotional Stability": "EST",
        "Agreeableness": "AGR",
        "Conscientiousness": "CSN",
        "Intellect/Imagination": "OPN"
    }

    # Selecting a personality feature
    selected_feature = st.selectbox(
        "Which personality feature would you like to analyze?",
        options=personality_features.keys()
    )

    # Getting the prefix for the selected feature
    feature_prefix = personality_features[selected_feature]

    # Filtering the dataset for the selected country
    country_data = questions[questions["Country"] == selected_country]

    # Extracting columns corresponding to the selected feature
    feature_questions = [col for col in country_data.columns if col.startswith(feature_prefix)]

    # Calculate the percentage share of each question's mean score
    question_means = country_data[feature_questions].mean()
    total_mean = question_means.sum()
    percentage_share = (question_means / total_mean) * 100

    # Create a pie chart
    fig = px.pie(
        names=question_means.index,  # Question shortcuts (e.g., EXT1, EXT2, etc.)
        values=percentage_share,  # Percentage share for each question
        title=f"Percentage share of {selected_feature} questions in {selected_country}"
    )

    # Display the pie chart
    st.plotly_chart(fig)



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
# Code written with help of AI 

elif page == "General Comparison":
    st.header("General Comparison of Personality Traits & Survey Answers within Coutntries and Regions")

    region_list = ["All Regions"] + sorted(questions["Region"].fillna("Unknown").unique())
    selected_region = st.selectbox("Choose a Region", options=region_list)

    if selected_region == "All Regions":
        country_list = ["All Countries"] + sorted(questions["Country"].fillna("Unknown").unique()) #had a trouble with NA values/ AI help
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
            "EXT": qualitative.Pastel1[0],  
            "AGR": qualitative.Pastel1[1],  
            "CSN": qualitative.Pastel1[2],  
            "EST": qualitative.Pastel1[3],  
            "OPN": qualitative.Pastel1[4] 
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
                                      f"<b>Mean Response:</b> {row['Mean_Response']:.2f}/5<br>"  # Średnia odpowiedź
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



# Density map of factors - Sasha ****************************************************
elif page == "Choropleth map":
    st.markdown("### Choropleth map of personality factors, HDI Rank and Happiness Rank")

    scaled_factors = factors.copy()
    scaled_factors[["Extroversion", "Emotional Stability", "Agreeablness", "Conscientiousness", "Intellect/Imagination"]] = scaled_factors[["Extroversion", "Emotional Stability", "Agreeablness", "Conscientiousness", "Intellect/Imagination"]] * 100
    
    grouped_factors = scaled_factors.pivot_table(
    index="Country", 
    values=["HDI rank", "Happiness Rank", "Extroversion", "Emotional Stability", "Agreeablness", "Conscientiousness", "Intellect/Imagination"]
    )
    grouped_factors_reset = grouped_factors.reset_index()  # Reset index so 'Country' is a column


    available_factors = grouped_factors_reset.columns.tolist()  # Get all column names
    available_factors.remove("Country")  # Remove 'Country' from the list of available factors
    
    selected_factor = st.selectbox(
    "Choose factor or rank",
    options=available_factors,
    index=0
    )
    
    
    if selected_factor == "HDI rank" or selected_factor == "Happiness Rank":
        fig_map = px.choropleth(
        grouped_factors_reset,
        locations= "Country",  
        locationmode= "country names",  
        color=selected_factor,  
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"{selected_factor} by country"
        )
    
    else:
        fig_map = px.choropleth(
        grouped_factors_reset,
        locations= "Country",
        locationmode= "country names",
        color=selected_factor,
        color_continuous_scale=px.colors.sequential.Viridis,
        title=f"{selected_factor} distribution by country"
        )
    

    
    
    
    st.plotly_chart(fig_map)




# ***********************************************

# Close the SQLite connection
conn.close()

