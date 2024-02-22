import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the lightweight data
lightweight_data = pd.read_csv('data/lightweight.csv')

# Display the first few rows of the dataframe
print("First few rows of the dataset:")
print(lightweight_data.head())

# Perform exploratory data analysis (EDA)
print("\nData types of each column:")
print(lightweight_data.dtypes)

print("\nSummary statistics for numeric columns:")
print(lightweight_data.describe())

# Separate features (X) and target variable (y)
X = lightweight_data.drop(['winner'], axis=1)
y = lightweight_data['winner']

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest classifier
rf_classifier = RandomForestClassifier(random_state=42)

# Train the classifier on the training data
rf_classifier.fit(X_train, y_train)

# Make predictions on the test data
y_pred = rf_classifier.predict(X_test)

# Evaluate the model's accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# # List the columns to explore for feature selection
# columns_to_explore = [
#     'referee', 'num_rounds', 'title_fight', 'gender', 'result', 'result_details', 
#     'finish_round', 'finish_time', 'event_name', 'event_date', 'event_city', 
#     'event_state', 'event_country', 'knockdowns', 'total_strikes_att', 
#     'total_strikes_succ', 'sig_strikes_att', 'sig_strikes_succ', 'takedown_att', 
#     'takedown_succ', 'submission_att', 'reversals', 'ctrl_time'
# ]

# # Optionally, you can also include fighter-related columns for feature selection
# # fighter_columns = ['fighter_f_name_fighter1', 'fighter_l_name_fighter1', ...]

# # Explore the data to decide which features to select
# selected_features = columns_to_explore  # You can customize this based on your analysis

# # Select the features from the lightweight data
# selected_data = lightweight_data[selected_features]

# # Save the selected features to a new CSV file
# selected_data.to_csv('data/lightweight_selected_features.csv', index=False)

# print("Selected features saved to lightweight_selected_features.csv.")
