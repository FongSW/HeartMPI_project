import pandas as pd
import numpy as np
import pickle
import random
import json
import os, shutil
from glob import glob
from dateutil import parser
from datetime import datetime, timedelta
import ast
from xgboost import XGBClassifier
import xgboost as xgb
import lightgbm as lgb
from lightgbm import LGBMClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

from utility_function.quantitative.re_train_model import tune_param_xgb_or_lgbm
from utility_function.quantitative.prepare_quanti_data_processing import load_prepare_data

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
    print(dict_confusion_matrix)
    return dict_confusion_matrix

def incre_xgb_model(dict_data_set, info_model):
    # Get variable environment
    path_model_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'model_temp')

    # Load model and paremeter (mockup) 
    dpath_model = info_model.model_dpath.values[0]
    target = info_model.target.values[0]
    p_file_model = glob(f"{dpath_model}/*model*")[0] 
    target = info_model.target.values[0]
    print(f'>>>>> {target}: model_dpath ', dpath_model)
    
    # Find parameter 
    algorithm = "xgb"
    bool_tune = True

    if bool_tune == True:
        re_train_model = tune_param_xgb_or_lgbm(algorithm, dict_data_set['X_train'], dict_data_set['y_train'])
        best_param = re_train_model.get_params()
    else: 
        best_param = {'colsample_bytree': 0.24339155273785987, 
                                  'learning_rate': 0.05427936367489443, 
                                  'max_depth': 2,
                                  'min_child_weight': 20, 
                                  'n_estimators': 20, 
                                  'objective': 'binary:logistic',
                                  'reg_alpha': 0.5214797957799494,
                                  'reg_lambda': 0.023396660664372935,
                                  'subsample': 0.5}
        
    # Load the old model
    with open(p_file_model, 'rb') as model_file:
        booster_model = pickle.load(model_file)

    # Prepare DMatrix for training data
    untrain_data = xgb.DMatrix(dict_data_set['X_untrain'], label=dict_data_set['y_untrain'])
    x_test = xgb.DMatrix(dict_data_set['X_test'])
    x_train = xgb.DMatrix(dict_data_set['X_all'])

    # Train the model
    dpath_temp_model = os.path.join(path_model_temp, f"incremental/{target.upper()}")
    path_text_model = os.path.join(dpath_temp_model, 'xgb_structure.txt')
    
    # Create directory
    try:
        print(f'>>>>> createt directory: {dpath_temp_model}')
        os.makedirs(dpath_temp_model)
    except Exception as e:
        print(f'>>>>> remove all file in directory: {dpath_temp_model}')
        list_file_name = os.listdir(dpath_temp_model)
        # Delect file
        if len(list_file_name) != 0:
            for filename in list_file_name:
                file_path = os.path.join(dpath_temp_model, filename)
                try: # Check file or directory 
                    if os.path.isfile(file_path): 
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                     raise Exception(e)
                 
    # Train the model
    booster_model.save_model(path_text_model)
    tranfer_model = xgb.train(best_param, untrain_data, 60, xgb_model=path_text_model)

    y_pred_test = tranfer_model.predict(x_test)
    y_pred_test[y_pred_test >= 0.5] = 1
    y_pred_test[y_pred_test < 0.5] = 0
    y_pred_train = tranfer_model.predict(x_train)
    y_pred_train[y_pred_train >= 0.5] = 1
    y_pred_train[y_pred_train < 0.5] = 0

    # Evaluate model
    print('>>>>> Form train data: ', evaluate_train_model(y_pred=y_pred_train, y_true=dict_data_set['y_all']))
    dict_evaluate = evaluate_train_model(y_pred=y_pred_test, y_true=dict_data_set['y_test'])
    print('>>>>> Form test data: ', dict_evaluate)

    version = (datetime.now() + timedelta(hours=7)).strftime('%d-%m-%Y')
    brand_model = 'xgb'
    filename_parameter = f"{version}_{target.lower()}_{brand_model}_quantitative_incremental_parameter.json"
    write_param_to_jsonfile(best_param, os.path.join(dpath_temp_model, filename_parameter))

    # Result evaluate model
    dict_evaluate_model = {
        'type': 'Incremental', 
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
        'brand_quanti_model': 'xgb',
        'model_dpath': dpath_temp_model,
        'type_evaluate': 'incremental_model'
    }
    # ------------------- save evaluate model (mockup) -------------------------------
    # # Random score (mockup) 
    # random.seed(6)
    # p = round(random.random(), 3)
    # n = round(random.random(), 3)
    # val_acc = round(random.random(), 3)
    
    # if target == 'LAD':
    #     val_acc = 1
    # dict_evaluate_model = {
    #     'type': 'Incremental',
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
    #     'model_dpath': dpath_temp_model,
    #     'type_evaluate': 'incremental_model'
    # }

    return dict_evaluate_model

def incre_lgbm_model(dict_data_set, info_model):
    # Get variable environment
    path_model_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'model_temp')
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')

    # Load model and paremeter 
    dpath_model = info_model.model_dpath.values[0]
    print('dpathmodel', dpath_model)
    p_file_model = glob(f"{dpath_model}/*model*")[0]
    old_model = pickle.load(open(p_file_model, 'rb'))
    target = info_model.target.values[0]
    print(f'>>>>> {target}: model_dpath ', dpath_model)
    
    #Find parameter
    algorithm = "lgbm"
    bool_tune = True

    if bool_tune == True:
        re_train_model = tune_param_xgb_or_lgbm(algorithm, dict_data_set['X_train'], dict_data_set['y_train'])
        print('tune_param_xgb_or_lgbm 100%')
        best_param = re_train_model.get_params()
    else: 
        best_param = {
        'learning_rate': 0.10984644713678246,
        'max_depth': 1,
        'min_data_in_leaf': 96,
        'num_leaves': 21
        }
    print('>>>>> parameter use incremental model:', best_param)
    # Check the type of the model
    if isinstance(old_model, lgb.basic.Booster):
        booster_model = old_model
    elif isinstance(old_model, lgb.LGBMClassifier):
        booster_model = old_model.booster_
    else:
        raise ValueError("Unknown model type")

    untrain_data = lgb.Dataset(dict_data_set['X_untrain'], label=dict_data_set['y_untrain'], free_raw_data=False)

    # # Train model
    tranfer_model = lgb.train(best_param, train_set=untrain_data, init_model=booster_model, num_boost_round=10, keep_training_booster=True)
    print(type(tranfer_model))

    # Evaluate model
    y_pred_test = tranfer_model.predict(dict_data_set['X_test'])
    y_pred_train = tranfer_model.predict(dict_data_set['X_all'])
    y_pred_test[y_pred_test >= 0.5] = 1
    y_pred_test[y_pred_test < 0.5] = 0
    y_pred_train[y_pred_train >= 0.5] = 1
    y_pred_train[y_pred_train < 0.5] = 0

    print('>>>>> Form train data: ', evaluate_train_model(y_pred=y_pred_train, y_true=dict_data_set['y_all']))
    dict_evaluate = evaluate_train_model(y_pred=y_pred_test, y_true=dict_data_set['y_test'])
    print('>>>>> Form test data: ', dict_evaluate)

    # Create directory
    dpath_temp_model = os.path.join(path_model_temp, f"incremental/{target.upper()}")
    try:
        print(f'>>>>> createt directory: {dpath_temp_model}')
        os.makedirs(dpath_temp_model)
    except Exception as e:
        print(f'>>>>> remove all file in directory: {dpath_temp_model}')
        list_file_name = os.listdir(dpath_temp_model)
        # Delect file
        if len(list_file_name) != 0:
            for filename in list_file_name:
                file_path = os.path.join(dpath_temp_model, filename)
                try: # Check file or directory 
                    if os.path.isfile(file_path): 
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                     raise Exception(e)
                 
    # Save model and parameter in temporary folder
    version = (datetime.now() + timedelta(hours=7)).strftime('%d-%m-%Y')
    brand_model = 'lgbm'
    filename_parameter = f"{version}_{target.lower()}_{brand_model}_quantitative_incremental_parameter.json"
    write_param_to_jsonfile(best_param, os.path.join(dpath_temp_model, filename_parameter))

    dict_evaluate_model = {
        'type': 'Incremental', 
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
        'brand_quanti_model': 'lgbm',
        'model_dpath': dpath_temp_model,
        'type_evaluate': 'incremental_model'
    }
    # ------------------- save evaluate model (mockup) -------------------------------
    # # Ramdom score (mockup) 
    # random.seed(10)
    # p = round(random.random(), 3)
    # n = round(random.random(), 3)
    # val_acc = round(random.random(), 3)
    # if target == 'LCX':
    #     val_acc = 1
    # dict_evaluate_model = {
    #     'type': 'Incremental', 
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
    #     'model_dpath': dpath_temp_model,
    #     'type_evaluate': 'incremental_model'
    # }



    return dict_evaluate_model

def lad_train_incre_model(**kwargs):
    ti = kwargs['ti']

    # Load infomation current model
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    df_info_all_model = pd.read_csv(os.path.join(path_data_temp, f"info_current_model.csv"))
    condition_qurey_model = "target == 'LAD' & is_best == True & name == 'Adaptive'" 
    info_model = df_info_all_model.query(condition_qurey_model)

    # Get brand model? (xgb, lgbm, superlearner)
    brand_model = info_model.brand_quanti_model.values[0]
    print('>>>>> LAD: brand_model ',brand_model)
    
    # Load data
    dict_data_set = load_prepare_data(target='lad')

    # Check brand model and train model
    if brand_model == 'xgb':
        dict_evaluate_model = incre_xgb_model(dict_data_set=dict_data_set, info_model=info_model)
    elif brand_model == 'lgbm':
        dict_evaluate_model = incre_lgbm_model(dict_data_set=dict_data_set, info_model=info_model)
    else:
        print(f'>>>>> This {brand_model} model cannot incremental learning')
        dict_evaluate_model = {'type': 'Incremental', 'target': 'LAD', 'brand_quanti_model': brand_model}
    
    # Push result evaluate model
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def lcx_train_incre_model(**kwargs):
    ti = kwargs['ti']

    # Load infomation current model
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    df_info_all_model = pd.read_csv(os.path.join(path_data_temp, f"info_current_model.csv"))
    condition_qurey_model = "target == 'LCX' & is_best == True & name == 'Adaptive'"
    info_model = df_info_all_model.query(condition_qurey_model)

    # Get brand model? (xgb, lgbm, superlearner)
    brand_model = info_model.brand_quanti_model.values[0]
    print('>>>>> LCX: brand_model ',brand_model)

    # Load data
    dict_data_set = load_prepare_data(target='lcx')

    # Check brand model and train model
    if brand_model == 'xgb':
        dict_evaluate_model = incre_xgb_model(dict_data_set=dict_data_set, info_model=info_model)
    elif brand_model == 'lgbm':
        dict_evaluate_model = incre_lgbm_model(dict_data_set=dict_data_set, info_model=info_model)
    else:
        print(f'>>>>> This {brand_model} model cannot incremental learning')
        dict_evaluate_model = {'type': 'Incremental', 'target': 'LCX', 'brand_quanti_model': brand_model}
    
    # Push result evaluate model
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def rca_train_incre_model(**kwargs):

    ti = kwargs['ti']

    # Load infomation current model
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    df_info_all_model = pd.read_csv(os.path.join(path_data_temp, f"info_current_model.csv"))
    condition_qurey_model = "target == 'RCA' & is_best == True & name == 'Adaptive'"
    info_model = df_info_all_model.query(condition_qurey_model)

    # Get brand model? (xgb, lgbm, superlearner)
    brand_model = info_model.brand_quanti_model.values[0]
    print('>>>>> RCA: brand_model ',brand_model)

    # Load data
    dict_data_set = load_prepare_data(target='rca')

    # Check brand model and train model
    if brand_model == 'xgb': 
        dict_evaluate_model = incre_xgb_model(dict_data_set=dict_data_set, info_model=info_model)
    elif brand_model == 'lgbm':
        dict_evaluate_model = incre_lgbm_model(dict_data_set=dict_data_set, info_model=info_model)
    else:
        print(f'>>>>> This {brand_model} model cannot incremental learning')
        dict_evaluate_model = {'type': 'Incremental', 'target': 'RCA', 'brand_quanti_model': brand_model}
    
    # push result evaluate model
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)

def patient_train_incre_model(**kwargs):

    ti = kwargs['ti']

    # Load infomation current model
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    df_info_all_model = pd.read_csv(os.path.join(path_data_temp, f"info_current_model.csv"))
    condition_qurey_model = "target == 'PATIENT' & is_best == True & name == 'Adaptive'"
    info_model = df_info_all_model.query(condition_qurey_model)

    # Get brand model? (xgb, lgbm, superlearner)
    brand_model = info_model.brand_quanti_model.values[0]
    print('>>>>> PATIENT: brand_model ',brand_model)

    # Load data
    dict_data_set = load_prepare_data(target='patient') 

    # Check brand model and train model
    if brand_model == 'xgb':
        dict_evaluate_model = incre_xgb_model(dict_data_set=dict_data_set, info_model=info_model)
    elif brand_model == 'lgbm':
        dict_evaluate_model = incre_lgbm_model(dict_data_set=dict_data_set, info_model=info_model)
    else:
        print(f'>>>>> This {brand_model} model cannot incremental learning')
        dict_evaluate_model = {'type': 'Incremental', 'target': 'PATIENT', 'brand_quanti_model': brand_model}
    
    # Push result evaluate model
    ti.xcom_push(key='evaluate_model', value = dict_evaluate_model)
