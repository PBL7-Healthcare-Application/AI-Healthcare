import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import joblib
# Đường dẫn đến các tệp dữ liệu
file_paths = [pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\Ask_Advice.csv"), pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\Ask_disease_info.csv"), pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\Ask_symptoms.csv"),pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\FareWell.csv"),pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\Feeling_sick.csv"),pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\Greeting.csv"),pd.read_csv("E:\Code_Project\PBL7\AI-Healthcare\\app\Intent\Listing_Symptoms.csv")]  # Thay đổi thành các đường dẫn thực tế của bạn

data = pd.concat(file_paths, ignore_index=True)

# Tiền xử lý dữ liệu
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['text'])
y = data['intent']

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình
model = MultinomialNB()
model.fit(X_train, y_train)

# Dự đoán và đánh giá mô hình
y_pred = model.predict(X_test)
model_file_path = "model.pkl"

# Lưu mô hình ra file
joblib.dump(model, model_file_path)
print(classification_report(y_test, y_pred))
print('Accuracy:', accuracy_score(y_test, y_pred))

# Hàm dự đoán ý định
def predict_intent(text):
    text_vector = vectorizer.transform([text])
    intent = model.predict(text_vector)[0]
    return intent

# Ví dụ sử dụng
print(predict_intent('What should I do?'))
print(predict_intent('Can you give me some advice?'))