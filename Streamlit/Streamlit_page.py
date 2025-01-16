import streamlit as st
import pandas as pd
import plotly_express as px
import sqlite3
from Variables import q_ids, region_llist
import statistics as stat
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.colors import qualitative
import matplotlib.pyplot as plt


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
page = st.sidebar.radio("Choose a page", ("Home", "Data Overview", "Questions-Answers Distribution Across the World",
                                           "Radar Chart of Five Personality Factors", "General Comparison", "Choropleth Map", "Normalized Data Comparison"))


# Logic to display content based on the sidebar selection
if page == "Home":
    st.write("Welcome to the Big Personalities Analysis Tool. Select a page from the sidebar to begin.")

    st.image("https://miro.medium.com/v2/resize:fit:1400/1*ZLc8umeA7FMlQ3cpUJBS5A.jpeg")

elif page == "Data Overview":
    st.write("Here you can see an overview of the dataset.")
    
    # AI help was used to modify variable 'text' to look better
    text = """
    ### Dataset Information

    The initial dataset *('data-final.csv')* was taken from Kaggle: [link](https://www.kaggle.com/datasets/tunguz/big-five-personality-test).  
    This dataset contained **1,015,342 questionnaire answers** (rows) collected online about Big Five personality traits, also known as the Five-Factor Model (FFM), which is a grouping for personality traits.

    ### Data Transformation Process

    The **'data-final.csv'** was transformed multiple times:  
    1️⃣ **Reduce the number of rows**: Equal sampling was applied to make the dataset more consistent.  
    2️⃣ **Optimize question answers**: Some questions were contradictory, so their values were reverted.  
    3️⃣ **Summarize 50 columns**: Consolidated questions into five personality factors.  
    4️⃣ **Additional data**: Added Happiness Rank, HDI Rank, Country Code, and Region.

    After transforming *'data-final.csv'*, two files were created as outcomes:  
    - **'factors_dataset.csv'**  
    - **'optimized_questions.csv'**

    ### File Details

    #### 📁 **factors_dataset.csv**  
    This file contains **13 columns**:  
    - **id**: Unique identifier for each record.  
    - **lat_appx_lots_of_err** & **long_appx_lots_of_err**: Approximate latitude and longitude of the respondent's location.  
    - **Country**, **Country_Code**, **Region**: Geographic information about the respondent.  
    - **Happiness Rank**: Respondent's country's rank in a happiness index.  
    - **HDI Rank**: Human Development Index rank of the respondent's country.  
    - **Extroversion**, **Emotional Stability**, **Agreeableness**, **Conscientiousness**, **Intellect/Imagination**: Scores on the Big Five personality traits.

    💡 **Summary**: This file provides personality trait scores alongside geographic and global index information.

    #### 📁 **optimized_questions.csv**  
    This file contains **58 columns**:  
    - **id**: Unique identifier for each record.  
    - **EXT1 to EXT10**: Responses related to Extroversion.  
    - **EST1 to EST10**: Responses related to Emotional Stability.  
    - **AGR1 to AGR10**: Responses related to Agreeableness.  
    - **CSN1 to CSN10**: Responses related to Conscientiousness.  
    - **OPN1 to OPN10**: Responses related to Intellect/Imagination (Openness).  
    - Geographic and global indices similar to `factors_dataset.csv`.

    💡 **Summary**: This file is similar to the initial dataset but with optimized and sampled questions. It includes detailed question-by-question responses for the Big Five personality traits.
    
    
    #### **factors_dataset.csv** and **optimized_questions.csv** were merged using SQLite into a single database, which was utilized in the main and final Python script for the Streamlit page. 
    
    """
        
    st.markdown(text)


# Place to add content to different pages:

# Histogram - Dawid ****************************************************
elif page == "Questions-Answers Distribution Across the World":
    selected_option = st.selectbox(
        "Select question?",
        options=q_ids,
        index=0)

    selected_region = st.selectbox(
        "Select region?",
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

# Radar / Pentagram Chart and Region/Country based histogram - Wojtek and Weronika ***********
# Code written with help of AI
# For the radar chart, I (Wojtek) was using AI mostly for solving some problems with the code, I was basing as much as possible on documentation of Plotly: https://plotly.com/python/polar-chart/.
elif page == "Radar Chart of Five Personality Factors":

    # Grouping data by Region and Country
    grouped_data = factors.groupby(["Region", "Country"]).agg({
        'Agreeablness': 'mean',
        'Conscientiousness': 'mean',
        'Emotional Stability': 'mean',
        'Extroversion': 'mean',       
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
                row['Agreeablness'],
                row['Conscientiousness'],
                row['Emotional Stability'],
                row['Extroversion'],
                row['Intellect/Imagination']
            ]
            personality_labels = ['Agreeablness', 'Conscientiousness', 'Emotional Stability', 'Extroversion', 'Intellect/Imagination']

            fig.add_trace(go.Scatterpolar(
                r=personality_values,
                theta=personality_labels,
                fill='toself',
                name=f"{row['Country']} ({row['Region']})"
            ))

            fig.update_traces(
                hovertemplate="Trait Value: %{r}<br>Personality Trait: %{theta}<extra></extra>"
            )

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1],
                        tickfont=dict(color="black")
                    ),
                    angularaxis=dict(
                        tickmode='array',
                        tickvals=[0, 1, 2, 3, 4],
                        ticktext=personality_labels
                    )
                ),
                title="Radar Chart for All Countries and Regions",
                showlegend=True,
                legend=dict(
                    x=1.1,
                    y=0.5,
                    xanchor="left",
                    yanchor="middle",
                    orientation="v",
                    font=dict(size=12)
                )
            )


    else:
        # Selecting just the first row if region and country are specific
        selected_row = filtered_data.iloc[0]

        # Personalities values
        personality_values = [
            selected_row['Agreeablness'],
            selected_row['Conscientiousness'],
            selected_row['Emotional Stability'],
            selected_row['Extroversion'],
            selected_row['Intellect/Imagination']
        ]

        personality_labels = ['Agreeablness', 'Conscientiousness', 'Emotional Stability', 'Extroversion', 'Intellect/Imagination']

        # Creating a radar chart for the selected data
        fig = go.Figure(data=go.Scatterpolar(
            r=personality_values,
            theta=personality_labels,
            fill='toself',
            name=selected_row['Country']
        ))

        fig.update_traces(
            hovertemplate="Trait Value in 0-1 Scale: %{r}<br>Personality Trait: %{theta}<extra></extra>"
        )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickfont=dict(color="black")
                ),
                angularaxis=dict(
                    tickmode='array',
                    tickvals=[0, 1, 2, 3, 4],
                    ticktext=personality_labels
                )
            ),
            title="Radar Chart for All Countries and Regions",
            showlegend=True
        )

    st.plotly_chart(fig)

  # Creating the bar chart for trait means
    trait_means = filtered_data[personality_labels].mean()
    bar_fig = px.bar(
        x=personality_labels,
        y=trait_means,
        labels={'x': 'Personality Trait', 'y': 'Average Score'},
        title="Average Personality Traits"
    )

    st.plotly_chart(bar_fig)
    

# General Comparison - Filip. Code written with help of AI - models: o1 and GPT-4o
# Scope: i asked AI if i had trouble with running code properly and it helped me to solve the problems

elif page == "General Comparison":
    st.header("General Comparison of Personality Factors & Survey Answers within Coutntries and Regions")

#region_llist got from database_preparation.py
    selected_region = st.selectbox("Choose a Region", options=region_llist) 

    if selected_region == "All Regions":
        country_list = ["All Countries"] + sorted(questions["Country"].unique()) 
    else:
        country_list = ["All Countries"] + sorted(
            questions[questions["Region"] == selected_region]["Country"].unique()
        )
    selected_country = st.selectbox("Choose a Country", options=country_list)

    # Filtering data (questions and factors) based on user selection. Checked with AI if all conditions are fullfiled as the if function is quite complex
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

    # Error handling if no data is available
    if filtered_questions.empty or filtered_factors.empty:
        st.error("No data available for the selected region or country. Please choose different filters.")
    else:
        # Mean response for each question
        question_columns = [col for col in filtered_questions.columns if col.startswith(("EXT", "AGR", "CSN", "EST", "OPN"))]
        question_means = filtered_questions[question_columns].mean().reset_index()
        question_means.columns = ["Question", "Mean_Response"]
        question_means["Factor"] = question_means["Question"].str[:3]

        # Mean factor level for each factor
        factor_means = filtered_factors[[
            "Extroversion", "Emotional Stability", "Agreeablness", 
            "Conscientiousness", "Intellect/Imagination"
        ]].mean().reset_index()
        factor_means.columns = ["Factor", "Factor_Level"]

        factor_dict = {
            "Extroversion": "EXT",
            "Emotional Stability": "EST",
            "Agreeablness": "AGR",
            "Conscientiousness": "CSN",
            "Intellect/Imagination": "OPN"
        }
        factor_means["Factor"] = factor_means["Factor"].apply(lambda key: factor_dict[key])

        # Merging factor means with question means
        merged_data = question_means.merge(factor_means, on="Factor")

        # Scaling the mean response based on factor level for stacked bar plot purposes
        merged_data["Scaled_Response"] = (
            merged_data["Mean_Response"] / merged_data.groupby("Factor")["Mean_Response"].transform("sum")
        ) * merged_data["Factor_Level"]

        # Contributions
        merged_data["Contribution"] = (merged_data["Mean_Response"] / merged_data.groupby("Factor")["Mean_Response"].transform("sum")) * merged_data["Factor_Level"]

        # Full question text
        question_dict = dict(q.split(": ", 1) for q in q_ids)
        merged_data["Full_Question"] = merged_data["Question"].apply(lambda key: question_dict.get(key))
        
        #AI suggested below to improve my but i didn't like it because i dont know map()
        #question_map = {q.split(": ")[0]: q.split(": ")[1] for q in q_ids}  #Dictionary comprehensions in q_ids list
        #merged_data["Full_Question"] = merged_data["Question"].map(question_map)  

        # Pastel colors for each factor. AI suggested to use qulivative as i asked it to help me assign pastel colors
        
        #factor_colors = {
         #   "EXT": "red",  
         #   "AGR": "blue",  
         #   "CSN": "green",  
         #   "EST": "yellow",  
         #   "OPN": "purple" 
        #}
        
        factor_colors = {
            "EXT": qualitative.Pastel1[0],  
            "AGR": qualitative.Pastel1[1],  
            "CSN": qualitative.Pastel1[2],  
            "EST": qualitative.Pastel1[3],  
            "OPN": qualitative.Pastel1[4] 
        }

        # Plotting the stacked bar plot. AI suggested to use go.Bar() as i asked it to help me with the plot. Asked him for marker_line sugggestion
        #as i am new to plotly i also asked about adjusting features of the plot like hovertemplate, textposition, textfont and marker_color
        #AI helped me with HTML part of hovertemplate
        stacked_bar_data = []
        labels = []  
        for factor, group in merged_data.groupby("Factor"):
            for i, (index, row) in enumerate(group.iterrows()):
                
                stacked_bar_data.append(
                    go.Bar(
                        x=[factor],
                        y=[row["Scaled_Response"]],
                        text=row["Question"],  
                        textposition="inside",  
                        textfont=dict(size=8, color="black"),  
                        marker_color=factor_colors[factor],  
                        marker_line=dict(width=1, color="black"),  
                        hovertemplate=
                                      f"<b>Full Question:</b> {row['Full_Question']}<br>" 
                                      f"<b>Mean Response:</b> {row['Mean_Response']:.2f}/5<br>"  
                                      f"<b>Contribution:</b> {row['Contribution']:.2f}<extra></extra>",  
                    )
                )

            factor_level = group["Factor_Level"].iloc[0] 
            labels.append(
                dict(
                    x=factor,  
                    y=group["Scaled_Response"].sum() + 0.05,
                    text=f"{factor_level:.3f}",  
                    showarrow=False,
                    font=dict(size=12, color="white"), 
                )
            )

        fig = go.Figure(data=stacked_bar_data)
        fig.update_layout(
            barmode="stack",
            title="How responses creates levels of factor",
            xaxis_title="Personality Factors",
            yaxis_title="Factor Level",
            annotations=labels,  #labeling the factor levels
            hovermode="closest",
            showlegend=False
        )

        # Show the plot
        st.plotly_chart(fig)

# Pie Chart: Structure of Answers - Weronika ****************************************************

        st.subheader("Structure of Answers")

        st.markdown("""The pie chart illustrates the percentage contribution of each survey question to the overall score for the 
        selected personality feature, providing insights into how individual questions contribute to the evaluation 
        of the trait.""") 

        personality_features = {
            "Extroversion": "EXT",
            "Emotional Stability": "EST",
            "Agreeableness": "AGR",
            "Conscientiousness": "CSN",
            "Intellect/Imagination": "OPN"
        }

        # Personality feature selecion
        selected_feature = st.selectbox("Choose a Personality Feature", options=personality_features.keys())
        feature_prefix = personality_features[selected_feature]

        # Identifying the relevant question
        country_data = filtered_questions if selected_country == "All Countries" else filtered_questions[filtered_questions["Country"] == selected_country]
        feature_questions = [col for col in country_data.columns if col.startswith(feature_prefix)]
        question_means = country_data[feature_questions].mean()
        total_mean = question_means.sum()
        percentage_share = (question_means / total_mean) * 100

        # Creating the pie chart
        pie_fig = px.pie(
            names=question_means.index,
            values=percentage_share,
            title=f"Percentage Share of {selected_feature} Questions",
        )

        # Show the plot
        st.plotly_chart(pie_fig)


# Density map of factors - Sasha ****************************************************
## AI help was used to optimize the code 
elif page == "Choropleth Map":
    st.markdown("### Choropleth map of personality factors, HDI Rank and Happiness Rank")

    scaled_factors = factors.copy()
    scaled_factors[["Extroversion", "Emotional Stability", "Agreeablness", "Conscientiousness", "Intellect/Imagination"]] = scaled_factors[["Extroversion", "Emotional Stability", "Agreeablness", "Conscientiousness", "Intellect/Imagination"]] * 100
    
    grouped_factors = scaled_factors.pivot_table(
    index="Country", 
    values=["HDI rank", "Happiness Rank", "Extroversion", "Emotional Stability", "Agreeablness", "Conscientiousness", "Intellect/Imagination"]
    )
    # Reset index so 'Country' is a column - AI helped to figure out this line of code
    grouped_factors_reset = grouped_factors.reset_index()  

    # Get all column names
    available_factors = grouped_factors_reset.columns.tolist()
    # Remove 'Country' from the list of available factors
    available_factors.remove("Country")  
    
    selected_factor = st.selectbox(
    "Choose factor or rank",
    options=available_factors,
    index=0
    )
    
    # AI helped with how some variables should be written
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


# *********************************************** Normalized data comparison - Dawid
elif page == "Normalized Data Comparison":
    grouped_factors = factors.groupby("Region")[['Extroversion',
                                                  'Emotional Stability', 'Agreeablness', 'Conscientiousness',
                                                  'Intellect/Imagination']].mean()
    means = grouped_factors.mean()
    std_devs = grouped_factors.std()

    # Apply Z-score normalization - with help of AI
    standardized_factors = grouped_factors.apply(lambda x: (x - means[x.name]) / std_devs[x.name], axis=0)

    # Setting the page elements
    personality_traits = ['Extroversion', 'Emotional Stability', 'Agreeablness', 'Conscientiousness', 'Intellect/Imagination']

    selected_option = st.selectbox("Choose factor:",options = personality_traits)

    # The graph - with help of AI
    if selected_option:
        selected_trait_data = standardized_factors[selected_option]

        # Create the bar plot for the selected trait
        fig, ax = plt.subplots(figsize=(10, 6))
        selected_trait_data.plot(kind='bar', ax=ax, color='skyblue')

        # Title and labels for the plot
        plt.title(f'Standardized Z-Score of {selected_option} by Region')
        plt.xlabel('Region')
        plt.ylabel('Standardized Score (Z-score)')

        # Display the plot in Streamlit app
        st.pyplot(fig)


# Close the SQLite connection
conn.close()