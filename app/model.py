import pandas as pd 
import sklearn 
import pickle
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import circlify
import re

from sklearn import preprocessing 
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score
from sklearn.linear_model import LogisticRegression

features_num = ['age', 'juv_fel_count', 'juv_misd_count', 'juv_other_count', 'priors_count']
features_cat = ['sex', 'race', 'dob', 'c_charge_desc', 'c_charge_degree']

def construct_lr_model(features, filename_str):
    df = pd.read_csv('data/cox-violent-parsed.csv', low_memory=False)
    df.drop(df.loc[df['is_recid']==-1].index, inplace=True)
    df = df.reset_index()
    df = df.astype(str).apply(lambda x: x.str.lower())
    whole_df = df [['is_recid', 'age', 'sex', 'race', 'dob', 'juv_fel_count', 'juv_misd_count', 'juv_other_count', 'priors_count', 'c_charge_desc', 'c_charge_degree']]
    print(whole_df['race'].unique())
    features = sorted(features)

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
    X_num = X_num.fillna(0)
    enc = preprocessing.OneHotEncoder()
    scaler = preprocessing.StandardScaler()

    if selected_cat_features != []:
        enc.fit(X_cat) 
        one_hot = enc.transform(X_cat) 
        X_cat_proc = pd.DataFrame(one_hot.toarray(), columns=enc.get_feature_names())
    else:
        X_cat_proc = pd.DataFrame()

    if selected_num_features != []:
        scaler.fit(X_num)
        scaled = scaler.transform(X_num)
        X_num_proc = pd.DataFrame(scaled, columns=selected_num_features)
    else:
        X_num_proc = pd.DataFrame()
    X = pd.concat([X_num_proc, X_cat_proc], axis=1, sort=False)
    print(X.columns.values)
    X = X.fillna(0) # remove NaN values
    y = df['is_recid']

    x_train, x_validation, y_train, y_validation = train_test_split(X, y, test_size=0.30) # split out into training 70% of our data

    model = LogisticRegression(solver='lbfgs', max_iter=100000).fit(x_train, y_train) 
    y_pred = model.predict(x_validation)
    precision = precision_score(y_validation, y_pred, pos_label='1')
    recall = recall_score(y_validation, y_pred, pos_label='1')
    coef = pd.concat([pd.DataFrame(x_train.columns),pd.DataFrame(np.abs(np.transpose(model.coef_)))], axis = 1)
    #randomly choose x, y values for each feature
    coef.columns = ['Feature', 'Weight']
    coef = coef[coef['Weight'] != 0]
    coef['Weight'] = coef['Weight'] * 100
    # print(coef)

    if "c_charge_degree" in selected_cat_features:
        charge_sum = 0
        charge_count = 0
        for index, row in coef.iterrows():
            if "(" in row['Feature']:
                charge_sum += row['Weight']
                charge_count += 1
        coef = coef[~coef['Feature'].str.contains("\(") & ~coef['Feature'].str.contains("nan")]
        coef = coef.append({'Feature': 'Charge Degree', 'Weight': charge_sum/charge_count}, ignore_index=True)
    coef['Feature'] = coef['Feature'].str.title()
    # print(coef)

    circles = circlify.circlify(coef['Weight'].tolist())
    fig, ax = plt.subplots(figsize=(10,10))

    # Title
    ax.set_title('Feature Intensities')

    # Remove axes
    ax.axis('off')

    # Find axis boundaries
    lim = max(
        max(
            abs(circle.x) + circle.r,
            abs(circle.y) + circle.r,
        )
        for circle in circles
    )
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)

    # list of labels
    regex = re.compile('X._')
    labels = []
    for v in coef['Feature'].values:
        if re.match(regex, v):
            vals = v.split("_")
            labels.append(vals[1])
        else:
            labels.append(v)

    colors = plt.cm.get_cmap('hsv', len(coef))
    i = 0
    legend_elems = []
    # print circles
    for circle, label in zip(circles, labels):
        x, y, r = circle
        ax.add_patch(plt.Circle((x, y), r*0.9, alpha=0.7, linewidth=2, color=colors(i)))
        legend_elems.append(Line2D([0], [0], color=colors(i), marker='o', label=label))
        i += 1
        if r > 0.1:
            plt.annotate(
                label, 
                (x,y ) ,
                va='center',
                ha='center',
                size=r*50
            )
    ax.legend(handles=legend_elems)
    
    filename= 'models_users/model&' + "&".join(selected_num_features) + "&" + "&".join(selected_cat_features) + "&" + filename_str 

    plt.savefig(filename + "_feature_intensity")

    outfile = open(filename + '.pkl', 'wb')
    pickle.dump(model, outfile)
    outfile.close()

    outfile = open(filename + '_enc.pkl', 'wb')
    pickle.dump(enc, outfile)
    outfile.close()

    outfile = open(filename + '_scaler.pkl', 'wb')
    pickle.dump(scaler, outfile)
    outfile.close()
    return filename, precision, recall, coef


def test_lr_model(model, enc, scaler, filename, features):
    #used featuers:
    used_features = filename.split("&")[1:-1]
    #reorder features
    #age, juv fel count, juv misd count, juv other count, 
    #priors count, sex, race, charge degree
    remove_idxs = []
    selected_cat_features = []
    selected_num_features = []
    str_list = []
    num_list = []
    for f in used_features:

        if f in features_num:
            selected_num_features.append(f)
        elif f in features_cat:
            selected_cat_features.append(f)
        
        if f == "age":
            num_list.append(int(features[0]))
        elif f == "juv_fel_count":
            num_list.append(int(features[1]))
        elif f == "juv_misd_count":
            num_list.append(int(features[2]))
        elif f == "juv_other_count":
            num_list.append(int(features[3]))
        elif f == "priors_count":
            num_list.append(int(features[4]))
        elif f == "sex":
            if features[5] == "other":
                str_list.append("Not Specified")
            else:
                str_list.append(features[5])
        elif f == "race":
            if features[6] == "native-american":
                feature[6] = "native american"
            str_list.append(features[6])
        elif f == "c_charge_degree":
            str_list.append("(" + features[7] + ")")

    num_df = pd.DataFrame([num_list])
    num_df.columns = selected_num_features

    str_df = pd.DataFrame([str_list])
    str_df.columns = selected_cat_features

    if selected_cat_features != []:
        one_hot = enc.transform(str_df)
        X_cat_proc = pd.DataFrame(one_hot.toarray(), columns=enc.get_feature_names())
    else:
        X_cat_proc = pd.DataFrame()

    if selected_num_features != []:
        scaled = scaler.transform(num_df)
        X_num_proc = pd.DataFrame(scaled, columns=selected_num_features)
    else:
        X_num_proc = pd.DataFrame()

    X = pd.concat([X_num_proc, X_cat_proc], axis=1, sort=False)

    #make prediction
    prediction = model.predict(X)
    confidence = model.predict_proba(X)
    return prediction, confidence[0]