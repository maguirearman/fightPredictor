# MMA Fight Predictor

A web application that predicts the winner of an MMA matchup using data from the UFC.

# Goal

Develop a model that accurately predicts which UFC fighter would win in a matchup.

# Approach

Data Exploration and Preprocessing:
 - Examined and cleaned the UFC database, joining tables to extract relevant feature vectors.
 - Data source: Kaggle MMA Dataset 2023 (https://www.kaggle.com/datasets/remypereira/mma-dataset-2023-ufc?resource=download)
 - The archive folder contains the original datasets, while the data set folder includes the scraped data that was processed.

Model Development
- Created multiple models to compare predictive performance

# MMA Fight Outcome Prediction
Model Performance Summary
- Random Forest Classifier
Accuracy: 86.37%
Precision (0): 89%
Precision (1): 81%
Recall (0): 91%
Recall (1): 77%
F1-score (0): 90%
F1-score (1): 79%
- Gradient Boosting Machine (GBM) Classifier
Accuracy: 88%
Precision (0): 92%
Precision (1): 89%
Recall (0): 95%
Recall (1): 83%
F1-score (0): 93%
F1-score (1): 86%
Accuracy (Mean): 88.41%
- Neural Network
Accuracy: 85.67%
Precision (0): 88%
Precision (1): 80%
Recall (0): 91%
Recall (1): 75%
F1-score (0): 89%
F1-score (1): 78%
- Support Vector Machine (SVM) Classifier
Accuracy: 81.29%
Precision (0): 84%
Precision (1): 75%
Recall (0): 90%
Recall (1): 65%
F1-score (0): 86%
F1-score (1): 70%
- Stochastic Gradient Descent (SGD) Classifier
Accuracy: 73%
Precision (0): 71%
Precision (1): 90%
Recall (0): 99%
Recall (1): 24%
F1-score (0): 83%
F1-score (1): 37%
Accuracy (Mean): 78.25%
- Conclusion
The Gradient Boosting Machine (GBM) classifier demonstrated the best overall performance, with the highest accuracy and F1 scores for both classes. It also maintains high cross-validation accuracy, indicating robustness.

# Model Deployment

Backend Integration: 
- The predictive model is loaded into the Python backend using joblib.
- User inputs are utilized to fetch relevant data and generate predictions.

Starting the Application: 
- Run the app with npm start to concurrently start the Flask server (flask run) and the React frontend.


# Frontend Development

1. Developed a React application based on the Node.js framework.
2. Connected the frontend and backend using Flask routes (e.g., /fighters, /predict).
3. The application enables users to select two fighters and predict the winner based on the trained model.
4. Utilized Material UI to enhance the interface's visual appeal.


Note: During testing, encountered CORS errors, which can be temporarily bypassed by disabling web security in Chrome. Run this command:
open -a Google\ Chrome --args --disable-web-security --user-data-dir

# Publishing website

I used Vercel to publish the website: https://fight-predictor.vercel.app/
