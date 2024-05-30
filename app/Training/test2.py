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

def sec_predict(symptoms_exp):
    df = pd.read_csv('E:\Code_Project\PBL7\AI-Healthcare\\app\Data\Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
      input_vector[[symptoms_dict[item]]] = 1

    return rf_clf.predict([input_vector])

symptoms = ["muscle_wasting", "patches_in_throat", "high_fever"]
predicted_disease = sec_predict(symptoms)
print("Predicted disease:", predicted_disease)