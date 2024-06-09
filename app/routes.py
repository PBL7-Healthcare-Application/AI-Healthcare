from flask import Blueprint, jsonify, request
from .Training.TraininggIntent import generate_response, predict_class
from .Training.Predict_Disease import contains_disease_info ,find_disease_description ,find_disease_advice,find_symptoms_from_disease
from .Training.GetSymptomFromText import get_symptoms
import pickle
import xgboost as xgb
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from .Training.Predict_Disease import predict_disease_from_symptom
from .Data.firebase_queries import update_symptom, get_symptom, add_symptom, save_message,get_name
main = Blueprint('main', __name__)


@main.route('/chatbot', methods=['POST'])
def predict():
   
    data = request.json
    entent = data['message']
    print(entent)
    save_message(data['idChat'], entent, True)
    _idDocument = data['idDocument']
    _nameSymptom = data['nameSymptom']
    
    #Nếu truyền giá trị _idDocument và _nameSymptom từ Storage thì sẽ check YES/NO Question
    if _nameSymptom is not None and _idDocument is not None:
        if entent != 'no' and entent != 'yes':
            res = 'You have to answer "yes" or "no" for this question. Please try again.' 
            response = {
            'response': res,
            'idDocument': _idDocument,
            'nameSymptom': _nameSymptom
            }
            return jsonify(response)
        else:
            if entent == 'yes':
                isSure = 1
            if entent == 'no':
                isSure = 2

            update_symptom(_idDocument, _nameSymptom, isSure)

            all_symptoms = get_symptom(_idDocument)
            
            if all_symptoms is not None:
                for symptom in all_symptoms:
                    if symptom['isSure'] == 0:
                        nameSymptom = symptom['nameSymptom'].replace('_',' ')
                        
                        res = 'Do you experience '+ nameSymptom + ' ?'
                        save_message(data['idChat'], res, False)
                        response = {
                        'response': res,
                        'idDocument': _idDocument,
                        'nameSymptom': nameSymptom
                        }
                        return jsonify(response)
            #Done get symptoms
            # res = generate_response('listing_symptoms')

            #Get list symptoms from Firebase to start predict desease
            list_symptoms = []

            all_symptoms2 = get_symptom(_idDocument)
            if all_symptoms2 is not None:
                
                for symptom in all_symptoms2:
                    if symptom['isSure'] == 1:
                        list_symptoms.append(symptom['nameSymptom'])
            
            #Predict desease
            print('list symptoms: ', list_symptoms)
            predict_disease = predict_disease_from_symptom(list_symptoms)
            res = 'Based on the information you provided, we think you have a disease: ' + predict_disease
            save_message(data['idChat'], res, False)
            response = {
            'response': res,
            'idDocument': None,
            'nameSymptom': None
            }
            return jsonify(response)

    #Nếu truyền 2 giá trị null _idDocument và _nameSymptom, system predict intent của câu  
    else:
        result = predict_class(entent)
        
        if result is not None:
            result = result[0]
            if result == 'list_symptoms':
                correctsym, psym = get_symptoms(entent)
                if len(psym)>0:
                    first_symp_ask = psym[0]
                    print('first_symp_ask: ', first_symp_ask)

                if len(psym)>0 or len(correctsym)>0:
                    doc_ref = add_symptom(correctsym, psym)

                nameSymptom = first_symp_ask.replace('_',' ')

                nameSymptom = first_symp_ask.replace('_',' ')

                res = 'Based on the signs you provided, I want to ask you a few things to confirm the information. \nDo you experience ' + nameSymptom + ' ?'
                save_message(data['idChat'], res, False)
                # doc_ref là một tuple chứa reference đến document vừa được tạo
                print(f'Tài liệu mới được tạo với ID: {doc_ref[1].id}')
                
                response = {
                'entent': result,
                'response': res,
                'idDocument': doc_ref[1].id,
                'nameSymptom': nameSymptom
                }
                return jsonify(response)
            if (result == 'ask_disease_info'):
                    disease = contains_disease_info(entent)
                    res = ''
                    if(disease):
                        res = find_disease_description(disease)
                    else:
                        res = generate_response(result)
                    save_message(data['idChat'], res, False)
                    response = {
                        'entent': result,
                        'response': res,
                        'idDocument': None,
                        'nameSymptom': None,
                    }
                
                    return jsonify(response)    
            if(result == 'ask_advice'):
                disease = contains_disease_info(entent)
                if(disease):
                    res = find_disease_advice(disease)
                else:
                    res = generate_response(result)
                save_message(data['idChat'], res, False)
                response = {
                    'entent': result,
                    'response': res,
                    'idDocument': None,
                    'nameSymptom': None,
                }
            
                return jsonify(response)
            if(result == 'ask_symptoms'):
                disease = contains_disease_info(entent)
                if(disease):
                    res = find_symptoms_from_disease(disease)
                else:
                    res = generate_response(result)
                save_message(data['idChat'], res, False)
                response = {
                    'entent': result,
                    'response': res,
                    'idDocument': None,
                    'nameSymptom': None,
                }
            
                return jsonify(response)
            if result == 'introduce_myself':
                name = get_name(data['idChat'])
                answer = generate_response("introduce_myself")
                res = "Hello, " + name + "! " + answer
                save_message(data['idChat'], res, False)
                response = {
                    'entent': result,
                    'response': res,
                    'idDocument': None,
                    'nameSymptom': None,
                }
                return jsonify(response)
            else:
                res = generate_response(result)
                save_message(data['idChat'], res, False)
                response = {
                    'entent': result,
                    'response': res,
                    'idDocument': None,
                    'nameSymptom': None,
                }
            
                return jsonify(response)
        
        else:
            res = generate_response("fallback")
            save_message(data['idChat'], res, False)

            response = {
                'entent': result,
                'response': res,
                'idDocument': doc_ref[1].id,
                'nameSymptom': nameSymptom
                }
            return jsonify(response)
        
