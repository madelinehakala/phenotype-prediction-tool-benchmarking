from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
from sklearn import svm
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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# training and testing rbf model
untunedRbfModel = svm.SVC(kernel = 'rbf')
untunedRbfModel.fit(X_train, y_train)
y_pred_untunedRbf = untunedRbfModel.predict(X_test)
f1_untunedRbf = f1_score(y_test, y_pred_untunedRbf, average = 'macro')
print(f'Rbf kernel F1 (before tuning): {f1_untunedRbf}')

# training and testing linear model
untunedLinearModel = svm.SVC(kernel = 'linear')
untunedLinearModel.fit(X_train, y_train)
y_pred_untunedLinear = untunedLinearModel.predict(X_test)
f1_untunedLinear = f1_score(y_test, y_pred_untunedLinear, average = 'macro')
print(f'Linear kernel F1 (before tuning): {f1_untunedLinear}')


# hyperparameter tuning
grid = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
results = {}
for c in grid:
    tunedLinearModel = svm.SVC(kernel='linear', C=c, random_state=0)
    tunedLinearModel.fit(X_train, y_train)
    y_pred_tunedLinear = tunedLinearModel.predict(X_test)
    f1_tunedLinear = f1_score(y_test, y_pred_tunedLinear, average = 'macro')
    results[('linear', c, np.nan)] = f1_tunedLinear
for c in grid:
    for g in grid:
        tunedRbfModel = svm.SVC(kernel = 'rbf', C = c, gamma = g, random_state = 0)
        tunedRbfModel.fit(X_train, y_train)
        y_pred_tunedRbf = tunedRbfModel.predict(X_test)
        f1_tunedRbf = f1_score(y_test, y_pred_tunedRbf, average = 'macro')
        results[('rbf', c, g)] = f1_tunedRbf
best_params = max(results, key=results.get)
print(f'Best params (kernel, C, gamma): {best_params}')
print(f'F1 score of best tuned model: {round(results[best_params], 2)}')
