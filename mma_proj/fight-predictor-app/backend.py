import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import csv
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report


app = Flask(__name__)
CORS(app)

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
    #print("Selected Features:\n", selected_features)


    # Verify if 'winner' is in selected features
    if 'winner' in selected_features:
        
        return merged_data[selected_features]
    else:
        print("'winner' column not found in selected features.")
        return None
    

def train_and_evaluate_gbm(X, y, n_estimators=100, max_depth=3, learning_rate=0.1, n_splits=5):
    # Initialize Gradient Boosting Classifier
    gbm = GradientBoostingClassifier(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate, random_state=42)
    
    # Initialize cross-validation
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    # Perform cross-validation
    cv_scores = cross_val_score(gbm, X, y, cv=cv, scoring='accuracy')
    
    # Fit the model on the entire dataset
    gbm.fit(X, y)
    
    # Make predictions
    y_pred = gbm.predict(X)
    
    # Print cross-validation results
    print("GBM Booster Cross-Validation Accuracy Scores:", cv_scores)
    print("GBM Booster Mean Accuracy:", cv_scores.mean())
    
    # Generate classification report on the entire dataset
    print("\nGBM Booster Classification Report:")
    print(classification_report(y, y_pred))
    
    # Return the trained model
    return gbm

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

# Define a method to check if a fighter belongs to the specified weight class
def check_fighter_weight_class(weight_class, fighter_name):
    with open('archive/ufc_fight_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['weight_class'] == weight_class and (row['fighter1'] == fighter_name or row['fighter2'] == fighter_name):
                return True
    return False

# Define a method to extract fighter IDs based on their names and weight class
def extract_fighter_ids(weight_class, fighter1_name, fighter2_name):
    fighter_ids = []
    with open('archive/ufc_fighter_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['weight_class'] == weight_class:
                if row['fighter_f_name'] + ' ' + row['fighter_l_name'] == fighter1_name:
                    fighter_ids.append(row['fighter_id'])
                elif row['fighter_f_name'] + ' ' + row['fighter_l_name'] == fighter2_name:
                    fighter_ids.append(row['fighter_id'])
    return fighter_ids


@app.route('/fighters', methods=['GET'])
def get_fighters():
    if request.method == 'OPTIONS':
        # Respond to preflight request
        response = make_response(jsonify({'message': 'Preflight request accepted.'}), 200)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        return response


    # Get the weight class from the query parameters
    weight_class = request.args.get('weightClass')


    fighters = get_fighter_names()
    response = jsonify(fighters)
    return response



@app.route('/predict', methods=['OPTIONS', 'POST'])
def predict_fight():
    if request.method == 'OPTIONS':
        # Respond to preflight request
        response = jsonify({'message': 'Preflight request accepted.'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    if request.method == 'POST':
        # Receive selected parameters from the frontend
        data = request.json
        weight_class = data['weightClass']
        print(weight_class)
        fighter1 = data['fighter1']
        fighter2 = data['fighter2']
        # fighter_ids = extract_fighter_ids(weight_class, fighter1, fighter2)
        # print(fighter_ids)

    # Check if fighters belong to the specified weight class
    if not check_fighter_weight_class(weight_class, fighter1) or not check_fighter_weight_class(weight_class, fighter2):
        return jsonify({'error': 'One or more fighters do not belong to the specified weight class.'}), 400
    
    # Extract fighter IDs
    fighter_ids = extract_fighter_ids(weight_class, fighter1, fighter2)
    print(fighter_ids)
    
    # Predict the outcome of the fight
    #predicted_winner = predict_fight_outcome(weight_class, fighter1, fighter2)
    
    #return jsonify({'predicted_winner': predicted_winner})

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
        gbm = train_and_evaluate_gbm(selected_data.drop(columns=['winner']), selected_data['winner'])

        # Dummy prediction using placeholders
        predicted_winner = 'Fighter 1' if weight_class == 'Flyweight' else 'Fighter 2'

        response = jsonify({'predicted_winner': predicted_winner})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

if __name__ == '__main__':
    app.run(debug=True)
