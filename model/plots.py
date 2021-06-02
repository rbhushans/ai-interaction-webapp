import pandas as pd 
import sklearn 
import os
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import numpy as np

from sklearn import preprocessing 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


def construct_lr_model_graph(features):
    features_num = ['age', 'juv_fel_count', 'juv_misd_count', 'juv_other_count', 'priors_count']
    features_cat = ['sex', 'race', 'c_charge_degree']
    sex_enc = ['x0_female', 'x0_male']
    race_enc = ['x1_african-american', 'x1_asian', 'x1_caucasian', 'x1_hispanic', 'x1_native american', 'x1_other']
    deg_enc = ['x2_(co3)', 'x2_(ct)',
    'x2_(f1)', 'x2_(f2)', 'x2_(f3)', 'x2_(f5)', 'x2_(f6)', 'x2_(f7)', 'x2_(m1)',
    'x2_(m2)', 'x2_(mo3)', 'x2_(ni0)', 'x2_(tcx)', 'x2_(x)', 'x2_nan']
    df = pd.read_csv('data/cox-violent-parsed.csv', low_memory=False)
    df.drop(df.loc[df['is_recid']==-1].index, inplace=True) # Removed all is_recid == -1
    df = df.reset_index()
    df = df.astype(str).apply(lambda x: x.str.lower())
    whole_df = df [['is_recid', 'age', 'sex', 'race', 'juv_fel_count', 'juv_misd_count', 'juv_other_count', 'priors_count', 'c_charge_degree']]

    features = sorted(features)

    selected_num_features = []
    selected_cat_features = []

    for f in features:
        f = f.lower()
        if f == "juvenile felony count":
            f = "juv_fel_count"
        elif f == "juvenile misdemeanor count":
            f = "juv_misd_count"
        elif f == "juvenile other count":
            f = "juv_other_count"
        elif f == "priors count":
            f = "priors_count"
        elif f == "charge degree":
            f = "c_charge_degree"

        if f in features_num:
            selected_num_features.append(f)
        else:
            selected_cat_features.append(f)

    features_edit = selected_num_features + selected_cat_features
    X_cat = df[features_cat]
    X_cat = X_cat.fillna('Not Specified')
    X_num = df[features_num]
    enc = preprocessing.OneHotEncoder()
    scaler = preprocessing.StandardScaler()

    enc.fit(X_cat) 
    one_hot = enc.transform(X_cat) 
    X_cat_proc = pd.DataFrame(one_hot.toarray(), columns=enc.get_feature_names())

    scaler.fit(X_num)
    scaled = scaler.transform(X_num)
    X_num_proc = pd.DataFrame(scaled, columns=features_num)

    X = pd.concat([X_num_proc, X_cat_proc], axis=1, sort=False)

    X = X.fillna(0) # remove NaN values
    y = df['is_recid']

    x_train, x_validation, y_train, y_validation = train_test_split(X, y, test_size=0.30)

    x_val_feat = x_validation.copy()
    for feat in X.columns.values:
        if (features_num.count(feat) > 0) and (selected_num_features.count(feat) == 0):
            #print('removing ' + feat)
            x_train = x_train.drop(columns=feat, axis = 1)
            x_val_feat = x_val_feat.drop(columns=feat, axis = 1)
        if sex_enc.count(feat) > 0 and selected_cat_features.count('sex') == 0:
            #print('removing ' + feat)
            x_train = x_train.drop(columns=feat, axis = 1)
            x_val_feat = x_val_feat.drop(columns=feat, axis = 1)
        if race_enc.count(feat) > 0 and selected_cat_features.count('race') == 0:
            #print('removing ' + feat)
            x_train = x_train.drop(columns=feat, axis = 1)
            x_val_feat = x_val_feat.drop(columns=feat, axis = 1)
        if deg_enc.count(feat) > 0 and selected_cat_features.count('c_charge_degree') == 0:
            #print('removing ' + feat)
            x_train = x_train.drop(columns=feat, axis = 1)
            x_val_feat = x_val_feat.drop(columns=feat, axis = 1)

    model = LogisticRegression(solver='lbfgs', max_iter=100000).fit(x_train, y_train)

    y_pred = model.predict(x_val_feat)
    validation_comp = x_validation.copy()
    validation_comp['is_recid'] = y_validation

    validation_pred = x_validation.copy()
    validation_pred['is_recid'] = y_pred

    num_inst = validation_comp.shape[0]

    unprivileged_group = 'african-american'
    privileged_group = 'caucasian'
    priv = []
    prot = []
    unpriv_dict = {}
    priv_dict = {}
    unpriv_col = ''
    priv_col = ''
    for i in range(validation_comp.shape[1]):
        #print(validation_comp.columns[i])
        if (validation_comp.columns[i].find(unprivileged_group) != -1):
            prot.append(validation_comp.columns[i])
            unpriv_dict = {validation_comp.columns[i]:1}
            priv.append([])
            unpriv_col = validation_comp.columns[i]
        elif (validation_comp.columns[i].find(privileged_group) != -1):
            #print('Privileged Group: ' + validation_comp.columns[i])
            priv.append([1])
            prot.append(validation_comp.columns[i])
            priv_dict = {validation_comp.columns[i]:1}
            priv_col = validation_comp.columns[i]
        else:
            priv.append([])
    priv_actual = validation_comp[validation_comp[priv_col] == 1]
    priv_pred = validation_pred[validation_pred[priv_col] == 1]
    priv_error = priv_actual[priv_actual['is_recid'] != priv_pred['is_recid']]        

    nonpriv_actual = validation_comp[validation_comp[priv_col] == 0]
    nonpriv_pred = validation_pred[validation_pred[priv_col] == 0]

    unpriv_actual = validation_comp[validation_comp[unpriv_col] == 1]
    unpriv_pred = validation_pred[validation_pred[unpriv_col] == 1]
    unpriv_error = unpriv_actual[unpriv_actual['is_recid'] != unpriv_pred['is_recid']]

    if (priv_pred['is_recid'].value_counts()[0] == priv_pred.shape[0]):
        num_priv_pos = 0
    else:
        num_priv_pos = priv_pred['is_recid'].value_counts()[1]

    if (unpriv_pred['is_recid'].value_counts()[0] == unpriv_pred.shape[0]):
        num_unpriv_pos = 0
    else:
        num_unpriv_pos = unpriv_pred['is_recid'].value_counts()[1]

    #num_pred_pos = validation_pred['is_recid'].value_counts()[1]
    #num_nonpriv_pos = nonpriv_pred['is_recid'].value_counts()[1]

    priv_error_rate = priv_error.shape[0] / priv_pred.shape[0]
    unpriv_error_rate = unpriv_error.shape[0] / unpriv_pred.shape[0]

    error_rate_ratio = unpriv_error_rate / priv_error_rate

    if (num_priv_pos == 0):
        disp_impact = 2
    else:
        disp_impact = (num_unpriv_pos/unpriv_pred.shape[0]) / (num_priv_pos/priv_pred.shape[0])
    save_disp_impact_img(disp_impact, features_edit)
    save_err_ratio_img(error_rate_ratio, features_edit)

    coef = pd.concat([pd.DataFrame(x_train.columns),pd.DataFrame(np.abs(np.transpose(model.coef_)))], axis = 1)
    


def save_disp_impact_img(disp_impact, features):
  plt.clf()
  #print('Plot for:')
  #print(features)
  #fig, axs = plt.subplots(1, 2)
  x = [1]
  di_y = [disp_impact]
  plt.ylim(bottom = 0, top = 2)
  plt.xlim(left = 0, right = 2)

  ax = plt.gca()
  ax.axes.xaxis.set_visible(False)

  plt.bar(x, di_y, width = 0.6)
  plt.axhline(y=1.25, xmin=0, xmax=2, linestyle='--', color='black')
  plt.axhline(y=1, xmin=0, xmax=2, linestyle='--', color='green')
  plt.axhline(y=0.75, xmin=0, xmax=2, linestyle='--', color='black')

  plt.title('Disparate Impact')
  filename = 'disp_impact_' + str(features).replace(" ","")
  plt.savefig(filename)

def save_err_ratio_img(err_ratio, features):
  plt.clf()
  x = [1]
  er_y = [err_ratio]
  plt.ylim(bottom = 0, top = 2)
  plt.xlim(left = 0, right = 2)

  ax = plt.gca()
  ax.axes.xaxis.set_visible(False)

  plt.bar(x, er_y, width = 0.6)
  plt.axhline(y=1.25, xmin=0, xmax=2, linestyle='--', color='black')
  plt.axhline(y=1, xmin=0, xmax=2, linestyle='--', color='green')
  plt.axhline(y=0.8, xmin=0, xmax=2, linestyle='--', color='black')

  plt.title('Error Rate Ratio')
  filename = 'err_ratio_' + str(features).replace(" ","")
  plt.savefig(filename)
