import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import json
import random
import nltk
import numpy as np
import pickle
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
# Đường dẫn đến các tệp dữ liệu
# file_paths = [pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\Ask_Advice.csv"), pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\Ask_disease_info.csv"), pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\Ask_symptoms.csv"),pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\FareWell.csv"),pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\Feeling_sick.csv"),pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\Greeting.csv"),pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\Listing_Symptoms.csv")]  # Thay đổi thành các đường dẫn thực tế của bạn

# data = pd.concat(file_paths, ignore_index=True)

# # Tiền xử lý dữ liệu
# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(data['text'])
# y = data['intent']

# # Chia dữ liệu thành tập huấn luyện và kiểm tra
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Huấn luyện mô hình
# model = MultinomialNB()
# model.fit(X_train, y_train)

# # Dự đoán và đánh giá mô hình
# y_pred = model.predict(X_test)
# model_file_path = "model.pkl"

# # Lưu mô hình ra file
# joblib.dump(model, model_file_path)

# vectorizer_file_path = "vectorizer.pkl"
# joblib.dump(vectorizer, vectorizer_file_path)
# print(classification_report(y_test, y_pred))
# print('Accuracy:', accuracy_score(y_test, y_pred))

# # Hàm dự đoán ý định
# def predict_intent(text):
#     model_path = 'E:\Code_Project\PBL7\AI-Healthcare\model.pkl'
#     clf = joblib.load(model_path)
#     vectorizer = TfidfVectorizer()
#     text_vector = vectorizer.transform([text])
#     intent = clf.predict(text_vector)[0]
#     return intent

# # Ví dụ sử dụng
# print(predict_intent('What should I do?'))
# print(predict_intent('Can you give me some advice?'))


# Hàm dự đoán ý định
def predict_intent(pattern):
    
    model_path = os.path.join("app/model", 'intent_prediction_model.pkl')
    vectorizer_path = os.path.join("app/model", 'vectorizer.pkl')
    loaded_model = joblib.load(model_path)
    loaded_vectorizer = joblib.load(vectorizer_path)
    
    # Vectorize the input pattern
    pattern_vec = loaded_vectorizer.transform([pattern])
    
    # Predict the intent
    intent = loaded_model.predict(pattern_vec)
    if intent is not None:
        return intent[0]
    else:
        return None

def generate_response(tag):
    print('tag: ', tag)
    with open(os.path.join("app/Intent", 'Intent.json')) as file:
        intents_json = json.load(file)
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

# ============================
def bow(sentence, words, show_details=True):
  sentence_words = clean_up_sentence(sentence)
#print(sentence_words)

# bag of words - matrix of N words, vocabulary matrix

  bag = [0]*len(words) 
  #print(bag)

  for s in sentence_words:  
      for i,w in enumerate(words):
          if w == s: 
              # assign 1 if current word is in the vocabulary position
              bag[i] = 1
              if show_details:
                  print ("found in bag: %s" % w)
              #print ("found in bag: %s" % w)
  #print(bag)
  return(np.array(bag))
def clean_up_sentence(sentence):
  sentence_words = nltk.word_tokenize(sentence)
#print(sentence_words)
# stem each word - create short form for word

  sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
#print(sentence_words)

  return sentence_words

def bow(sentence, words, show_details=True):
  sentence_words = clean_up_sentence(sentence)
#print(sentence_words)

# bag of words - matrix of N words, vocabulary matrix

  bag = [0]*len(words) 
  #print(bag)

  for s in sentence_words:  
      for i,w in enumerate(words):
          if w == s: 
              # assign 1 if current word is in the vocabulary position
              bag[i] = 1
              if show_details:
                  print ("found in bag: %s" % w)
              #print ("found in bag: %s" % w)
  #print(bag)
  return(np.array(bag))

def predict_class(sentence):
  try:
        model = load_model(os.path.join("app/model", 'chatbot_model.h5'))
        words = pickle.load(open(os.path.join("app/model", 'words.pkl'),'rb'))

        classes = pickle.load(open(os.path.join("app/model", 'classes.pkl'),'rb'))
        p = bow(sentence, words,show_details=False)

        res = model.predict(np.array([p]))
        if res is not None:
           res = res[0]
        else:
            print("Prediction returned None")
            return None

        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)

        return_list = []

        for r in results:
            return_list.append(classes[r[0]])
        if len(return_list) > 0:
            return return_list
        else:
            return None   
  except Exception as error:
        print(f"An error occurred: {error}")
        return None

def getResponse(ints):
  intentShort = os.path.join("app/Data", 'intents_short.json')
  with open(intentShort, 'r') as f:
        intents_json = json.load(f)
  tag = ints[0]['intent']
#print(tag)

  list_of_intents = intents_json['intents']
  #print(list_of_intents)

  for i in list_of_intents:
      if(i['tag']== tag):
          result = random.choice(i['responses'])
          break
  return result

