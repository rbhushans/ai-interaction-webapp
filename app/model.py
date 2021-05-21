import pandas as pd 
import sklearn 
import pickle
import os
import numpy as np

from sklearn import preprocessing 
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score
from sklearn.linear_model import LogisticRegression

enc = preprocessing.OneHotEncoder()

def construct_lr_model(features, filename_str):
    df = pd.read_csv('data/cox-violent-parsed.csv', low_memory=False)
    df.drop(df.loc[df['is_recid']==-1].index, inplace=True)
    whole_df = df [['is_recid', 'age', 'sex', 'race', 'dob', 'juv_fel_count', 'juv_misd_count', 'juv_other_count', 'priors_count', 'c_charge_desc', 'c_charge_degree']]

    features = sorted(features)
    features_num = ['age', 'juv_fel_count', 'juv_misd_count', 'juv_other_count', 'priors_count']
    features_cat = ['sex', 'race', 'dob', 'c_charge_desc', 'c_charge_degree']


    selected_num_features = []
    selected_cat_features = []

    for f in features:
        f = f.lower()
        if f == "date of birth":
            f = "dob"
        elif f == "juvenile felony count":
            f = "juv_fel_count"
        elif f == "juvenile misdemeanor count":
            f = "juv_misd_count"
        elif f == "juvenile other count":
            f = "juv_other_count"
        elif f == "priors count":
            f = "priors_count"
        elif f == "charge description":
            f = "c_charge_desc"
        elif f == "charge degree":
            f = "c_charge_degree"

        if f in features_num:
            selected_num_features.append(f)
        else:
            selected_cat_features.append(f)

    X_cat = df[selected_cat_features]
    X_cat = X_cat.fillna('Not Specified')
    X_num = df[selected_num_features]

    
    global enc
    enc.fit(X_cat) 
    one_hot = enc.transform(X_cat) 
    X_cat_proc = pd.DataFrame(one_hot.toarray(), columns=enc.get_feature_names())
    scaled = preprocessing.scale(X_num)
    X_num_proc = pd.DataFrame(scaled, columns=selected_num_features)
    X = pd.concat([X_num_proc, X_cat_proc], axis=1, sort=False)
    X = X.fillna(0) # remove NaN values
    y = df['is_recid']

    x_train, x_validation, y_train, y_validation = train_test_split(X, y, test_size=0.30) # split out into training 70% of our data

    model = LogisticRegression(solver='lbfgs', max_iter=100000).fit(x_train, y_train) 
    y_pred = model.predict(x_validation)
    precision = precision_score(y_validation, y_pred)
    recall = recall_score(y_validation, y_pred)

    filename = 'models_users/model&' + "&".join(selected_num_features) + "&" + "&".join(selected_cat_features) + "&" + filename_str + '.pkl'

    outfile = open(filename, 'wb')
    pickle.dump(model, outfile)
    outfile.close()
    return filename, precision, recall


def test_lr_model(model, filename, features):
    #used featuers:
    print(filename)
    used_features = filename.split("&")[1:-1]
    #reorder features
    #age, juv fel count, juv misd count, juv other count, 
    #priors count, sex, race, charge degree
    remove_idxs = []
    if "age" not in used_features:
        remove_idxs.append(0)
    if "juv_fel_count" not in used_features:
        remove_idxs.append(1)
    if "juv_misd_count" not in used_features:
        remove_idxs.append(2)
    if "juv_other_count" not in used_features:
        remove_idxs.append(3)
    if "priors_count" not in used_features:
        remove_idxs.append(4)
    if "sex" not in used_features:
        remove_idxs.append(5)
    if "race" not in used_features:
        remove_idxs.append(6)
    if "c_charge_degree" not in used_features:
        remove_idxs.append(7)

    remove_idxs = sorted(remove_idxs, reverse=True)
    for index in remove_idxs:
        del features[index]
    
    num_list = []
    str_list = []

    for f in features:
        try:
            num_list.append(int(f))
        except ValueError:
            str_list.append(f)

    

    #one hot encoding
    
    print(enc.categories)
    enc.transform(np.array(str_list).reshape(1, -1))
    features = np.concatenate((np.array(num_list).reshape(1, -1), str_list))

    # features = np.array(features).reshape(1, -1)
    print(used_features)
    print(features)

    #make prediction
    prediction = model.predict(features)
    confidence = model.decision_function(features)
    return prediction, confidence