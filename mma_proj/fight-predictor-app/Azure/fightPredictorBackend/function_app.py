import logging
import pandas as pd
import joblib
from azure.functions import HttpRequest, HttpResponse, FunctionApp
from sklearn.impute import SimpleImputer

app = FunctionApp()

# Load the trained model
model = joblib.load('trained_model.pkl')

# Define methods to load and process data
def load_and_prepare_data():
    # Load and merge data from CSV files
    ufc_events = pd.read_csv('archive/ufc_event_data.csv')
    ufc_fights = pd.read_csv('archive/ufc_fight_data.csv')
    ufc_fight_stats = pd.read_csv('archive/ufc_fight_stat_data.csv')
    ufc_fighters = pd.read_csv('archive/ufc_fighter_data.csv')
    
    merged_data = pd.merge(ufc_fights, ufc_events, on='event_id')
    merged_data = pd.merge(merged_data, ufc_fighters, left_on='f_1', right_on='fighter_id', suffixes=('_fighter1', '_fighter2'))
    merged_data = pd.merge(merged_data, ufc_fighters, left_on='f_2', right_on='fighter_id', suffixes=('_fighter2', '_fighter1'))
    
    ufc_fight_stats_fighter1 = pd.merge(ufc_fight_stats, ufc_fighters, left_on='fighter_id', right_on='fighter_id', suffixes=('_fighter1', '_fighter2'))
    ufc_fight_stats_fighter2 = pd.merge(ufc_fight_stats, ufc_fighters, left_on='fighter_id', right_on='fighter_id', suffixes=('_fighter2', '_fighter1'))
    
    merged_data = pd.merge(merged_data, ufc_fight_stats_fighter1, left_on=['fight_id', 'f_1'], right_on=['fight_id', 'fighter_id'])
    merged_data = pd.merge(merged_data, ufc_fight_stats_fighter2, left_on=['fight_id', 'f_2'], right_on=['fight_id', 'fighter_id'])
    
    merged_data.drop(['event_id', 'fighter_id_fighter1', 'fighter_id_fighter2'], axis=1, inplace=True)
    
    # Process control time columns
    merged_data['ctrl_time_x'] = merged_data['ctrl_time_x'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]) if pd.notnull(x) and x != '--' else 0)
    merged_data['ctrl_time_y'] = merged_data['ctrl_time_y'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]) if pd.notnull(x) and x != '--' else 0)
    
    # Drop non-numeric columns
    non_numeric_columns = ['referee', 'event_name', 'event_date', 'event_city', 'event_state', 'event_country', 'fight_url', 'fighter_url_fighter1', 'fighter_url_fighter2', 'event_url', 'fight_url_x', 'fight_url_y', 'fighter_url_x', 'fighter_url_y']
    merged_data = merged_data.drop(columns=non_numeric_columns)
    
    # Impute NaN values for numeric columns
    numeric_columns = merged_data.select_dtypes(include='number').columns
    imputer = SimpleImputer(strategy='mean')
    merged_data[numeric_columns] = imputer.fit_transform(merged_data[numeric_columns])
    
    # Replace winner IDs with binary values
    merged_data['winner'] = merged_data.apply(lambda row: 0 if row['winner'] == row['f_1'] else 1, axis=1)
    
    unique_columns = ['fight_id', 'f_1', 'f_2']
    merged_data.drop_duplicates(subset=unique_columns, inplace=True)
    
    return merged_data

def extract_fighter_ids(fighter1_name, fighter2_name):
    fighter_ids = []
    with open('archive/ufc_fighter_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['fighter_f_name'] + ' ' + row['fighter_l_name'] == fighter1_name:
                fighter_ids.append(row['fighter_id'])
            elif row['fighter_f_name'] + ' ' + row['fighter_l_name'] == fighter2_name:
                fighter_ids.append(row['fighter_id'])
    return fighter_ids

def extract_features_for_fighters(fighter1_name, fighter2_name, merged_data):
    fighter1_id, fighter2_id = extract_fighter_ids(fighter1_name, fighter2_name)
    
    # Aggregate stats for each fighter
    fighter1_stats = aggregate_fighter_stats(fighter1_id, merged_data)
    fighter2_stats = aggregate_fighter_stats(fighter2_id, merged_data)
    
    # Prepare the final feature dictionary
    fighter1_features = {f"{key}_x": value for key, value in fighter1_stats.items()}
    fighter2_features = {f"{key}_y": value for key, value in fighter2_stats.items()}
    combined_features = {**fighter1_features, **fighter2_features}
    
    # Convert to DataFrame
    features_df = pd.DataFrame([combined_features])
    
    return features_df

@app.route(route="fighterBackend", auth_level=func.AuthLevel.FUNCTION)
def fighterBackend(req: HttpRequest) -> HttpResponse:
    logging.info('Processing a request in fighterBackend function.')
    
    try:
        data = req.get_json()
    except ValueError:
        return HttpResponse("Invalid JSON in request body.", status_code=400)
    
    fighter1 = data.get('fighter1')
    fighter2 = data.get('fighter2')

    if not fighter1 or not fighter2:
        return HttpResponse("Missing fighter1 or fighter2 in request.", status_code=400)

    merged_data = load_and_prepare_data()
    features = extract_features_for_fighters(fighter1, fighter2, merged_data)
    
    # Predict the outcome probabilities
    probabilities = model.predict_proba(features)[0]
    fighter1_probability = probabilities[0]
    fighter2_probability = probabilities[1]

    # Determine the predicted winner
    predicted_winner_name = fighter1 if fighter1_probability > fighter2_probability else fighter2

    # Prepare the response
    response = {
        "fighter1": fighter1,
        "fighter2": fighter2,
        "fighter1_probability": fighter1_probability,
        "fighter2_probability": fighter2_probability,
        "predicted_winner": predicted_winner_name
    }

    return HttpResponse(json.dumps(response), status_code=200, mimetype="application/json")
