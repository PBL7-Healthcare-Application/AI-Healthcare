import numpy as np
from joblib import load
import pandas as pd
import pickle
import re
import os
import csv
import random

def contains_disease_info(text):
    csv_file_path = os.path.join("app/Data", 'diseases.csv')
    df = pd.read_csv(csv_file_path)
    disease_keywords = df['Drug Reaction'].tolist()
    disease_pattern = re.compile(r'\b(' + '|'.join(re.escape(keyword) for keyword in disease_keywords) + r')\b', re.IGNORECASE)
    
    # Tìm kiếm trong đoạn văn bản
    match = disease_pattern.search(text)
    if match:
        return match.group(0).lower()
    else:
        return None
    

def find_disease_description(text):
    # Đọc file CSV để lấy danh sách các mô tả bệnh
    description_list = {}
    csv_file_path = os.path.join("app/Data", 'symptom_Description.csv')
    with open(csv_file_path) as csv_file:  # Thay bằng đường dẫn thực tế đến file
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line_count, row in enumerate(csv_reader):
            if line_count == 0:
                continue  # Bỏ qua dòng tiêu đề
            description_list[row[0].lower()] = row[1]
    
    # Tạo danh sách các từ khóa từ description_list
    disease_keywords = list(description_list.keys())
    
    # Tạo một mẫu regex từ danh sách từ khóa
    disease_pattern = re.compile(r'\b(' + '|'.join(re.escape(keyword) for keyword in disease_keywords) + r')\b', re.IGNORECASE)
    
    # Tìm kiếm trong đoạn văn bản
    match = disease_pattern.search(text)
    if match:
        disease_name = match.group(0)
        return description_list[disease_name.lower()]
    else:
        return "No disease information found in the text."



def find_disease_advice(text):
    description_list = {}
    csv_file_path = os.path.join("app/Data", 'symptom_precaution.csv')
    with open(csv_file_path) as csv_file:  # Thay bằng đường dẫn thực tế đến file
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line_count, row in enumerate(csv_reader):
            if line_count == 0:
                continue  # Bỏ qua dòng tiêu đề
            description_list[row[0].lower()] = [row[1:]]
    
    # Tạo danh sách các từ khóa từ description_list
    disease_keywords = list(description_list.keys())
    
    # Tạo một mẫu regex từ danh sách từ khóa
    disease_pattern = re.compile(r'\b(' + '|'.join(re.escape(keyword) for keyword in disease_keywords) + r')\b', re.IGNORECASE)
    
    # Tìm kiếm trong đoạn văn bản
    match = disease_pattern.search(text)
    if match:
        disease_name = match.group(0)
        return description_list[disease_name.lower()]
    else:
        return "No disease information found in the text."
    

def get_time_from_sentence(sentence):
    # Biểu thức chính quy để tìm kiếm thông tin thời gian trong câu
    time_pattern = r'\b(\d+|\w+)\s*(day|week|month|year)s?\b'  # Biểu thức chính quy tìm kiếm số hoặc chữ kèm theo đơn vị thời gian

    # Tìm tất cả các chuỗi thời gian trong câu
    matches = re.findall(time_pattern, sentence, re.IGNORECASE)

    # Duyệt qua các kết quả và xử lý chúng
    total_days = 0
    for match in matches:
        time_value = match[0]  # Giá trị thời gian (số hoặc chữ)
        time_unit = match[1]   # Đơn vị thời gian
        # Chuyển đổi các giá trị chữ thành số nếu cần
        if time_value.isdigit():
            time_value = int(time_value)
        else:
            # Xử lý các giá trị chữ thành số tương ứng
            if time_value.lower() == 'a': 
                time_value = 1
            elif time_value.lower() == 'an':  
                time_value = 1
            elif time_value.lower() == 'two':
                time_value = 2
            elif time_value.lower() == 'three':
                time_value = 3
            elif time_value.lower() == 'four':
                time_value = 4
            elif time_value.lower() == 'five':
                time_value = 5
            elif time_value.lower() == 'six':
                time_value = 6
            elif time_value.lower() == 'seven':
                time_value = 7
            elif time_value.lower() == 'eight':
                time_value = 8
            elif time_value.lower() == 'nine':
                time_value = 9
            
        if time_unit == 'day':
            total_days += time_value
        elif time_unit == 'week':
            total_days += time_value * 7
        elif time_unit == 'month':
            total_days += time_value * 30  # Giả sử một tháng là 30 ngày
        elif time_unit == 'year':
            total_days += time_value * 365  # Giả sử một năm là 365 ngày

    return total_days

def find_symptoms_from_disease(text):
    symptoms_list = []
    csv_file_path = os.path.join("app/Data", 'dataset.csv')
    with open(csv_file_path) as csv_file:  # Thay bằng đường dẫn thực tế đến file
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line_count, row in enumerate(csv_reader):
            if line_count == 0:
                continue  # Bỏ qua dòng tiêu đề
            if text.lower() in row[0].lower():
                filtered_row = [item for item in row[1:] if item != '']
                symptoms_list.append([row[0], filtered_row])
    return random.choice(symptoms_list)[1]
