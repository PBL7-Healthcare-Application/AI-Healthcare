from flask import Blueprint, jsonify, request
from .Training.Predict_Disease import predict_disease_from_symptom
import pickle
import xgboost as xgb
main = Blueprint('main', __name__)





@main.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = data['symptoms']
    
    
    result = predict_disease_from_symptom(features)
    response = {
        'prediction': float(result[0])
    }
    
    return jsonify(response)