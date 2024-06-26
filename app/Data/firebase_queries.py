import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
from pytz import timezone
import pytz

# Đường dẫn đến tệp JSON bạn đã tải xuống

cred = credentials.Certificate(os.path.join("app/Data",'ai-healthcare-chatwithchatbot-firebase-adminsdk-35y92-e2cd5aba79.json'))

# Khởi tạo ứng dụng Firebase
firebase_admin.initialize_app(cred)

# Lấy client Firestore
db = firestore.client()

def update_symptom(_idDocument, _nameSymptom, isSure):
    symptomdocument = db.collection('symptom').document(_idDocument)
    listsymptom = symptomdocument.get()
    symptoms = listsymptom.get('symptoms')

    # Tìm và cập nhật phần tử cần thiết
    for symptom in symptoms:
        if symptom['nameSymptom'] == _nameSymptom.replace(' ','_'):
            symptom['isSure'] = isSure
            break

    symptomdocument.update({'symptoms': symptoms})

    
def get_symptom(_idDocument):
    getpossymp = db.collection('symptom').document(_idDocument).get()
    if getpossymp.exists:
        return getpossymp.to_dict()['symptoms']
    return None

def add_symptom(correctsym, psym):
    symptoms = []
    for symptom in correctsym:
        symptoms.append({
            'nameSymptom': symptom,
            'isSure': 1,
            'i' : 0
        })
    i = 0
    for symptom in psym:
        i+=1
        symptoms.append({
            'nameSymptom': symptom,
            # 'isSure': 0
            'isSure': 0,
            'i' : i
        })
    # Get the current time in UTC+7
    utc_plus_7 = pytz.timezone('Asia/Bangkok')
    current_time = datetime.now(utc_plus_7).isoformat()

    data_pushFirebase = {
    'idUser': 'unique_user_id',
    'symptoms': symptoms,
    'createdAt': current_time
    }

    doc_ref = db.collection('symptom').add(data_pushFirebase)
    return doc_ref

def save_message(idDocument, message, isUserSender):
    user_ref = db.collection('chatbot').document(idDocument)
    user = user_ref.get()

    # Get the current time in UTC+7
    utc_plus_7 = pytz.timezone('Asia/Bangkok')
    current_time = datetime.now(utc_plus_7).isoformat()

    message_obj = {
        'text': message,
        'isUserSender': isUserSender,
        'createdAt': current_time
    }

    if user.exists:
        # User already exists, append the new message
        user_ref.update({
            'messages': firestore.ArrayUnion([message_obj])
        })
    # else:
    #     # User does not exist, create a new document
    #     user_ref.set({
    #         'idUser': idUser,
    #         'createdAt': datetime.now().isoformat(),
    #         'messages': [message_obj]
    #     })

def get_name(idDocument):
    getpossymp = db.collection('chatbot').document(idDocument).get()
    if getpossymp.exists:
        return getpossymp.to_dict()['name']
    return None

