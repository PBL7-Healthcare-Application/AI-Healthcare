import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Đường dẫn đến tệp JSON bạn đã tải xuống
cred = credentials.Certificate('F:/PBL7/ai-healthcare-chatwithchatbot-firebase-adminsdk-35y92-a20f1ae30c.json')

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
            'isSure': 1
        })
    for symptom in psym:
        symptoms.append({
            'nameSymptom': symptom,
            'isSure': 0
        })

    data_pushFirebase = {
    'idUser': 'unique_user_id',
    'symptoms': symptoms,
    'createdAt': datetime.now().isoformat()
    }

    doc_ref = db.collection('symptom').add(data_pushFirebase)
    return doc_ref