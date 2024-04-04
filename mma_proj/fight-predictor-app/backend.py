import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import csv
from flask_cors import cross_origin
import joblib


# Apply CORS globally to all routes, the simplest solution
app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load('trained_model.pkl')

def read_data():
    ufc_events = pd.read_csv('archive/ufc_event_data.csv')
    ufc_fights = pd.read_csv('archive/ufc_fight_data.csv')
    ufc_fight_stats = pd.read_csv('archive/ufc_fight_stat_data.csv')
    ufc_fighters = pd.read_csv('archive/ufc_fighter_data.csv')
    return ufc_events, ufc_fights, ufc_fight_stats, ufc_fighters

def load_and_prepare_data():
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

    # Convert control time columns to total seconds
    merged_data['ctrl_time_x'] = merged_data['ctrl_time_x'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]) if pd.notnull(x) and x != '--' else 0)
    merged_data['ctrl_time_y'] = merged_data['ctrl_time_y'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]) if pd.notnull(x) and x != '--' else 0)
    
    # Drop non-numeric columns
    non_numeric_columns = ['referee', 'event_name', 'event_date', 'event_city', 'event_state', 'event_country', 'fight_url', 'fighter_url_fighter1', 'fighter_url_fighter2', 'event_url', 'fight_url_x', 'fight_url_y', 'fighter_url_x', 'fighter_url_y']
    merged_data = merged_data.drop(columns=non_numeric_columns)
    
    # Impute NaN values for numeric columns
    numeric_columns = merged_data.select_dtypes(include='number').columns
    imputer = SimpleImputer(strategy='mean')
    merged_data[numeric_columns] = imputer.fit_transform(merged_data[numeric_columns])
    
    # Replace winner IDs with 'x' or 'y'
    merged_data['winner'] = merged_data.apply(lambda row: 0 if row['winner'] == row['f_1'] else 1, axis=1)
    
    unique_columns = ['fight_id', 'f_1', 'f_2']
    merged_data.drop_duplicates(subset=unique_columns, inplace=True)
    
    return merged_data

def clean_data(merged_data):
    # Convert control time columns to total seconds
    merged_data['ctrl_time_x'] = merged_data['ctrl_time_x'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]) if pd.notnull(x) and x != '--' else 0)
    merged_data['ctrl_time_y'] = merged_data['ctrl_time_y'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]) if pd.notnull(x) and x != '--' else 0)
    
    # Drop non-numeric columns
    non_numeric_columns = ['referee', 'event_name', 'event_date', 'event_city', 'event_state', 'event_country', 'fight_url', 'fighter_url_fighter1', 'fighter_url_fighter2', 'event_url', 'fight_url_x', 'fight_url_y', 'fighter_url_x', 'fighter_url_y']
    merged_data = merged_data.drop(columns=non_numeric_columns)
    
    # Impute NaN values for numeric columns
    numeric_columns = merged_data.select_dtypes(include='number').columns
    imputer = SimpleImputer(strategy='mean')
    merged_data[numeric_columns] = imputer.fit_transform(merged_data[numeric_columns])
    
    # Replace winner IDs with 'x' or 'y'
    merged_data['winner'] = merged_data.apply(lambda row: 0 if row['winner'] == row['f_1'] else 1, axis=1)
    
    unique_columns = ['fight_id', 'f_1', 'f_2']
    merged_data.drop_duplicates(subset=unique_columns, inplace=True)
    
    return merged_data


# Use your machine learning model to predict the outcome of the fight
def predict_fight_outcome(weight_class, fighter1_name, fighter2_name):
    # Example: Use your trained machine learning model to predict the outcome
    # Replace this with your actual prediction logic
    predicted_winner = 'Fighter 1' if weight_class == 'Flyweight' else 'Fighter 2'
    return predicted_winner


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

def check_fighter_weight_class(weight_class, fighter_id):
    # Convert the fighter ID to a string and append '.0'
    fighter_id_str = str(fighter_id) + '.0'
    with open('archive/ufc_fight_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if the weight class matches and if the fighter ID matches either f_1 or f_2
            if row['weight_class'] == weight_class and (row['f_1'] == fighter_id_str or row['f_2'] == fighter_id_str):
                return True
    return False


# Define a method to extract fighter IDs based on their names and weight class
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


@app.route('/fighters', methods=['GET', 'OPTIONS'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type'], methods=['GET', 'OPTIONS'])
def get_fighters():
    if request.method == 'OPTIONS':
        # Respond to preflight request
        response = make_response(jsonify({'message': 'Preflight request accepted.'}), 200)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        return response
    
    fighters = get_fighter_names()
    response = jsonify(fighters)
    return response

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
    # Assuming extract_fighter_ids is implemented elsewhere and returns correct IDs
    fighter1_id, fighter2_id = extract_fighter_ids(fighter1_name, fighter2_name)

    # Aggregate stats for each fighter
    fighter1_stats = aggregate_fighter_stats(fighter1_id, merged_data)
    fighter2_stats = aggregate_fighter_stats(fighter2_id, merged_data)

    # Add suffixes and prepare the final feature dictionary
    fighter1_features = {f"{key}_x": value for key, value in fighter1_stats.items()}
    fighter2_features = {f"{key}_y": value for key, value in fighter2_stats.items()}


    print(fighter1_features)
    print(fighter2_features)
    # Ensure the order of features matches your requirement
    ordered_features = {**fighter1_features, **fighter2_features}
    
    # If you need to strictly control the order, you might explicitly list them:
    feature_order = [
        'fighter_id_x', 'knockdowns_x', 'total_strikes_att_x', 'total_strikes_succ_x', 
        'sig_strikes_att_x', 'sig_strikes_succ_x', 'takedown_att_x', 'takedown_succ_x', 
        'submission_att_x', 'reversals_x', 'ctrl_time_x', 'fighter_id_y', 'knockdowns_y', 
        'total_strikes_att_y', 'total_strikes_succ_y', 'sig_strikes_att_y', 
        'sig_strikes_succ_y', 'takedown_att_y', 'takedown_succ_y', 
        'submission_att_y', 'reversals_y', 'ctrl_time_y'
    ]

    # Use the ordered list to create a structured dictionary
    #structured_features = {feature: ordered_features[feature] for feature in feature_order}

    # Convert to DataFrame if required by your model
    features_df = pd.DataFrame([fighter1_features, fighter2_features])

    return features_df




@app.route('/predict', methods=['POST', 'OPTIONS'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type'], methods=['POST', 'OPTIONS'])
def predict_fight():
    if request.method == 'OPTIONS':
        # Respond to preflight request
        response = jsonify({'message': 'Preflight request accepted.'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    if request.method == 'POST':
        merged_data = load_and_prepare_data()
        # Receive selected parameters from the frontend
        data = request.json
        weight_class = data['weightClass']
        print(weight_class)
        fighter1 = data['fighter1']
        fighter2 = data['fighter2']
        print(fighter1)
        print(fighter2)
        # Extract fighter IDs
        fighter_ids = extract_fighter_ids(fighter1, fighter2)
        print(fighter_ids)
        # Check if fighters belong to the specified weight class
        for fighter_id in fighter_ids:
            if not check_fighter_weight_class(weight_class, fighter_id):
                error_message = f'Fighter with ID {fighter_id} does not belong to the specified weight class.'
                print(error_message)
        # Extract features for the fighters
        features = extract_features_for_fighters(fighter1, fighter2, merged_data)
        print(features)
        # Predict the outcome
        #prediction = model.predict(features)
        # Interpret the prediction (adjust according to your model's output)
        # predicted_winner = 'Fighter 1' if prediction[0] == 0 else 'Fighter 2'
    
        # print("predicted_winner: "+ predicted_winner)

            # Your logic here
        prediction = 1

        print(prediction)

    
        # Ensure a return statement that sends a response back to the client
        return jsonify({'prediction': prediction}), 200
    
        
        




if __name__ == '__main__':
    app.run(debug=True)
