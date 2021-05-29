import pandas as pd 
import sklearn 
import pickle

from sklearn import preprocessing 
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression

from aif360.datasets import StandardDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric

import matplotlib.pyplot as plt

df = pd.read_csv('../data/cox-violent-parsed.csv', low_memory=False)
whole_df = df [['is_violent_recid', 'age', 'sex', 'race', 'dob', 'juv_fel_count', 'juv_misd_count', 'juv_other_count', 'priors_count', 'c_charge_desc', 'c_charge_degree']]


features_num = ['age', 'juv_fel_count', 'juv_misd_count', 'juv_other_count', 'priors_count']
features_cat = ['sex', 'race', 'dob', 'c_charge_desc', 'c_charge_degree']

X_cat = df[features_cat]
X_cat = X_cat.fillna('Not Specified')
X_num = df[features_num]

enc = preprocessing.OneHotEncoder()
enc.fit(X_cat) 
one_hot = enc.transform(X_cat) 
X_cat_proc = pd.DataFrame(one_hot.toarray(), columns=enc.get_feature_names())
scaled = preprocessing.scale(X_num)
X_num_proc = pd.DataFrame(scaled, columns=features_num)
X = pd.concat([X_num_proc, X_cat_proc], axis=1, sort=False)
X = X.fillna(0) # remove NaN values
y = df['is_violent_recid']

X_train, X_TEMP, y_train, y_TEMP = train_test_split(X, y, test_size=0.30) # split out into training 70% of our data
X_validation, X_test, y_validation, y_test = train_test_split(X_TEMP, y_TEMP, test_size=0.50) # split out into validation 15% of our data and test 15% of our data

model = LogisticRegression(solver='lbfgs', max_iter=100000).fit(X_train, y_train) 

filename = 'all_feat_model.pkl'
outfile = open(filename, 'wb')
pickle.dump(model, outfile)
outfile.close()

#Compute Metrics on validation set
y_pred = model.predict(X_validation)
validation_comp = X_validation.copy()
validation_comp['is_violent_recid'] = y_validation

validation_pred = X_validation.copy()
validation_pred['is_violent_recid'] = y_pred

#Choose privileged and unprivileged groups; this is just an example
unprivileged_group = 'African-American'
privileged_group = 'Caucasian'
priv = []
prot = []
unpriv_dict = {}
priv_dict = {}
f_c = []
for i in range(validation_comp.shape[1]):
    f_c.append([])
    if (validation_comp.columns[i].find(unprivileged_group) != -1):
        prot.append(validation_comp.columns[i])
        unpriv_dict = {validation_comp.columns[i]:1}
    if (validation_comp.columns[i].find(privileged_group) != -1):
        priv.append([1])
        prot.append(validation_comp.columns[i])
        priv_dict = {validation_comp.columns[i]:1}
    else:
        priv.append([])

stdDs = StandardDataset(validation_comp, 'is_violent_recid', [0], prot, priv)
stdPred = StandardDataset(validation_pred, 'is_violent_recid', [0], prot, priv)
bi_met = BinaryLabelDatasetMetric(stdDs, privileged_groups=[priv_dict], unprivileged_groups=[unpriv_dict])
class_met = ClassificationMetric(stdDs, stdPred, unprivileged_groups=[unpriv_dict], privileged_groups=[priv_dict])

disparate_impact = bi_met.disparate_impact()
#error_rate_ratio = class_met.error_rate_ratio()
eq_diff = class_met.equal_opportunity_difference()

#Create 2 Bar Graphs
x = [1]
di_y = [disparate_impact]
er_y = [error_rate_ratio]
plt.ylim(bottom = 0, top = 2)
plt.xlim(left = 0, right = 2)

ax = plt.gca()
ax.axes.xaxis.set_visible(False)

plt.bar(x, di_y, width = 0.6)
plt.axhline(y=1.25, xmin=0, xmax=2, linestyle='--', color='black')
plt.axhline(y=1, xmin=0, xmax=2, linestyle='--', color='green')
plt.axhline(y=0.75, xmin=0, xmax=2, linestyle='--', color='black')

plt.title('Disparate Impact')
plt.show()

plt.ylim(bottom = 0, top = 2)
plt.xlim(left = 0, right = 2)
ax = plt.gca()
ax.axes.xaxis.set_visible(False)

plt.bar(di_x, er_y, width = 0.6)
plt.axhline(y=1.25, xmin=0, xmax=2, linestyle='--', color='black')
plt.axhline(y=1, xmin=0, xmax=2, linestyle='--', color='green')
plt.axhline(y=0.8, xmin=0, xmax=2, linestyle='--', color='black')
plt.title('Error Rate Ratio')
plt.show()
