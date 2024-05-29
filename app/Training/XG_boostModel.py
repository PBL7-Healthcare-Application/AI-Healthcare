import re
import pandas as pd
import pyttsx3
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import csv
import warnings


data = pd.read_csv('E:\Code_Project\PBL7\AI-Healthcare\\app\model\xgboost_model.pkl')
data.info();

# print("huy")