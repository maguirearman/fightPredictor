import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the merged dataset
merged_data = pd.read_csv('data/merged_data.csv')

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(merged_data.head())

# Check the data types of each column
print("\nData types of each column:")
print(merged_data.dtypes)

# Summary statistics for numeric columns
print("\nSummary statistics for numeric columns:")
print(merged_data.describe())

# Histogram of numeric columns
numeric_cols = merged_data.select_dtypes(include=['int64', 'float64']).columns
merged_data[numeric_cols].hist(figsize=(12, 10))
plt.tight_layout()
plt.show()

# Box plot of numeric columns
plt.figure(figsize=(12, 8))
sns.boxplot(data=merged_data[numeric_cols])
plt.xticks(rotation=45)
plt.show()


