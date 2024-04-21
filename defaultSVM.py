from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
from sklearn import svm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# reading data
df = pd.read_csv("mouse_cortical_layers.csv")

# scaling data as needed
scaler = MinMaxScaler ()
for column in df.columns:
  try:
    df[column] = scaler.fit_transform(df[[column]])
  except:
    df[column] = df[[column]]

# extract the target variable and the feature variables
y = df['cortical_layer_class_label']
X = df.drop(columns = ['cell', 'cortical_layer_class_label'])

# splitting into training/test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# training and testing tuned model with best hyperparameters
model = svm.SVC()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
f1 = f1_score(y_test, y_pred, average = 'macro')
