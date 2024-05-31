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
from Constants.AppString import XGBOOST_MODEL_PATH_ALLAN

data = pd.read_csv(XGBOOST_MODEL_PATH_ALLAN)
data.info()

# print("huy")