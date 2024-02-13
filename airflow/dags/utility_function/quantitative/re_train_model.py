import pandas as pd
import numpy as np
import pickle
import json

from utility_function.quantitative.prepare_quanti_data_processing import load_prepare_data
import random

from datetime import datetime, timedelta, date
import os, shutil

from functools import partial

#import lib use to train model
from xgboost import XGBClassifier
import xgboost as xgb
import lightgbm as lgb
from lightgbm import LGBMClassifier
from module_superlearner.superlearner_model import SuperLearnerClassifier

from sklearn import linear_model
from sklearn import ensemble
from sklearn import tree
from sklearn import neighbors
from sklearn import svm
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

def write_param_to_jsonfile(dict_param, file_name):
    with open(file_name, "w") as file:
        json.dump(dict_param, file)

def read_jsonfile_to_dict(file_name):
    with open(file_name, "r") as file:
        data = json.load(file)
    return data

def evaluate_train_model(y_pred, y_true):
    def accuracy_prob(y_pred, y_true):
        acc = (y_pred == y_true).mean()
        return round(acc, 3)

    def sensitivity(tp, fn):
        sen = tp / (tp + fn + 1e-6)
        return round(sen, 3)

    def specificity(tn, fp):
        spec = tn / (tn + fp + 1e-6)
        return round(spec, 3)

    # Calculate predictions and confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    # Compute evaluation metrics
    accuracy = accuracy_prob(y_pred, y_true)
    specificity_score = specificity(tn, fp)
    precision = round(precision_score(y_true, y_pred), 3)
    recall = round(recall_score(y_true, y_pred), 3)
    f1 = round(f1_score(y_true, y_pred), 3)
    tpr = sensitivity(tp, fn)
    tnr = specificity_score
    fnr = round(fn / (fn + tp + 1e-6), 3)
    fpr = round(fp / (fp + tn + 1e-6), 3)

    dict_confusion_matrix = {
        'val_acc': accuracy,
        'val_specificity': specificity_score,
        'val_precision': precision,
        'val_recall': recall,
        'val_f1': f1,
        'val_fnr': fnr,
        'val_tpr': tpr,
        'val_tnr': tnr,
        'val_fpr': fpr,
    }

    return dict_confusion_matrix

def tune_param_xgb_or_lgbm(algorithm, feat, Y):
    def tuned_model_indivi_bayessearch(model, param):
  
        print(np.__version__)
        # outer_cv = KFold(10)
        outer_cv = LeaveOneOut()
        tuned_model = BayesSearchCV(model, param, n_iter=60, n_jobs=-1, scoring="accuracy", cv=outer_cv)
        return tuned_model, outer_cv

    if algorithm == 'lgbm':
        param = {
            'max_depth': Integer(1, 20),
            'num_leaves': Integer(20, 100),
            'min_data_in_leaf': Integer(1, 100),
            'learning_rate': Real(.1, 1.)
        }
        model = LGBMClassifier()
    elif algorithm == 'xgb':
        param = {
            'learning_rate': Real(.05, .1 + .05),  # lower bound and upper bound
            'objective': ['binary:logistic'],
            'subsample': Real(.2, .5),
            'n_estimators': Integer(20, 70),
            'min_child_weight': Integer(20, 40),
            'reg_alpha': Real(0, 0 + .7),
            'reg_lambda': Real(0, 0 + .7),
            'colsample_bytree': Real(.1, .1 + .7),
            'max_depth': Integer(2, 6)
        }
        model = XGBClassifier()
  
    search_cv, cv_corr = tuned_model_indivi_bayessearch(model, param)
    search_cv.fit(feat, Y)

    if algorithm == 'xgb':
        model_search_cv = XGBClassifier(**search_cv.best_params_)
    elif algorithm == 'lgbm':
        model_search_cv = LGBMClassifier(**search_cv.best_params_)

    return model_search_cv

def tune_param_superleaner(feat, Y, tune_param_estimators):
    
    def tuned_model_with_grid(model, param):
        print(np.__version__)
        outer_cv = LeaveOneOut()
        tuned_model = GridSearchCV(model, param, scoring="accuracy", cv=outer_cv, n_jobs=-1)
        return tuned_model, outer_cv
    
    tune_param = {
            'estimators': tune_param_estimators,
            'cv_folds': [5, 10, 15, 20],
            'proba_2train_meta': [False, True],
            'ori_input_2train_meta': [False, True],
            'meta_model_type': ['DCT'],
    }
    model = SuperLearnerClassifier(n_classes=2)
    search_cv, cv_corr = tuned_model_with_grid(model, tune_param)
    search_cv.fit(feat, Y)
    model_search_cv = SuperLearnerClassifier(n_classes=2, **search_cv.best_params_)

    return model_search_cv


def re_xgb_model(dict_data_set, target):
    # Get variable environment
    path_model_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'model_temp')
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    
    # Find parameter
    algorithm = "xgb"
    bool_tune = True
    if bool_tune == True:
        re_train_model = tune_param_xgb_or_lgbm(algorithm, dict_data_set['X_train'], dict_data_set['y_train'])
        dict_param = re_train_model.get_params()
    else: 
        re_train_model = XGBClassifier(colsample_bytree=0.24339155273785987, 
                                  learning_rate=0.05427936367489443, 
                                  max_depth=2, min_child_weight=20, 
                                  n_estimators=20, 
                                  objective='binary:logistic',
                                  reg_alpha=0.5214797957799494,
                                  reg_lambda=0.023396660664372935,
                                  subsample=0.5)
        dict_param = re_train_model.get_xgb_params()

    # Train model
    model_fit = re_train_model.fit(dict_data_set['X_train'], dict_data_set['y_train'])
    y_pred_test = model_fit.predict(dict_data_set['X_test'])
    y_pred_train = model_fit.predict(dict_data_set['X_train'])


    # Save model and parameter in temporary folder
    dpath_model = os.path.join(path_model_temp, f"re-train/{target.upper()}/{algorithm}")
    try:
        print(f'>>>>> createt directory: {dpath_model}')
        os.makedirs(dpath_model)
    except Exception as e:
        print(f'>>>>> remove all file in directory: {dpath_model}')
        list_file_name = os.listdir(dpath_model)
        # Delect file
        if len(list_file_name) != 0:
            for filename in list_file_name:
                file_path = os.path.join(dpath_model, filename)
                try: # Check file or directory 
                    if os.path.isfile(file_path): 
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                     raise Exception(e)

    # Save parameter in temporary folder
    version = (datetime.now() + timedelta(hours=7)).strftime('%d-%m-%Y')
    filename_parameter = f"{version}_{target.lower()}_{algorithm}_quantitative_re-train_parameter.json"
    write_param_to_jsonfile(dict_param, os.path.join(dpath_model, filename_parameter))
    
    # Evaluate model
    print('>>>>> Form train data: ', evaluate_train_model(y_pred=y_pred_train, y_true=dict_data_set['y_train']))
    dict_evaluate = evaluate_train_model(y_pred=y_pred_test, y_true=dict_data_set['y_test'])
    print('>>>>> Form test data: ', dict_evaluate)

    dict_evaluate_model = {
        'type': 'Fully Re-train', 
        'target': target,
        'val_acc': dict_evaluate['val_acc'],
        'val_specificity': dict_evaluate['val_specificity'],
        'val_precision': dict_evaluate['val_precision'],
        'val_recall': dict_evaluate['val_recall'],
        'val_f1': dict_evaluate['val_f1'],
        'val_fnr': dict_evaluate['val_fnr'],
        'val_tpr': dict_evaluate['val_tpr'],
        'val_tnr': dict_evaluate['val_tnr'],
        'val_fpr': dict_evaluate['val_fpr'],
        'brand_quanti_model': algorithm,
        'model_dpath': dpath_model,
        'type_evaluate': 're-train_model'
    }
    #------------------------------- model mockup ----------------------------
    # random.seed(5)
    # p = round(random.random(), 3)
    # n = round(random.random(), 3)
    # val_acc = round(random.random(), 3)
    # # if target == 'LAD':
    # #     val_acc = 1
    # dict_evaluate_model = {
    #     'type': 'Fully Re-train',
    #     'target': target,
    #     'val_acc': val_acc,
    #     'val_specificity': round(random.random(), 3),
    #     'val_precision': round(random.random(), 3),
    #     'val_recall': round(random.random(), 3),
    #     'val_f1': round(random.random(), 3),
    #     'val_fnr': 1-n,
    #     'val_tpr': p,
    #     'val_tnr': n,
    #     'val_fpr': 1-p,
    #     'brand_quanti_model': 'xgb',
    #     'model_dpath': dpath_model,
    #     'type_evaluate': 're-train_model'
    # }
    return dict_evaluate_model

def re_lgbm_model(dict_data_set, target):
    # Get variable environment
    path_model_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'model_temp')
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')

    #Find parameter 
    algorithm = "lgbm"
    bool_tune = True
    if bool_tune == True:
        re_train_model = tune_param_xgb_or_lgbm(algorithm, dict_data_set['X_train'], dict_data_set['y_train'])
        print('tune_param_xgb_or_lgbm 100%')
        dict_param = re_train_model.get_params()
    else: 
        re_train_model = LGBMClassifier(
        learning_rate=0.10984644713678246,
        max_depth=1,
        min_data_in_leaf=96,
        num_leaves=21)
        dict_param = re_train_model.get_params()

    # Train model
    model_fit = re_train_model.fit(dict_data_set['X_train'], dict_data_set['y_train'])
    y_pred_test = model_fit.predict(dict_data_set['X_test'])
    y_pred_train = model_fit.predict(dict_data_set['X_train'])


    # Save model and parameter in temporary folder
    dpath_model = os.path.join(path_model_temp, f"re-train/{target.upper()}/{algorithm}")
    try:
        print(f'>>>>> createt directory: {dpath_model}')
        os.makedirs(dpath_model)
    except Exception as e:
        print(f'>>>>> remove all file in directory: {dpath_model}')
        list_file_name = os.listdir(dpath_model)
        # Delect file
        if len(list_file_name) != 0:
            for filename in list_file_name:
                file_path = os.path.join(dpath_model, filename)
                try: # Check file or directory 
                    if os.path.isfile(file_path): 
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                     raise Exception(e)

    # Save parameter in temporary folder
    version = (datetime.now() + timedelta(hours=7)).strftime('%d-%m-%Y')
    filename_parameter = f"{version}_{target.lower()}_{algorithm}_quantitative_re-train_parameter.json"
    write_param_to_jsonfile(dict_param, os.path.join(dpath_model, filename_parameter))

    # Evaluate model
    print('>>>>> Form train data: ', evaluate_train_model(y_pred=y_pred_train, y_true=dict_data_set['y_train']))
    dict_evaluate = evaluate_train_model(y_pred=y_pred_test, y_true=dict_data_set['y_test'])
    print('>>>>> Form test data: ', dict_evaluate)

    dict_evaluate_model = {
        'type': 'Fully Re-train', 
        'target': target,
        'val_acc': dict_evaluate['val_acc'],
        'val_specificity': dict_evaluate['val_specificity'],
        'val_precision': dict_evaluate['val_precision'],
        'val_recall': dict_evaluate['val_recall'],
        'val_f1': dict_evaluate['val_f1'],
        'val_fnr': dict_evaluate['val_fnr'],
        'val_tpr': dict_evaluate['val_tpr'],
        'val_tnr': dict_evaluate['val_tnr'],
        'val_fpr': dict_evaluate['val_fpr'],
        'brand_quanti_model': algorithm,
        'model_dpath': dpath_model,
        'type_evaluate': 're-train_model'
    }
    # # ------------------------------- evaluate model mockup ----------------------------
    # # print('re_lgbm_model')
    # random.seed(2)
    # p = round(random.random(), 3)
    # n = round(random.random(), 3)
    # val_acc = round(random.random(), 3)
    # # if target == 'LCX':
    # #     val_acc = 1
    # dict_evaluate_model = {
    #     'type': 'Fully Re-train',
    #     'target': target,
    #     'val_acc': val_acc,
    #     'val_specificity': round(random.random(), 3),
    #     'val_precision': round(random.random(), 3),
    #     'val_recall': round(random.random(), 3),
    #     'val_f1': round(random.random(), 3),
    #     'val_fnr': 1-n,
    #     'val_tpr': p,
    #     'val_tnr': n,
    #     'val_fpr': 1-p,
    #     'brand_quanti_model': 'lgbm',
    #     'model_dpath': dpath_model,
    #     'type_evaluate': 're-train_model'
    # }
    return dict_evaluate_model

def re_superlearner_model(dict_data_set, target):
    # Get variable environment 
    path_model_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'model_temp')
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    
    # Find parameter 
    algorithm = "superlearner"
    bool_tune = True
    if bool_tune == True:
        tune_param_estimators = [[tree.DecisionTreeClassifier(criterion='entropy', max_depth=10),
                tree.ExtraTreeClassifier(),
                linear_model.LogisticRegression(),
                svm.NuSVC(probability=True),
                svm.SVC(probability=True),
                neighbors.KNeighborsClassifier(n_neighbors=5)]]
        
        re_train_model = tune_param_superleaner(dict_data_set['X_train'], dict_data_set['y_train'], tune_param_estimators)
        dict_param = re_train_model.get_params()
    else:
        re_train_model = SuperLearnerClassifier(n_classes=2, meta_model_type="DCT")
        dict_param = re_train_model.get_params()

    model_fit = re_train_model.fit(dict_data_set['X_train'], dict_data_set['y_train'])
    y_pred_test = model_fit.predict(dict_data_set['X_test'])
    y_pred_train = model_fit.predict(dict_data_set['X_train'])

    # Save model and parameter in temporary folder
    dpath_model = os.path.join(path_model_temp, f"re-train/{target.upper()}/{algorithm}")
    try:
        print(f'>>>>> createt directory: {dpath_model}')
        os.makedirs(dpath_model)
    except Exception as e:
        print(f'>>>>> remove all file in directory: {dpath_model}')
        list_file_name = os.listdir(dpath_model)
        # Delect file
        if len(list_file_name) != 0:
            for filename in list_file_name:
                file_path = os.path.join(dpath_model, filename)
                try: # Check file or directory 
                    if os.path.isfile(file_path): 
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                     raise Exception(e)

    # Save parameter in temporary folder
    version = (datetime.now() + timedelta(hours=7)).strftime('%d-%m-%Y')
    filename_parameter = f"{version}_{target.lower()}_{algorithm}_quantitative_re-train_parameter.pickle"
    dict_param = re_train_model.get_params()
    with open(os.path.join(dpath_model, filename_parameter), 'wb') as filename:
        pickle.dump(dict_param, filename)
    
    # Evaluate model
    print('>>>>> Form train data: ', evaluate_train_model(y_pred=y_pred_train, y_true=dict_data_set['y_train']))
    dict_evaluate = evaluate_train_model(y_pred=y_pred_test, y_true=dict_data_set['y_test'])
    print('>>>>> Form test data: ', dict_evaluate)

    dict_evaluate_model = {
        'type': 'Fully Re-train', 
        'target': target,
        'val_acc': dict_evaluate['val_acc'],
        'val_specificity': dict_evaluate['val_specificity'],
        'val_precision': dict_evaluate['val_precision'],
        'val_recall': dict_evaluate['val_recall'],
        'val_f1': dict_evaluate['val_f1'],
        'val_fnr': dict_evaluate['val_fnr'],
        'val_tpr': dict_evaluate['val_tpr'],
        'val_tnr': dict_evaluate['val_tnr'],
        'val_fpr': dict_evaluate['val_fpr'],
        'brand_quanti_model': algorithm,
        'model_dpath': dpath_model,
        'type_evaluate': 're-train_model'
    }
    print(dict_evaluate_model)

    # ------------------------------- evaluate model mockup ----------------------------
    # print('re_superlearner_model')
    # random.seed(10)
    # p = round(random.random(), 3)
    # n = round(random.random(), 3)
    # val_acc = round(random.random(), 3)
    # # if target == 'LAD':
    # #     val_acc = 1
    # dict_evaluate_model = {
    #     'type': 'Fully Re-train',
    #     'target': target,
    #     'val_acc': val_acc,
    #     'val_specificity': round(random.random(), 3),
    #     'val_precision': round(random.random(), 3),
    #     'val_recall': round(random.random(), 3),
    #     'val_f1': round(random.random(), 3),
    #     'val_fnr': 1-n,
    #     'val_tpr': p,
    #     'val_tnr': n,
    #     'val_fpr': 1-p,
    #     'brand_quanti_model': 'superlearner',
    #     'model_dpath': dpath_model,
    #     'type_evaluate': 're-train_model'
    # }
    return dict_evaluate_model

def lad_xgb_re_train(**kwargs):
    ti = kwargs['ti']
    dict_data_set = load_prepare_data(target='lad')
    dict_evaluate_model = re_xgb_model(dict_data_set=dict_data_set, target='LAD')
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def lcx_xgb_re_train(**kwargs):
    ti = kwargs['ti']
    dict_data_set = load_prepare_data(target='lcx')
    dict_evaluate_model = re_xgb_model(dict_data_set=dict_data_set, target='LCX')
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def rca_xgb_re_train(**kwargs):
    ti = kwargs['ti']
    dict_data_set = load_prepare_data(target='rca')
    dict_evaluate_model = re_xgb_model(dict_data_set=dict_data_set, target='RCA')
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def patient_xgb_re_train(**kwargs):
    ti = kwargs['ti']
    dict_data_set = load_prepare_data(target='patient')
    dict_evaluate_model = re_xgb_model(dict_data_set=dict_data_set, target='PATIENT')
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def lad_lgbm_re_train(**kwargs):
    ti = kwargs['ti']
    dict_data_set = load_prepare_data(target='lad')
    dict_evaluate_model = re_lgbm_model(dict_data_set=dict_data_set, target='LAD')
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def lcx_lgbm_re_train(**kwargs):
    ti = kwargs['ti']
    dict_data_set = load_prepare_data(target='lcx')
    dict_evaluate_model = re_lgbm_model(dict_data_set=dict_data_set, target='LCX')
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def rca_lgbm_re_train(**kwargs):
    ti = kwargs['ti']
    dict_data_set = load_prepare_data(target='rca')
    dict_evaluate_model = re_lgbm_model(dict_data_set=dict_data_set, target='RCA')
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def patient_lgbm_re_train(**kwargs):
    ti = kwargs['ti']
    dict_data_set = load_prepare_data(target='patient')
    dict_evaluate_model = re_lgbm_model(dict_data_set=dict_data_set, target='PATIENT')
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def lad_superlearner_re_train(**kwargs):
    ti = kwargs['ti']
    dict_data_set = load_prepare_data(target='lad')
    dict_evaluate_model = re_superlearner_model(dict_data_set=dict_data_set, target='LAD')
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def lcx_superlearner_re_train(**kwargs):
    ti = kwargs['ti']
    dict_data_set = load_prepare_data(target='lcx')
    dict_evaluate_model = re_superlearner_model(dict_data_set=dict_data_set, target='LCX')
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def rca_superlearner_re_train(**kwargs):
    ti = kwargs['ti']
    dict_data_set = load_prepare_data(target='rca')
    dict_evaluate_model = re_superlearner_model(dict_data_set=dict_data_set, target='RCA')
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def patient_superlearner_re_train(**kwargs):
    ti = kwargs['ti']
    dict_data_set = load_prepare_data(target='patient')
    dict_evaluate_model = re_superlearner_model(dict_data_set=dict_data_set, target='PATIENT')
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)
