import pandas as pd

# Wczytaj plik CSV do DataFrame
df = pd.read_csv('cleaned_big_personalities_dataset.csv', sep=',')

df = df.reset_index(drop=True)
df['id'] = df.index

columns = ['id'] + list(df.columns[:-1])
df = df[columns]

columns_to_melt = [
    'EXT1', 'EXT2', 'EXT3', 'EXT4', 'EXT5', 'EXT6', 'EXT7', 'EXT8', 'EXT9', 'EXT10', 
    'EST1', 'EST2', 'EST3', 'EST4', 'EST5', 'EST6', 'EST7', 'EST8', 'EST9', 'EST10', 
    'AGR1', 'AGR2', 'AGR3', 'AGR4', 'AGR5', 'AGR6', 'AGR7', 'AGR8', 'AGR9', 'AGR10', 
    'CSN1', 'CSN2', 'CSN3', 'CSN4', 'CSN5', 'CSN6', 'CSN7', 'CSN8', 'CSN9', 'CSN10', 
    'OPN1', 'OPN2', 'OPN3', 'OPN4', 'OPN5', 'OPN6', 'OPN7', 'OPN8', 'OPN9', 'OPN10'
]

df = pd.melt(df, id_vars = ["id", "dateload","screenw","screenh","introelapse","testelapse","endelapse","IPC","country","lat_appx_lots_of_err","long_appx_lots_of_err"], value_vars=columns_to_melt, var_name='question_id', value_name='answer')

columns_to_remove = ['dateload', 'screenw', 'screenh', 'introelapse', 'testelapse', 'endelapse', 'IPC']
df.drop(columns=columns_to_remove, inplace=True)
columns_2 = ['id', 'question_id', 'answer', 'country', 'lat_appx_lots_of_err', 'long_appx_lots_of_err']
df = df[columns_2]

df_questions = pd.read_csv('questions_factors_IDs.csv', sep=';')

df = df.merge(df_questions, how='left', left_on='question_id', right_on='Question_ID')

columns_to_remove_2 = ['Question_ID']
df.drop(columns=columns_to_remove_2, inplace=True)

df_countries = pd.read_csv('wikipedia-iso-country-codes.csv', sep=',')

df = df.merge(df_countries, how='left', left_on='country', right_on='Alpha-2 code')

columns_to_remove_3 = ['Alpha-2 code', 'Numeric code','ISO 3166-2']

df.drop(columns=columns_to_remove_3, inplace=True)

df_happiness = pd.read_csv('happieness2016.csv', sep=',')

df = df.merge(df_happiness, how='inner', left_on='English short name lower case', right_on='Country')

columns_to_remove_4 = ['Country', 'Happiness Score', 'Lower Confidence Interval', 'Upper Confidence Interval', 'Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)', 'Freedom', 'Trust (Government Corruption)', 'Generosity', 'Dystopia Residual']

df.drop(columns=columns_to_remove_4, inplace=True)

df_hdi = pd.read_csv('HDI_Index.csv', sep=';')

df = df.merge(df_hdi, how='inner', left_on='English short name lower case', right_on='Country')

columns_to_remove_5 = ['Country', 'Human Development Index (HDI) ', 'Life expectancy at birth', 'Expected years of schooling', 'Mean years of schooling', 'Gross national income (GNI) per capita', 'GNI per capita rank minus HDI rank', 'HDI rank_1']

df.drop(columns=columns_to_remove_5, inplace=True)

df.to_csv('optimised_big_personalities_dataset.csv', index=False)