import csv
import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from io import StringIO
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pickle
import joblib
from sklearn import preprocessing

def sec_predict(symptoms_exp):
    
    model_path = 'D:\Project\Chatbot\\app\model\\random_forest_model.pkl'
    clf = joblib.load(model_path)

    training = pd.read_csv('/content/drive/MyDrive/PBL7/Training.csv')
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
    


symptoms = ["muscle_wasting", "patches_in_throat", "high_fever"]
predicted_disease = sec_predict(symptoms)
print("Predicted disease:", predicted_disease)