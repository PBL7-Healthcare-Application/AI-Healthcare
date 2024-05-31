# import re
# import pandas as pd
# from sklearn import preprocessing
# from sklearn.ensemble import RandomForestClassifier
# import numpy as np
# from sklearn.model_selection import train_test_split, cross_val_score
# import joblib
# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# # Load datasets
# training = pd.read_csv('D:\Project\Chatbot\\app\Data\Training.csv')
# testing = pd.read_csv('D:\Project\Chatbot\\app\Data\Testing.csv')

# # Prepare the data
# cols = training.columns[:-1]
# x = training[cols]
# y = training['prognosis']
# y1 = y

# # Grouping by prognosis to get the maximum values
# reduced_data = training.groupby(training['prognosis']).max()

# # Mapping strings to numbers
# le = preprocessing.LabelEncoder()
# le.fit(y)
# y = le.transform(y)

# # Splitting the data into training and test sets
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
# testx = testing[cols]
# testy = testing['prognosis']
# testy = le.transform(testy)

# # Training the Random Forest classifier
# clf = RandomForestClassifier(n_estimators=100, random_state=42)
# clf.fit(x_train, y_train)

# # Evaluating the model
# train_accuracy = clf.score(x_train, y_train)
# test_accuracy = clf.score(x_test, y_test)
# cross_val_accuracy = cross_val_score(clf, x, y, cv=5).mean()

# print(f"Training Accuracy: {train_accuracy}")
# print(f"Test Accuracy: {test_accuracy}")
# print(f"Cross-validation Accuracy: {cross_val_accuracy}")

# # Save the trained model using Joblib
# model_path = 'random_forest_model1.joblib'
# joblib.dump(clf, model_path)

import numpy as np
import pandas as pd
import joblib
from sklearn import preprocessing

# Load the saved model


# Function to predict disease
def predict_disease(symptoms_exp):
    model_path = 'D:\Project\Chatbot\\random_forest_model1.joblib'
    clf = joblib.load(model_path)

    # Load the data again to have the symptoms list and label encoder
    training = pd.read_csv('D:\Project\Chatbot\\app\Data\Training.csv')
    cols = training.columns[:-1]
    y = training['prognosis']

    # Mapping strings to numbers
    le = preprocessing.LabelEncoder()
    le.fit(y)
    symptoms_dict = {symptom: index for index, symptom in enumerate(cols)}
    input_vector = np.zeros(len(symptoms_dict))
    for symptom in symptoms_exp:
        if symptom in symptoms_dict:
            input_vector[symptoms_dict[symptom]] = 1
    predicted_disease_encoded = clf.predict([input_vector])[0]
    predicted_disease = le.inverse_transform([predicted_disease_encoded])
    return predicted_disease[0]

# Example symptoms
symptoms = ['cough', 'headache', 'continuous_sneezing', 'muscle_pain', 'blood_in_sputum', 'phlegm']
predicted_disease = predict_disease(symptoms)
print("Predicted disease:", predicted_disease)