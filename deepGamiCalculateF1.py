import pandas as pd
from sklearn.metrics import f1_score

# reading csv with true class labels
truth = pd.read_csv('DeepGAMI/run1_test_truth.csv', names = ['truth'])

## Assessing cg model
# reading csv with cg model class probabilities and adding predicted labels and true labels columns
cg = pd.read_csv('DeepGAMI/run1_cg_test_prob.csv', names = [0, 1, 2, 3, 4])
cg['prediction'] = cg.idxmax(axis = 1)
cg['truth'] = truth

# calculating cg model f1 score
f1_cg = f1_score(cg['truth'], cg['prediction'], average = 'macro')


## Assessing 2m model
# reading csv with cg model class probabilities and adding predicted labels and true labels columns
m = pd.read_csv('DeepGAMI/run1_2m_test_prob.csv', names = [0, 1, 2, 3, 4])
m['prediction'] = m.idxmax(axis = 1)
m['truth'] = truth

# calculating cg model f1 score
f1_m = f1_score(m['truth'], m['prediction'], average = 'macro')

## Average performance
print((f1_m + f1_cg) / 2)
