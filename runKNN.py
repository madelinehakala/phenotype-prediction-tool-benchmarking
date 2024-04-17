from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

df = pd.read_csv("mouse_cortical_layers.csv")

# checking the class balance 
print(df['cortical_layer_class_label'].value_counts())

# plotting class (im)balance
labels = sorted(df['cortical_layer_class_label'].unique())
counts = df['cortical_layer_class_label'].value_counts()
plt.bar(labels, counts)
x_labs = ['1', '2/3', '4', '5', '6']
plt.xticks(labels, x_labs)
plt.xlabel('Cortical Layer')
plt.ylabel('Count')
plt.title('Class Balance of Target Variable (Cortical Layer)')
plt.show()

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

# training and testing model
tunedModel = KNeighborsClassifier(leaf_size = 1)
tunedModel.fit(X_train, y_train)
y_pred_tuned = tunedModel.predict(X_test)
f1_tuned = f1_score(y_test, y_pred_tuned, average = 'macro')
print(f'F1 score: {f1_tuned}')
