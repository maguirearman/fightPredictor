import logging
import pandas as pd
import joblib
import json
import csv
import azure.functions as func  # Import the Azure Functions library
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

def aggregate_fighter_stats(fighter_id, ufc_fight_data):
    # Initialize dictionaries to hold the sums of each stat and the count of fights for averaging
    stats_sum = {}
    fight_count = 0
    fighter_id_float = float(fighter_id)

    # Define the stats we're interested in aggregating
    stats_of_interest = ['fighter_id','knockdowns', 'total_strikes_att', 'total_strikes_succ',
                         'sig_strikes_att', 'sig_strikes_succ', 'takedown_att',
                         'takedown_succ', 'submission_att', 'reversals', 'ctrl_time']

    for _, row in ufc_fight_data.iterrows():
        # Determine if the fighter is f_1 or f_2 in this fight
        if row['f_1'] == fighter_id_float:
            prefix = 'x'
        elif row['f_2'] == fighter_id_float:
            prefix = 'y'
        else:
            continue  # This fight does not involve the fighter in question
        
        # Aggregate stats for the fighter
        for stat in stats_of_interest:
            key = f'{stat}_{prefix}'  # Construct the key name for this stat
            # Special handling for 'ctrl_time' due to its string format 'MM:SS'
            if stat == 'ctrl_time' and isinstance(row.get(key, '0:0'), str):
                minutes, seconds = map(int, row.get(key, '0:0').split(':'))
                total_seconds = minutes * 60 + seconds
                stats_sum[stat] = stats_sum.get(stat, 0) + total_seconds
            else:
                # Directly aggregate other stats
                stats_sum[stat] = stats_sum.get(stat, 0) + row.get(key, 0)
        
        fight_count += 1

    # Calculate average stats
    if fight_count == 0:
        raise ValueError(f"No fight data found for fighter ID {fighter_id}")
    
    avg_stats = {stat: total / fight_count for stat, total in stats_sum.items()}
    
    return avg_stats

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


# Function returns a list of the names of all fighters
def get_fighter_names():
    fighter_names = []
    names_count = {}
    with open('archive/ufc_fighter_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fighter_name = f"{row['fighter_f_name']} {row['fighter_l_name']}"
            if fighter_name in fighter_names:
                # If the name already exists, add the middle name or nickname
                nickname = row.get('fighter_nickname', '')
                if nickname:
                    fighter_name += f" '{nickname}'"
                # If both middle name and nickname are missing, add a unique identifier
                else:
                    if fighter_name in names_count:
                        names_count[fighter_name] += 1
                        fighter_name += f" {names_count[fighter_name]}"
                    else:
                        names_count[fighter_name] = 1
            fighter_names.append(fighter_name)
    return fighter_names

@app.function_name(name="getFighters")
@app.route(route="fighters", auth_level=func.AuthLevel.FUNCTION, methods=["GET", "OPTIONS"])
def get_fighters(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == 'OPTIONS':
        # Respond to preflight request
        response = func.HttpResponse(
            json.dumps({'message': 'Preflight request accepted.'}),
            status_code=200,
            mimetype="application/json"
        )
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        return response
    
    fighters = get_fighter_names()  # Make sure you have this function defined somewhere
    response = func.HttpResponse(
        json.dumps(fighters),
        status_code=200,
        mimetype="application/json"
    )
    return response

@app.function_name(name="fighterBackend")
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
