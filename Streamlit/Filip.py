import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt

# Load data
questions_df = pd.read_csv("Datasets/optimized_questions.csv")
factors_df = pd.read_csv("Datasets/factors_dataset.csv")

# Map questions to full descriptions
q_ids = [
    "EXT1: I am the life of the party.",
    "EXT2: I don't talk a lot.",
    "EXT3: I feel comfortable around people.",
    "EXT4: I keep in the background.",
    "EXT5: I start conversations.",
    "EXT6: I have little to say.",
    "EXT7: I talk to a lot of different people at parties.",
    "EXT8: I don't like to draw attention to myself.",
    "EXT9: I don't mind being the center of attention.",
    "EXT10: I am quiet around strangers.",
    "EST1: I get stressed out easily.",
    "EST2: I am relaxed most of the time.",
    "EST3: I worry about things.",
    "EST4: I seldom feel blue.",
    "EST5: I am easily disturbed.",
    "EST6: I get upset easily.",
    "EST7: I change my mood a lot.",
    "EST8: I have frequent mood swings.",
    "EST9: I get irritated easily.",
    "EST10: I often feel blue.",
    "AGR1: I feel little concern for others.",
    "AGR2: I am interested in people.",
    "AGR3: I insult people.",
    "AGR4: I sympathize with others' feelings.",
    "AGR5: I am not interested in other people's problems.",
    "AGR6: I have a soft heart.",
    "AGR7: I am not really interested in others.",
    "AGR8: I take time out for others.",
    "AGR9: I feel others' emotions.",
    "AGR10: I make people feel at ease.",
    "CSN1: I am always prepared.",
    "CSN2: I leave my belongings around.",
    "CSN3: I pay attention to details.",
    "CSN4: I make a mess of things.",
    "CSN5: I get chores done right away.",
    "CSN6: I often forget to put things back in their proper place.",
    "CSN7: I like order.",
    "CSN8: I shirk my duties.",
    "CSN9: I follow a schedule.",
    "CSN10: I am exacting in my work.",
    "OPN1: I have a rich vocabulary.",
    "OPN2: I have difficulty understanding abstract ideas.",
    "OPN3: I have a vivid imagination.",
    "OPN4: I am not interested in abstract ideas.",
    "OPN5: I have excellent ideas.",
    "OPN6: I do not have a good imagination.",
    "OPN7: I am quick to understand things.",
    "OPN8: I use difficult words.",
    "OPN9: I spend time reflecting on things.",
    "OPN10: I am full of ideas."
]

# Create a dictionary mapping question codes to descriptions
question_map = {q.split(": ")[0]: q.split(": ")[1] for q in q_ids}

# Sidebar filtering
st.sidebar.title("General Comparison Filters")
region_list = ['All Regions', 'Middle East and Northern Africa', 'Latin America and Caribbean',
               'Western Europe', 'Australia and New Zealand',
               'Central and Eastern Europe', 'North America',
               'Southeastern Asia', 'Southern Asia', 'Eastern Asia',
               'Sub-Saharan Africa']
selected_region = st.sidebar.selectbox("Choose a Region", options=region_list)
selected_country = st.sidebar.selectbox("Choose a Country", options=["All Countries"] + list(factors_df["Country"].unique()))

# Filter data by region or country
if selected_country != "All Countries":
    filtered_data = questions_df[questions_df["Country"] == selected_country]
    trait_data = factors_df[factors_df["Country"] == selected_country]
elif selected_region != "All Regions":
    filtered_data = questions_df[questions_df["Region"] == selected_region]
    trait_data = factors_df[factors_df["Region"] == selected_region]
else:
    filtered_data = questions_df
    trait_data = factors_df

# Calculate mean responses for each question
question_columns = [col for col in questions_df.columns if col.startswith(("EXT", "AGR", "CSN", "EST", "OPN"))]
question_means = filtered_data[question_columns].mean().reset_index()
question_means.columns = ["Question", "Mean_Response"]

# Map questions to their descriptions and traits
question_means["Trait"] = question_means["Question"].str[:3]

# Calculate trait levels directly from the factors dataset
trait_levels = trait_data[
    ["Extroversion", "Agreeablness", "Conscientiousness", "Emotional Stability", "Intellect/Imagination"]
].mean().reset_index()
trait_levels.columns = ["Trait", "Trait_Level"]

# Map trait names to their codes
trait_map = {
    "Extroversion": "EXT",
    "Agreeablness": "AGR",
    "Conscientiousness": "CSN",
    "Emotional Stability": "EST",
    "Intellect/Imagination": "OPN"
}
trait_levels["Trait"] = trait_levels["Trait"].map(trait_map)

# Merge trait levels back to questions
question_means = question_means.merge(trait_levels, on="Trait")

# Scale question levels to fit the trait level
question_means["Scaled_Response"] = (
    question_means["Mean_Response"] / question_means["Mean_Response"].sum()
) * question_means["Trait_Level"]

# Define valid colormap names for each trait
trait_colors = {
    "EXT": "Blues",
    "AGR": "Greens",
    "CSN": "Oranges",
    "EST": "Reds",
    "OPN": "Purples"
}

# Generate shades of colors for each question
def generate_shades(colormap_name, n):
    cmap = plt.get_cmap(colormap_name)  # Use colormap name
    return [cmap(i / (n - 1)) for i in range(n)]  # Generate n shades

# Create the stacked bar plot
stacked_bar_data = []
for trait, group in question_means.groupby("Trait"):
    n_questions = len(group)
    shades = generate_shades(trait_colors[trait], n_questions)
    for i, (index, row) in enumerate(group.iterrows()):
        stacked_bar_data.append(
            go.Bar(
                x=[trait],  # Repeated trait name for stacking
                y=[row["Scaled_Response"]],  # Scaled responses
                text=row["Question"],  # Hover info displays only the question code
                marker_color=f"rgba({int(shades[i][0]*255)}, {int(shades[i][1]*255)}, {int(shades[i][2]*255)}, {shades[i][3]})"
            )
        )

# Plot the data
fig = go.Figure(data=stacked_bar_data)
fig.update_layout(
    barmode="stack",
    title="Stacked Bar Plot of Questions by Personality Traits",
    xaxis_title="Personality Traits",
    yaxis_title="Trait Level",
    hovermode="x unified",
    showlegend=False  # Disable legend
)

# Display the plot in Streamlit
st.plotly_chart(fig)
