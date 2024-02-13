import pandas as pd
import numpy as np
import pickle

from utility_function.quantitative.prepare_quanti_data_processing import load_prepare_data
import os, shutil
from glob import glob
import xgboost as xgb
import lightgbm as lgb
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

def score_model(y_pred, y_true):
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

def evaluate_model(dict_data_set, info_model):
    # Load evaluate model
    dpath_model = info_model.model_dpath.values[0] 
    brand = info_model.brand_quanti_model.values[0]
    p_file_model = glob(f"{dpath_model}/*model*")[0] 
    target = info_model.target.values[0]
    print(f'>>>>> {target}: model_dpath ', dpath_model)
    with open(p_file_model, 'rb') as model_file:
        old_model = pickle.load(model_file)

    # Check the type of the model and predict
    if brand == 'xgb':
        if isinstance(old_model, xgb.core.Booster):
            y_pred = old_model.predict(xgb.DMatrix(dict_data_set['X_test']))
            y_pred[y_pred >= 0.5] = 1
            y_pred[y_pred < 0.5] = 0
        elif isinstance(old_model, xgb.XGBClassifier):
            y_pred = old_model.predict(dict_data_set['X_test'])
    elif brand == 'lgbm':
        if isinstance(old_model, lgb.basic.Booster):
            y_pred = old_model.predict(dict_data_set['X_test'])
            y_pred[y_pred >= 0.5] = 1
            y_pred[y_pred < 0.5] = 0
        elif isinstance(old_model, lgb.LGBMClassifier):
            y_pred = old_model.predict(dict_data_set['X_test'])
    elif brand == 'superlearner':
            y_pred = old_model.predict(dict_data_set['X_test'])
    else:
        raise ValueError(f"Unknown model type from dpath '{dpath_model}'")
    # Evaluate model
    score_evaluate = score_model(y_pred=y_pred, y_true=dict_data_set['y_test'])
    print('>>>>> Form test data: ', score_evaluate)

    # Return result evaluate model 
    dict_evaluate_model = { 
        'type': info_model.type.values[0],
        'target': target,
        'val_acc': score_evaluate['val_acc'],
        'val_specificity': score_evaluate['val_specificity'],
        'val_precision': score_evaluate['val_precision'],
        'val_recall': score_evaluate['val_recall'],
        'val_f1': score_evaluate['val_f1'],
        'val_fnr': score_evaluate['val_fnr'],
        'val_tpr': score_evaluate['val_tpr'],
        'val_tnr': score_evaluate['val_tnr'],
        'val_fpr': score_evaluate['val_fpr'],
        'brand_quanti_model': brand,
        'model_dpath': '',
        'type_evaluate': 'current_model'
    }

    return dict_evaluate_model

def lad_evaluate_model(**kwargs):
    ti = kwargs['ti']

    # Load infomation current model
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    df_info_all_model = pd.read_csv(os.path.join(path_data_temp, f"info_current_model.csv"))
    condition_qurey_model = "target == 'LAD' & is_best == True"
    info_model = df_info_all_model.query(condition_qurey_model)

    # Get brand model? (xgb, lgbm, superlearner)
    brand_model = info_model.brand_quanti_model.values[0]
    print('>>>>> LAD: brand_model ',brand_model)

    # Load data
    dict_data_set = load_prepare_data(target='lad')

    # Evaluate lad current model
    dict_evaluate_model = evaluate_model(dict_data_set=dict_data_set, info_model=info_model)

    # Push result evaluate model
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)


def lcx_evaluate_model(**kwargs):
    ti = kwargs['ti']

    # Load infomation current model
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    df_info_all_model = pd.read_csv(os.path.join(path_data_temp, f"info_current_model.csv"))
    condition_qurey_model = "target == 'LCX' & is_best == True"
    info_model = df_info_all_model.query(condition_qurey_model)

    # Get brand model? (xgb, lgbm, superlearner)
    brand_model = info_model.brand_quanti_model.values[0]
    print('>>>>> LCX: brand_model ',brand_model)

    # Load data
    dict_data_set = load_prepare_data(target='lcx')

    # Evaluate lad current model
    dict_evaluate_model = evaluate_model(dict_data_set=dict_data_set, info_model=info_model)

    # Push result evaluate model
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)


def rca_evaluate_model(**kwargs):
    ti = kwargs['ti']

    # Load infomation current model
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    df_info_all_model = pd.read_csv(os.path.join(path_data_temp, f"info_current_model.csv"))
    condition_qurey_model = "target == 'RCA' & is_best == True"
    info_model = df_info_all_model.query(condition_qurey_model)

    # Get brand model? (xgb, lgbm, superlearner)
    brand_model = info_model.brand_quanti_model.values[0]
    print('>>>>> RCA: brand_model ',brand_model)

    # Load data
    dict_data_set = load_prepare_data(target='rca')

    # Evaluate lad current model
    dict_evaluate_model = evaluate_model(dict_data_set=dict_data_set, info_model=info_model)

    # Push result evaluate model
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def patient_evaluate_model(**kwargs): 
    ti = kwargs['ti']

    # load infomation current model
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    df_info_all_model = pd.read_csv(os.path.join(path_data_temp, f"info_current_model.csv"))
    condition_qurey_model = "target == 'PATIENT' & is_best == True"
    info_model = df_info_all_model.query(condition_qurey_model)

    # get brand model? (xgb, lgbm, superlearner)
    brand_model = info_model.brand_quanti_model.values[0]
    print('>>>>> PATIENT: brand_model ',brand_model)

    # load data
    dict_data_set = load_prepare_data(target='patient')

    # evaluate lad current model
    dict_evaluate_model = evaluate_model(dict_data_set=dict_data_set, info_model=info_model)

    # push result evaluate model
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)
