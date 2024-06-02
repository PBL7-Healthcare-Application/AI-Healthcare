from flask import Blueprint, jsonify, request
from .Training.TraininggIntent import predict_intent
from .Intent.Response.Response import get_response 
from .Training.Predict_Disease import contains_disease_info ,find_disease_description ,find_disease_advice,find_symptoms_from_disease
import pickle
import xgboost as xgb
main = Blueprint('main', __name__)


@main.route('/chatbot', methods=['POST'])
def predict():
   
    data = request.json
    message= data['message']
    
    
    result = predict_intent(message)
    res= ''
    if(result == 'greeting'):
        res = get_response(result)
    if(result == 'farewell'):
        res = get_response(result)
    #=================================================
    if(result == 'ask_disease_info'):
        disease = contains_disease_info(message)
        if(disease):
            res = find_disease_description(disease)
        else:
            res = get_response(result)
    if(result == 'ask_advice'):
        disease = contains_disease_info(message)
        if(disease):
            res = find_disease_advice(disease)
        else:
            res = get_response(result)
    if(result == 'ask_symptoms'):
        disease = contains_disease_info(message)
        if(disease):
            res = find_symptoms_from_disease(disease)
        else:
            res = get_response(result)
    if(result == 'feeling_sick'):
        res = get_response(result)
    response = {
        'entent': result,
        'response': res,
    }
    
    return jsonify(response)