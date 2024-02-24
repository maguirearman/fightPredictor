import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.impute import SimpleImputer

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
    print("Selected Features:\n", selected_features)


    # Verify if 'winner' is in selected features
    if 'winner' in selected_features:
        # Verify correlation with the target variable
        corr_with_target = merged_data[selected_features].corr(numeric_only=True)['winner'].abs().sort_values(ascending=False)
        print("\nCorrelation with Target:\n", corr_with_target)
        
        return merged_data[selected_features]
    else:
        print("'winner' column not found in selected features.")
        return None

def train_logistic_regression(data):
    # Separate features and target variable
    X = data.drop(columns=['winner'])
    y = data['winner']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    
    # Initialize and train the logistic regression model
    model = LogisticRegression(max_iter=1000)  # Increase max_iter if needed
    model.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    return model, accuracy, report


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
    #     model, accuracy, report = train_logistic_regression(selected_data)
    #     print("Accuracy: ", accuracy)
    #     print("Classification Report:\n", report)
        selected_data.to_csv('data/selected_data.csv', index=False)
    else:
        print("No features selected. Nothing saved to CSV.")

if __name__ == "__main__":
    main()
    