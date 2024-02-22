import pandas as pd

# Read CSV files into DataFrames
ufc_events = pd.read_csv('archive/ufc_event_data.csv')
ufc_fights = pd.read_csv('archive/ufc_fight_data.csv')
ufc_fight_stats = pd.read_csv('archive/ufc_fight_stat_data.csv')
ufc_fighters = pd.read_csv('archive/ufc_fighter_data.csv')

# Join ufc_events with ufc_fights on event_id
merged_data = pd.merge(ufc_fights, ufc_events, on='event_id')

# Join with ufc_fight_stats on fight_id
merged_data = pd.merge(merged_data, ufc_fight_stats, on='fight_id')

# Join with ufc_fighters twice on f_1 and f_2
merged_data = pd.merge(merged_data, ufc_fighters, left_on='f_1', right_on='fighter_id', suffixes=('_fighter1', '_fighter2'))
merged_data = pd.merge(merged_data, ufc_fighters, left_on='f_2', right_on='fighter_id', suffixes=('_fighter2', '_fighter1'))



# Drop duplicate columns after merging
merged_data.drop(['event_id', 'fighter_id_fighter1', 'fighter_id_fighter2'], axis=1, inplace=True)

# Define criteria for uniqueness based on selected columns
unique_columns = ['fight_id', 'event_name', 'event_date', 'event_city', 'event_state', 'event_country', 'f_1', 'f_2']

# Drop duplicate rows based on unique_columns
merged_data.drop_duplicates(subset=unique_columns, inplace=True)

# Save the DataFrame to a CSV file
merged_data.to_csv('data/merged_data.csv', index=False)

# Now you can perform further data processing and feature extraction as needed
