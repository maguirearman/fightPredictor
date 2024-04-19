# fightPredictor
Uses ufc database to predict the winner of an mma matchup

Goal: To build a model that predicts which UFC Fighter would win in a matchup

- I started out with exploring database and preprocessing the records
- Next, I used the joined tables to properly extract feature vectors

Database: https://www.kaggle.com/datasets/remypereira/mma-dataset-2023-ufc?resource=download

archive folder is the original data sets

data set is the scraped data that i worked on


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
The Gradient Boosting Machine (GBM) classifier demonstrates the best overall performance, achieving the highest accuracy and F1-scores for both classes. Additionally, it maintains high accuracy during cross-validation, indicating robustness and generalization capability.


I used joblib to load the model into my backend python file and then used the users inputs to retrieve data and use model to predict winner


npm start: Concurrently runs flask server (flask run) and the react frontend.


# Frontend Development

Created a react application w node.js framework
Connected frontend with backend using flask routes (fighters, predict, etc.)
It is now functional and the user can select two fighters and then the winner will be predicted using my model
Using Material UI to make things pretty


Encountered a plethora of issues regarding cors errors so for now i am using this command to temporarily disable cors on chrome (just for testing)

The command to disable cors errors: open -a Google\ Chrome --args --disable-web-security --user-data-dir
