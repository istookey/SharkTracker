import json
import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sklearn
import sys
from sklearn.linear_model import LogisticRegression as lr
from sklearn.tree import DecisionTreeClassifier as dt
from sklearn.ensemble import RandomForestClassifier as rf
from sklearn.model_selection import train_test_split as tts
from sklearn.model_selection import cross_val_score as cvs
from sklearn.preprocessing import MultiLabelBinarizer

americas = pd.read_csv('americas.csv')

africa = pd.read_csv('africa.csv')

tree = dt(random_state=42)
lr_model = lr(random_state=42, max_iter=100000, solver='lbfgs')
rf_model = rf(random_state=42, n_estimators=100, class_weight='balanced')

americas['coord'] = americas[['lat', 'long']].apply(tuple, axis=1)
americas['time'] = pd.to_datetime(americas['time'])
americas['time'] = americas['time']
americas['time'] = americas['time'].apply(lambda x: x.value)

print("Training Americas Tree...")

# cvs(tree, np.array(americas['month']).reshape(-1,1), coords, cv=5, verbose=0, n_jobs=-1)
print(f"Max Score: {cvs(tree, americas.drop(['month', 'coord', 'name', 'id', 'time'], axis=1), np.array(americas['month']).reshape(-1,1), cv=10, verbose=0, n_jobs=-1).max()}")

print("Training Americas Logistic Regression...")

print(f"Max Score: {cvs(lr_model, americas.drop(['month', 'coord', 'name', 'id', 'time'], axis=1), np.array(americas['month']), cv=10, verbose=0, n_jobs=-1).max()}")

print("Training Americas Random Forest...")

print(f"Max Score: {cvs(rf_model, americas.drop(['month', 'coord', 'name', 'id', 'time'], axis=1), np.array(americas['month']), cv=10, verbose=0, n_jobs=-1).max()}")

# cvs(lr_model, np.array(americas['month']).reshape(-1,1), coords, cv=5, verbose=0, n_jobs=-1)

africa['coord'] = africa[['lat', 'long']].apply(tuple, axis=1)
africa['time'] = pd.to_datetime(africa['time'])
africa['time'] = africa['time']
africa['time'] = africa['time'].apply(lambda x: x.value)

print("Training Africa Tree...")

# cvs(tree, np.array(americas['month']).reshape(-1,1), coords, cv=5, verbose=0, n_jobs=-1)
print(f"Max Score: {cvs(tree, africa.drop(['month', 'coord', 'name', 'id', 'time'], axis=1), np.array(africa['month']).reshape(-1,1), cv=10, verbose=0, n_jobs=-1).max()}")

print("Training Africa Logistic Regression...")

print(f"Max Score: {cvs(lr_model, africa.drop(['month', 'coord', 'name', 'id', 'time'], axis=1), np.array(africa['month']), cv=10, verbose=0, n_jobs=-1).max()}")

print("Training Africa Random Forest...")

print(f"Max Score: {cvs(rf_model, africa.drop(['month', 'coord', 'name', 'id', 'time'], axis=1), np.array(africa['month']), cv=10, verbose=0, n_jobs=-1).max()}")
