from flask import Blueprint, jsonify, request
from .Training.TraininggIntent import predict_intent
from .Intent.Response.Response import get_response 
import pickle
import xgboost as xgb
main = Blueprint('main', __name__)





@main.route('/chatbot', methods=['POST'])
def predict():
   
    data = request.json
    entent = data['message']
    
    
    result = predict_intent(entent)
    res = get_response(result)
    response = {
        'entent': result,
        'response': res,
    }
    
    return jsonify(response)