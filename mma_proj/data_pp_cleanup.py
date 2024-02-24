import pandas as pd

def read_data():
    ufc_events = pd.read_csv('archive/ufc_event_data.csv')
    ufc_fights = pd.read_csv('archive/ufc_fight_data.csv')
    ufc_fight_stats = pd.read_csv('archive/ufc_fight_stat_data.csv')
    ufc_fighters = pd.read_csv('archive/ufc_fighter_data.csv')
    return ufc_events, ufc_fights, ufc_fight_stats, ufc_fighters

def merge_data(ufc_fights, ufc_events, ufc_fighters, ufc_fight_stats):
    merged_data = pd.merge(ufc_fights, ufc_events, on='event_id')
    merged_data = pd.merge(merged_data, ufc_fighters, left_on='f_1', right_on='fighter_id', suffixes=('_fighter1', '_fighter2'))
    merged_data = pd.merge(merged_data, ufc_fighters, left_on='f_2', right_on='fighter_id', suffixes=('_fighter2', '_fighter1'))
    ufc_fight_stats_fighter1 = pd.merge(ufc_fight_stats, ufc_fighters, left_on='fighter_id', right_on='fighter_id', suffixes=('_fighter1', '_fighter2'))
    ufc_fight_stats_fighter2 = pd.merge(ufc_fight_stats, ufc_fighters, left_on='fighter_id', right_on='fighter_id', suffixes=('_fighter2', '_fighter1'))
    merged_data = pd.merge(merged_data, ufc_fight_stats_fighter1, left_on=['fight_id', 'f_1'], right_on=['fight_id', 'fighter_id'])
    merged_data = pd.merge(merged_data, ufc_fight_stats_fighter2, left_on=['fight_id', 'f_2'], right_on=['fight_id', 'fighter_id'])
    merged_data.drop(['event_id', 'fighter_id_fighter1', 'fighter_id_fighter2'], axis=1, inplace=True)
    return merged_data

def clean_data(merged_data):
    unique_columns = ['fight_id', 'event_name', 'event_date', 'event_city', 'event_state', 'event_country', 'f_1', 'f_2']
    merged_data.drop_duplicates(subset=unique_columns, inplace=True)
    columns_to_drop = ['referee', 'title_fight', 'event_name', 'event_date', 'event_city', 'event_state', 'event_country', 'fight_url', 'fighter_url_fighter1', 'fighter_url_fighter2', 'event_url', 'fight_url_x', 'fight_url_y', 'fighter_url_x', 'fighter_url_y']
    merged_data.drop(columns_to_drop, axis=1, inplace=True)
    return merged_data

def feature_selection(merged_data):
    # Perform feature selection here
    # You can use any of the techniques mentioned earlier
    
     # Example: Select features based on domain knowledge
    selected_features = [
    'fighter_id_x', 'knockdowns_x', 'total_strikes_att_x', 'total_strikes_succ_x', 
    'sig_strikes_att_x', 'sig_strikes_succ_x', 'takedown_att_x', 'takedown_succ_x', 
    'submission_att_x', 'reversals_x', 'ctrl_time_x', 'fighter_id_y', 'knockdowns_y', 
    'total_strikes_att_y', 'total_strikes_succ_y', 'sig_strikes_att_y', 
    'sig_strikes_succ_y', 'takedown_att_y', 'takedown_succ_y', 
    'submission_att_y', 'reversals_y', 'ctrl_time_y', 'winner']
    # Inspect the selected features
    print("Selected Features:\n", selected_features)


    # Verify if 'winner' is in selected features
    if 'winner' in selected_features:
        # Verify correlation with the target variable
        corr_with_target = merged_data[selected_features].corr()['winner'].abs().sort_values(ascending=False)
        print("\nCorrelation with Target:\n", corr_with_target)
        
        return merged_data[selected_features]
    else:
        print("'winner' column not found in selected features.")
        return None


def main():
    # Read data
    ufc_events, ufc_fights, ufc_fight_stats, ufc_fighters = read_data()
    
    # Merge data
    merged_data = merge_data(ufc_fights, ufc_events, ufc_fighters, ufc_fight_stats)
    
    # Clean data
    cleaned_data = clean_data(merged_data)
    
    # Perform feature selection
    selected_data = feature_selection(cleaned_data)
    
    # If selected_data is not None, save it to CSV
    if selected_data is not None:
        selected_data.to_csv('data/selected_data.csv', index=False)
    else:
        print("No features selected. Nothing saved to CSV.")

if __name__ == "__main__":
    main()
    