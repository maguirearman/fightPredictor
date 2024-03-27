import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import joblib

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

    # Verify if 'winner' is in selected features
    if 'winner' in selected_features:
        
        return merged_data[selected_features]
    else:
        print("'winner' column not found in selected features.")
        return None
    
def train_and_evaluate_model(X, y, n_estimators=100, max_depth=3, learning_rate=0.1, n_splits=5):
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

# Load and prepare the data
merged_data = load_and_prepare_data()
merged_data_w_features = feature_selection(merged_data)
gbm = train_and_evaluate_model(merged_data_w_features.drop(columns=['winner']), merged_data_w_features['winner'])

# Save the trained model to a file
joblib.dump(gbm, 'trained_model.pkl')
