# The aim of this file is to create an SQL database (.db format file) with our datasets as tables
import sqlite3
import pandas as pd


# List of CSV files and corresponding table names
csv_files = ['Datasets/optimized_questions.csv', 'Datasets/factors_dataset.csv']
table_names = ['Questions', 'Factors']

# Create a SQLite database
conn = sqlite3.connect("personality_database.db")

try:
    # Loop through each CSV file and table name
    for csv_file, table_name in zip(csv_files, table_names):
        # 1. Read CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)

        # 2. Save DataFrame created above to the SQLite database as a table
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        print(f"Table '{table_name}' has been created from '{csv_file}'.")
finally:
    # Close the connection
    conn.close()