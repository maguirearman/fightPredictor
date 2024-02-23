import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the data
df = pd.read_csv('data/lightweight.csv')

# Select relevant columns
relevant_columns = ['fighter_f_name_fighter1', 'fighter_l_name_fighter1', 'fighter_f_name_fighter2',
                    'fighter_l_name_fighter2', 'f_1', 'f_2', 'knockdowns', 'total_strikes_att', 'total_strikes_succ',
                    'sig_strikes_att', 'sig_strikes_succ', 'takedown_att', 'takedown_succ',
                    'submission_att', 'reversals', 'ctrl_time', 'num_rounds', 'finish_round',
                    'finish_time', 'title_fight', 'weight_class', 'gender', 'result',
                    'result_details']

# Create feature matrix
X = df[relevant_columns]

# Display the first few rows of the feature matrix
# Export DataFrame to a CSV file
X.to_csv('data/feature_matrix_lightweight.csv', index=False)



# # Separate features (X) and target variable (y)
# X = lightweight_data.drop(['winner'], axis=1)
# y = lightweight_data['winner']
# # Perform one-hot encoding for the 'referee' column
# X_encoded = pd.get_dummies(X, columns=['referee'])

# # Split the encoded data into training and testing sets
# X_train_encoded, X_test_encoded, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# # Initialize the Random Forest classifier
# rf_classifier = RandomForestClassifier(random_state=42)

# # Train the classifier on the training data
# rf_classifier.fit(X_train_encoded, y_train)

# # Make predictions on the test data
# y_pred = rf_classifier.predict(X_test_encoded)

# # Evaluate the model's accuracy
# accuracy = accuracy_score(y_test, y_pred)
# print("Accuracy:", accuracy)
