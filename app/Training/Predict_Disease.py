import joblib
from sklearn import preprocessing
import pandas as pd
import numpy as np

def predict_disease_from_symptom(symptoms_exp):
    model_path = 'F:\\PBL7\AI-Healthcare\\app\model\\random_forest_model1.joblib'
    clf = joblib.load(model_path)

    # Load the data again to have the symptoms list and label encoder
    training = pd.read_csv('F:\PBL7\AI-Healthcare\\app\Data\Training.csv')
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