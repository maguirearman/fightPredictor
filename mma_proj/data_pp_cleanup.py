import pandas as pd

# Read CSV files into DataFrames
ufc_events = pd.read_csv('archive/ufc_event_data.csv')
ufc_fights = pd.read_csv('archive/ufc_fight_data.csv')
ufc_fight_stats = pd.read_csv('archive/ufc_fight_stat_data.csv')
ufc_fighters = pd.read_csv('archive/ufc_fighter_data.csv')

# Join ufc_events with ufc_fights on event_id
merged_data = pd.merge(ufc_fights, ufc_events, on='event_id')


# Join with ufc_fighters twice on f_1 and f_2
merged_data = pd.merge(merged_data, ufc_fighters, left_on='f_1', right_on='fighter_id', suffixes=('_fighter1', '_fighter2'))
merged_data = pd.merge(merged_data, ufc_fighters, left_on='f_2', right_on='fighter_id', suffixes=('_fighter2', '_fighter1'))

# Merge ufc_fight_stats with ufc_fighters to get fighter information
ufc_fight_stats_fighter1 = pd.merge(ufc_fight_stats, ufc_fighters, left_on='fighter_id', right_on='fighter_id', suffixes=('_fighter1', '_fighter2'))
ufc_fight_stats_fighter2 = pd.merge(ufc_fight_stats, ufc_fighters, left_on='fighter_id', right_on='fighter_id', suffixes=('_fighter2', '_fighter1'))

# Merge with merged_data using fight_id and fighter_id for each fighter
merged_data = pd.merge(merged_data, ufc_fight_stats_fighter1, left_on=['fight_id', 'f_1'], right_on=['fight_id', 'fighter_id'])
merged_data = pd.merge(merged_data, ufc_fight_stats_fighter2, left_on=['fight_id', 'f_2'], right_on=['fight_id', 'fighter_id'])
# Drop duplicate columns after merging
merged_data.drop(['event_id', 'fighter_id_fighter1', 'fighter_id_fighter2'], axis=1, inplace=True)

# Define criteria for uniqueness based on selected columns
unique_columns = ['fight_id', 'event_name', 'event_date', 'event_city', 'event_state', 'event_country', 'f_1', 'f_2']

# Drop duplicate rows based on unique_columns
merged_data.drop_duplicates(subset=unique_columns, inplace=True)

# Drop unwanted columns
columns_to_drop = ['referee', 'title_fight', 'event_name', 'event_date', 'event_city', 'event_state', 'event_country', 'fight_url', 'fighter_url_fighter1', 'fighter_url_fighter2', 'event_url', 'fight_url_x', 'fight_url_y', 'fighter_url_x', 'fighter_url_y']
merged_data.drop(columns_to_drop, axis=1, inplace=True)
column_order = ['fight_id', 
                'f_1', 
                'fighter_f_name_x', 
                'fighter_l_name_x', 
                'fighter_nickname_x', 
                'f_2', 
                'fighter_f_name_y', 
                'fighter_l_name_y', 
                'fighter_nickname_y', 
                'winner', 
                'num_rounds', 
                'weight_class', 
                'gender', 
                'result', 
                'result_details', 
                'finish_round', 
                'finish_time',
                'fighter_height_cm_x', 
                'fighter_weight_lbs_x',
                'fighter_reach_cm_x', 
                'fighter_stance_x', 
                'fighter_dob_x', 
                'fighter_w_x', 
                'fighter_l_x', 
                'fighter_d_x',
                'fighter_nc_dq_x', 
                'fight_stat_id_x', 
                'fighter_id_x', 
                'knockdowns_x', 
                'total_strikes_att_x', 
                'total_strikes_succ_x', 
                'sig_strikes_att_x',
                'sig_strikes_succ_x', 
                'takedown_att_x', 
                'takedown_succ_x', 
                'submission_att_x', 
                'reversals_x', 
                'ctrl_time_x', 
                'fighter_f_name_y', 
                'fighter_l_name_y',
                'fighter_nickname_y', 
                'fighter_height_cm_y', 
                'fighter_weight_lbs_y', 
                'fighter_reach_cm_y', 
                'fighter_stance_y', 
                'fighter_dob_y',
                'fighter_w_y', 
                'fighter_l_y', 
                'fighter_d_y', 
                'fighter_nc_dq_y', 
                'fight_stat_id_y', 
                'fighter_id_y', 
                'knockdowns_y', 
                'total_strikes_att_y', 
                'total_strikes_succ_y',
                'sig_strikes_att_y', 
                'sig_strikes_succ_y', 
                'takedown_att_y', 
                'takedown_succ_y', 
                'submission_att_y', 
                'reversals_y', 
                'ctrl_time_y']

merged_data = merged_data[column_order]


# Save the DataFrame to a CSV file
merged_data.to_csv('data/merged_data.csv', index=False)