import pandas as pd

# Wczytaj plik CSV do DataFrame
df = pd.read_csv('raw_big_personalities_dataset.csv', sep='\t')

# Lista wybranych krajów do uwzględnienia
selected_countries = [
    'US', 'GB', 'CA', 'AU', 'DE', 'IN', 'PH', 'MX', 'NO', 'NL', 'SE', 'MY', 'NZ', 'ID', 'BR', 'SG', 'FR', 'IT', 'ES', 
    'PL', 'IE', 'FI', 'DK', 'RO', 'CO', 'AR', 'RU', 'ZA', 'BE', 'HK', 'PK', 'TR', 'GR', 'PT', 'CH', 'AE', 'CL', 'AT', 
    'HR', 'RS', 'VN', 'CZ', 'JP', 'PE', 'TH', 'HU', 'KR', 'IL', 'VE', 'KE', 'BG', 'EC'
]
columns_to_remove = [
    'EXT1_E', 'EXT2_E', 'EXT3_E', 'EXT4_E', 'EXT5_E', 'EXT6_E', 'EXT7_E', 
    'EXT8_E', 'EXT9_E', 'EXT10_E', 'EST1_E', 'EST2_E', 'EST3_E', 'EST4_E', 
    'EST5_E', 'EST6_E', 'EST7_E', 'EST8_E', 'EST9_E', 'EST10_E', 'AGR1_E', 
    'AGR2_E', 'AGR3_E', 'AGR4_E', 'AGR5_E', 'AGR6_E', 'AGR7_E', 'AGR8_E', 
    'AGR9_E', 'AGR10_E', 'CSN1_E', 'CSN2_E', 'CSN3_E', 'CSN4_E', 'CSN5_E', 
    'CSN6_E', 'CSN7_E', 'CSN8_E', 'CSN9_E', 'CSN10_E', 'OPN1_E', 'OPN2_E', 
    'OPN3_E', 'OPN4_E', 'OPN5_E', 'OPN6_E', 'OPN7_E', 'OPN8_E', 'OPN9_E', 
    'OPN10_E'
]
df.drop(columns=columns_to_remove, inplace=True)
# Filtrowanie danych, aby zawierały tylko wybrane kraje
df_filtered = df[(df['country'].isin(selected_countries)) & (df['IPC'] == 1)]
# Przefiltruj dane, aby zachować maksymalnie 1000 losowo wybranych wierszy dla każdego kraju
df_sampled = df_filtered.groupby('country').apply(lambda x: x.sample(285))
# Zapisz przefiltrowane dane do nowego pliku CSV
df_sampled.to_csv('cleaned_big_personalities_dataset.csv', index=False)
print("Nowy plik został utworzony z maksymalnie 285 losowymi wierszami dla każdego wybranego kraju.")