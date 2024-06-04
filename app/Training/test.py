from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import json
import random
import nltk
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

lemmatizer = WordNetLemmatizer()
model = load_model('E:\Code_Project\PBL7\AI-Healthcare\\app\model\chatbot_model.h5')

with open('E:\Code_Project\PBL7\AI-Healthcare\\app\Data\intents.json') as file:
    intents = json.load(file)

words = [] # Danh sách các từ duy nhất
classes = [] # Danh sách các nhãn (intent)
documents = [] # Danh sách các cặp (mẫu câu, nhãn)
ignore_words = ['?', '!']
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"found in bag: {w}")
    return(np.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['patterns'])
            break
    return result

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json['message']
    ints = predict_class(user_message, model)
    response = get_response(ints, intents)
    return jsonify({"response": response})
    # return jsonify({"response": response})

if __name__ == "__main__":
    app.run()