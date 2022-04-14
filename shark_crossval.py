import json
import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sklearn
import sys
from sklearn.linear_model import LogisticRegression as lr
from sklearn.tree import DecisionTreeClassifier as dt
from sklearn.model_selection import train_test_split as tts
from sklearn.model_selection import cross_val_score as cvs
from sklearn.preprocessing import MultiLabelBinarizer

americas = pd.read_csv('americas.csv')

africa = pd.read_csv('africa.csv')

tree = dt(random_state=42)
lr_model = lr(random_state=42)

americas['coord'] = americas[['lat', 'long']].apply(tuple, axis=1)

print("Processing...")

coords = MultiLabelBinarizer().fit_transform(americas['coord'])

print("Training Tree...")

cvs(tree, np.array(americas['month']).reshape(-1,1), coords, cv=5, verbose=1, n_jobs=-1)

# print("Training Logistic Regression...")

# cvs(lr_model, np.array(americas['month']).reshape(-1,1), coords, cv=5, verbose=1, n_jobs=-1)