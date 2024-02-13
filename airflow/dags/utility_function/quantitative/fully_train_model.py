import pandas as pd
import numpy as np
import pickle
import json
import os
from glob import glob
from dateutil import parser
from datetime import datetime, timedelta
import ast
import xgboost as xgb
import lightgbm as lgb

#import lib use to train model
from xgboost import XGBClassifier
import xgboost as xgb
import lightgbm as lgb
from lightgbm import LGBMClassifier

from module_superlearner.superlearner_model import SuperLearnerClassifier
from sklearn import linear_model
from utility_function.quantitative.prepare_quanti_data_processing import load_prepare_data

def write_param_to_jsonfile(dict_param, file_name):
    with open(file_name, "w") as file:
        json.dump(dict_param, file)

def read_jsonfile_to_dict(file_name):
    with open(file_name, "r") as file:
        data = json.load(file)
    return data

def fully_incre_xgb_model(dict_data_set, info_model):
    # Get variable environment
    path_model_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'model_temp')
    target = info_model.target.values[0]
    dpath_temp_model = os.path.join(path_model_temp, f"incremental/{target.upper()}")


    # Load model and paremeter (mockup) 
    dpath_model = info_model.model_dpath.values[0] # Example: "/opt/app/model/archived_model/pateint/xgb/n.n.n (version)
    p_file_model = glob(f"{dpath_model}/*model*")[0] 
    p_file_param = glob(f"{dpath_temp_model}/*parameter*")[0]
    param = read_jsonfile_to_dict(p_file_param)
    target = info_model.target.values[0]
    print(f'>>>>> {target}: model_dpath ', dpath_model)

    # Load the old model
    with open(p_file_model, 'rb') as model_file:
        booster_model = pickle.load(model_file)

    # Prepare DMatrix for training data
    untrain_data = xgb.DMatrix(dict_data_set['X_all_untrain'], label=dict_data_set['y_all_untrain'])

    # Train the model
    path_text_model = os.path.join(dpath_temp_model, 'xgb_structure.txt')
    booster_model.save_model(path_text_model)
    tranfer_model = xgb.train(param, untrain_data, 60, xgb_model=path_text_model)

    # Save fully train model
    version = (datetime.now() + timedelta(hours=7)).strftime('%d-%m-%Y')
    brand_model = 'xgb'
    filename_model = f"{version}_{target.lower()}_{brand_model}_quantitative_incremental_model.pickle"
    with open(os.path.join(dpath_temp_model, filename_model), 'wb') as filename:
        pickle.dump(tranfer_model, filename)


def fully_incre_lgbm_model(dict_data_set, info_model):
    # Get variable environment
    path_model_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'model_temp')
    target = info_model.target.values[0]
    dpath_temp_model = os.path.join(path_model_temp, f"incremental/{target.upper()}")

    # Load model and paremeter (mockup) 
    dpath_model = info_model.model_dpath.values[0] # Example: "/opt/app/model/archived_model/pateint/lgbm/n.n.n (version)
    print('dpathmodel', dpath_model)
    p_file_model = glob(f"{dpath_model}/*model*")[0]
    p_file_param = glob(f"{dpath_temp_model}/*parameter*")[0]
    old_model = pickle.load(open(p_file_model, 'rb'))
    param = read_jsonfile_to_dict(p_file_param)
    print(f'>>>>> {target}: model_dpath ', dpath_model)

    # Check the type of the model
    if isinstance(old_model, lgb.basic.Booster):
        booster_model = old_model
    elif isinstance(old_model, lgb.LGBMClassifier):
        booster_model = old_model.booster_
    else:
        raise ValueError("Unknown model type")

    # Prepare dataset for train data
    untrain_data = lgb.Dataset(dict_data_set['X_all_untrain'], label=dict_data_set['y_all_untrain'], free_raw_data=False)

    # Train model
    tranfer_model = lgb.train(param, train_set=untrain_data, init_model=booster_model, num_boost_round=60, keep_training_booster=True)
    print(type(tranfer_model))


    # Save fully train model in temporary folder
    version = (datetime.now() + timedelta(hours=7)).strftime('%d-%m-%Y')
    brand_model = 'lgbm'
    filename_model = f"{version}_{target.lower()}_{brand_model}_quantitative_incremental_model.pickle"
    with open(os.path.join(dpath_temp_model, filename_model), 'wb') as filename:
        pickle.dump(tranfer_model, filename)

def fully_retrain_xgb_model(dict_data_set, target):
    # Get variable environment
    algorithm = "xgb"
    path_model_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'model_temp')
    dpath_model = os.path.join(path_model_temp, f"re-train/{target.upper()}/{algorithm}")
    
    # Get parameter
    p_file_param = glob(f"{dpath_model}/*parameter*")[0]
    param = read_jsonfile_to_dict(p_file_param)
    
    # Load model and assign parameter
    re_train_model = XGBClassifier(**param)
    print(re_train_model)
    
    # Train model
    model_fit = re_train_model.fit(dict_data_set['X_all'], dict_data_set['y_all'])

    # Save model and parameter in temporary folder
    version = (datetime.now() + timedelta(hours=7)).strftime('%d-%m-%Y')
    filename_model = f"{version}_{target.lower()}_{algorithm}_quantitative_re-train_model.pickle"
    with open(os.path.join(dpath_model, filename_model), 'wb') as filename:
        pickle.dump(model_fit, filename)

def fully_retrain_lgbm_model(dict_data_set, target):
    # Get variable environment
    algorithm = 'lgbm'
    path_model_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'model_temp')
    
    # Get parameter
    dpath_model = os.path.join(path_model_temp, f"re-train/{target.upper()}/{algorithm}")
    p_file_param = glob(f"{dpath_model}/*parameter*")[0]
    param = read_jsonfile_to_dict(p_file_param)

    # Load model and assign parameter
    re_train_model = LGBMClassifier(**param)
    print(re_train_model)
    
    # Train model    
    model_fit = re_train_model.fit(dict_data_set['X_all'], dict_data_set['y_all'])

    # Save model and parameter in temporary folder
    version = (datetime.now() + timedelta(hours=7)).strftime('%d-%m-%Y')
    filename_model = f"{version}_{target.lower()}_{algorithm}_quantitative_re-train_model.pickle"
    with open(os.path.join(dpath_model, filename_model), 'wb') as filename:
        pickle.dump(model_fit, filename)


def fully_retrain_super_model(dict_data_set, target):
    # Get variable environment
    algorithm = 'superlearner'
    path_model_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'model_temp')
    
    # Get parameter
    dpath_model = os.path.join(path_model_temp, f"re-train/{target.upper()}/{algorithm}")
    p_file_param = glob(f"{dpath_model}/*parameter*")[0]
    param = pickle.load(open(p_file_param, 'rb'))
    
    # Load model and assign parameter
    re_train_model = SuperLearnerClassifier(**param)
    
    # Train model    
    model_fit = re_train_model.fit(dict_data_set['X_all'], dict_data_set['y_all'])

    # Save model and parameter in temporary folder
    version = (datetime.now() + timedelta(hours=7)).strftime('%d-%m-%Y')
    filename_model = f"{version}_{target.lower()}_{algorithm}_quantitative_re-train_model.pickle"
    with open(os.path.join(dpath_model, filename_model), 'wb') as filename:
        pickle.dump(model_fit, filename)
    
def target_fully_train_model(target):
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    df_info_all_model = pd.read_csv(os.path.join(path_data_temp, f"info_current_model.csv"))
    df_best_model = pd.read_csv(os.path.join(path_data_temp, f"result_best_model.csv"))
    best_model_lad = df_best_model.loc[df_best_model.target == target.upper()]

    # Load data
    dict_data_set = load_prepare_data(target= target.lower())
    brand = best_model_lad.loc[:, 'brand_quanti_model'].values[0]  
    type_train = best_model_lad.loc[:, 'type'].values[0]
    print(f'>>>>> brand: {brand}, type train: {type_train}')
    
    if type_train == 'Fully Re-train':
        # Load infomation current model
        if brand == 'xgb':
            fully_retrain_xgb_model(dict_data_set, target= target.upper())
        elif brand == 'lgbm':
            fully_retrain_lgbm_model(dict_data_set, target= target.upper())
        elif brand == 'superlearner':
            fully_retrain_super_model(dict_data_set, target= target.upper())
    elif type_train == 'Incremental':
        condition_qurey_model = f"target == '{target.upper()}' & is_best == True"
        info_model = df_info_all_model.query(condition_qurey_model)
        print('ok')
        if brand == 'xgb':
            fully_incre_xgb_model(dict_data_set, info_model)
        elif brand == 'lgbm':
            fully_incre_lgbm_model(dict_data_set, info_model)
    else:
        raise('Error not found')

def patient_fully_train_model(**kwargs):
    ti = kwargs['ti']
    target = 'patient'
    print(f'>>>>> train model: {target}')
    target_fully_train_model(target)

def rca_fully_train_model(**kwargs):
    ti = kwargs['ti']
    target = 'rca'
    print(f'>>>>> train model: {target}')
    target_fully_train_model(target)
    
def lcx_fully_train_model(**kwargs):
    ti = kwargs['ti']
    target = 'lcx'
    print(f'>>>>> train model: {target}')
    target_fully_train_model(target)
    
def lad_fully_train_model(**kwargs):
    ti = kwargs['ti']
    target = 'lad'
    print(f'>>>>> train model: {target}')
    target_fully_train_model(target)
    
