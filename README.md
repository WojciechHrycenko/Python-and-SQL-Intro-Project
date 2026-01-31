# Big Personalities Analysis - Python & SQL Project

![Project Status](https://img.shields.io/badge/Status-Completed-green)
![Course](https://img.shields.io/badge/Course-Python%20%26%20SQL-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Plotly](https://img.shields.io/badge/Library-Plotly-3F4F75?logo=plotly&logoColor=white)

## Project Overview

This repository contains a comprehensive data analysis and visualization tool focused on **Psychological Data Visualization**. The project utilizes the "Big Five" personality traits dataset to explore global personality patterns. By integrating raw survey results with global indices like **HDI** and **Happiness Rank**, the application provides an interactive platform to analyze how personality factors vary across different regions and countries.

## Authors
* **Aliaksandra Labko**
* **Weronika Mądro**
* **Dawid Grzesiak**
* **Filip Żebrowski**
* **Wojciech Hrycenko**

---

## Repository Contents

### 1. Interactive Analysis Tool
**File:** `Streamlit_page.py`

**Objective**
The main goal of this application is to visualize and compare personality traits globally through:
1.  **Global Distribution:** Analyzing how answers to specific personality questions are distributed across different world regions.
2.  **Trait Comparison:** Using Radar Charts to compare the Five Factor Model (FFM) profiles between countries.
3.  **Socio-economic Correlation:** Visualizing personality factors alongside HDI and Happiness Ranks using Choropleth Maps.
4.  **Data Normalization:** Comparing regional personality scores using Z-score standardization.

**Dataset**
The project is based on the **Big Five Personality Test** dataset from Kaggle, originally containing over **1,000,000 responses**. The data was processed into two optimized tables:
* `factors_dataset.csv`: Aggregated scores for Extroversion, Emotional Stability, Agreeableness, Conscientiousness, and Openness.
* `optimized_questions.csv`: Individual item responses with optimized scales.

**Methodology**
* **Data Processing:**
    * **Cleaning & Sampling:** Reducing row count for performance and ensuring equal sampling.
    * **Optimization:** Reverting contradictory questions and consolidating 50 columns into 5 core personality factors.
    * **Enrichment:** Merging survey data with geographic info, HDI Rank, and Happiness Rank.
* **Architecture:**
    * **Storage:** Data is migrated from CSV files to a **SQLite** database (`personality_database.db`) for efficient querying.
    * **Frontend:** An interactive dashboard built with **Streamlit** featuring sidebar navigation and dynamic filtering.
* **Visualizations:**
    * Interactive Radar Charts, Choropleth Maps, Stacked Bar Plots, and Pie Charts powered by **Plotly Express** and **Graph Objects**.

---

## Technologies and Libraries

The project was developed in **Python**, utilizing the following key technologies:

* **Streamlit:** For building the interactive web interface.
* **SQLite3:** For relational data storage and SQL-based data retrieval.
* **Pandas:** For data manipulation, cleaning, and CSV/SQL integration.
* **Plotly & Matplotlib:** For creating diverse interactive and static visualizations.
* **Statistics:** For calculating Z-scores and data normalization.

## Usage Instructions

1.  Clone this repository to your local machine.
2.  Navigate to the `Streamlit` folder.
3.  Install required dependencies (Streamlit, Pandas, Plotly, Matplotlib).
4.  Run the following command to start the application:
    ```bash
    python -m streamlit run Streamlit_page.py
    ```
    *(Note: Ensure `personality_database.db` is generated using `Data_transfer.py` if not already present)*.
5.  Use the sidebar to navigate between different data visualization modules, such as the **Radar Chart** or **Choropleth Map**.
