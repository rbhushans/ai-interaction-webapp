import pandas as pd 
import sklearn 
import pickle

from sklearn import preprocessing 
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression

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
#print(X_train.shape, X_validation.shape, X_test.shape) # print data shape to check the sizing is correct

model = LogisticRegression(solver='lbfgs', max_iter=100000).fit(X_train, y_train) 

filename = 'all_feat_model.pkl'
outfile = open(filename, 'wb')
pickle.dump(model, outfile)
outfile.close()
