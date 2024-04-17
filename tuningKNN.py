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
untunedModel = KNeighborsClassifier()
untunedModel.fit(X_train, y_train)
y_pred_untuned = untunedModel.predict(X_test)
f1_untuned = f1_score(y_test, y_pred_untuned, average = 'macro')
print(f'F1 score (before tuning): {f1_untuned}')

# hyperparameter tuning
leafs = list(range(1, 50))
results = {}
for l in leafs:
  tunedModel = KNeighborsClassifier(n_neighbors = 5, leaf_size = l)
  tunedModel.fit(X_train, y_train)
  y_pred_tuned = tunedModel.predict(X_test)
  f1_tuned = f1_score(y_test, y_pred_tuned, average = 'macro')
  results[(l)] = f1_tuned
best_params = max(results, key = results.get)
print(f'Best params (leafSize): {best_params}')
print(f'F1 score of best tuned model: {round(results[best_params], 2)}')
