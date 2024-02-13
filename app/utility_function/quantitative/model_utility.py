import pandas as pdcag
import numpy as np
import shutil, pickle
import pickle, os
import lightgbm as lgb
from glob import glob
import json
import ast
import xgboost as xgb
import os
# import ml_model from query
from app.utility_function.query_ml_model import ml_model

from datetime import datetime

# *******************base model function************************
def load_base_quantitative_patient_model():
    # query model (in mock-up) glob('/content/01.01.2077'+'/*model*')
    df_info_model = ml_model.query("indicator=='Quantitative' & name=='Base' & target=='PATIENT'")
    log_model_folder = glob(os.path.join(df_info_model.model_dpath.values[0],'*model*'))[0]
    with open(log_model_folder, "rb") as file_d:
        current_model = pickle.load(file_d)
    return current_model, df_info_model.brand_quanti_model.values[0]
def load_base_quantitative_rca_model():
    # query model (in mock-up)
    df_info_model = ml_model.query("indicator=='Quantitative' & name=='Base' & target=='RCA'")
    log_model_folder = glob(os.path.join(df_info_model.model_dpath.values[0],'*model*'))[0]
    with open(log_model_folder, "rb") as file_d:
        current_model = pickle.load(file_d)
    return current_model, df_info_model.brand_quanti_model.values[0]
def load_base_quantitative_lad_model():
    # query model (in mock-up)
    df_info_model = ml_model.query("indicator=='Quantitative' & name=='Base' & target=='LAD'")
    log_model_folder = glob(os.path.join(df_info_model.model_dpath.values[0],'*model*'))[0]
    with open(log_model_folder, "rb") as file_d:
        current_model = pickle.load(file_d)
    return current_model, df_info_model.brand_quanti_model.values[0]
def load_base_quantitative_lcx_model():
    # query model (in mock-up)
    df_info_model = ml_model.query("indicator=='Quantitative' & name=='Base' & target=='LCX'")
    log_model_folder = glob(os.path.join(df_info_model.model_dpath.values[0],'*model*'))[0]
    with open(log_model_folder, "rb") as file_d:
        current_model = pickle.load(file_d)
    return current_model, df_info_model.brand_quanti_model.values[0]

def load_base_quantitative_model():
    # load quantitative model (demo)
    patient_model, patient_info = load_base_quantitative_patient_model()
    rca_model, rca_info = load_base_quantitative_rca_model()
    lad_model, lad_info = load_base_quantitative_lad_model()
    lcx_model, lcx_info = load_base_quantitative_lcx_model()
    model_quantitative = {
        'patient': patient_model,
        'rca': rca_model,
        'lad': lad_model,
        "lcx": lcx_model
    }
    brand_quantitative = {
        'patient': patient_info,
        'rca': rca_info,
        'lad': lad_info,
        "lcx": lcx_info
    }
    return model_quantitative, brand_quantitative

# loading base model 
base_model_quantitative, base_brand_quantitative = load_base_quantitative_model()


# *******************airflow model function************************

def load_airflow_quantitative_patient_model():
    # query model
    df_info_model = ml_model.query("indicator=='Quantitative' & name=='Adaptive' & target=='PATIENT' & is_best == True")
    log_model_folder = glob(os.path.join(df_info_model.model_dpath.values[0], '*model*'))[0]
    
    # load info objective
    brand_model = df_info_model.brand_quanti_model.values[0]
    print(f'>>>>> patient_model: {log_model_folder}, brand model: {brand_model}')
    
    # load model
    with open(log_model_folder, "rb") as file_d:
        current_model = pickle.load(file_d)
        
    return current_model, brand_model
def load_airflow_quantitative_rca_model():
    # query model 
    df_info_model = ml_model.query("indicator=='Quantitative' & name=='Adaptive' & target=='RCA' & is_best == True")
    log_model_folder = glob(os.path.join(df_info_model.model_dpath.values[0], '*model*'))[0]
    
    # load info objective
    brand_model = df_info_model.brand_quanti_model.values[0]
    print(f'>>>>> patient_model: {log_model_folder}, brand model: {brand_model}')
    
    # load model
    with open(log_model_folder, "rb") as file_d:
        current_model = pickle.load(file_d)
        
    return current_model, brand_model
def load_airflow_quantitative_lad_model():
    # query model
    df_info_model = ml_model.query("indicator=='Quantitative' & name=='Adaptive' & target=='LAD' & is_best == True")
    log_model_folder = glob(os.path.join(df_info_model.model_dpath.values[0], '*model*'))[0]
    
    # load info objective
    brand_model = df_info_model.brand_quanti_model.values[0]
    print(f'>>>>> patient_model: {log_model_folder}, brand model: {brand_model}')
    
    # load model
    with open(log_model_folder, "rb") as file_d:
        current_model = pickle.load(file_d)
        
    return current_model, brand_model
def load_airflow_quantitative_lcx_model():
    # query model
    df_info_model = ml_model.query("indicator=='Quantitative' & name=='Adaptive' & target=='LCX' & is_best == True")
    log_model_folder = glob(os.path.join(df_info_model.model_dpath.values[0], '*model*'))[0]
    
    # load info objective
    brand_model = df_info_model.brand_quanti_model.values[0]
    print(f'>>>>> patient_model: {log_model_folder}, brand model: {brand_model}')
    
    # load model
    with open(log_model_folder, "rb") as file_d:
        current_model = pickle.load(file_d)
        
    return current_model, brand_model

def load_airflow_quantitative_model():
    # load quantitative model (demo)
    patient_model,  patient_brand = load_airflow_quantitative_patient_model()
    rca_model, rca_brand = load_airflow_quantitative_rca_model()
    lad_model, lad_brand = load_airflow_quantitative_lad_model()
    lcx_model, lcx_brand = load_airflow_quantitative_lcx_model()

    model_quantitative = {
        'patient': patient_model,
        'rca': rca_model,
        'lad': lad_model,
        "lcx": lcx_model
    }
    brand_quantitative = {
        'patient': patient_brand,
        'rca': rca_brand,
        'lad': lad_brand,
        "lcx": lcx_brand
    }
    return model_quantitative, brand_quantitative

def read_jsonfile_to_dict(file_name):
    print('>>>>> encode: ', file_name)
    with open(file_name, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)
    return data

# loading airflow model 
airflow_model_quantitative, airflow_brand_quantitative = load_airflow_quantitative_model() 

# *********************************************************************************************************************************************
def predict_quantitative_label(model, x, indicator_model):
    threshold = 0.5
    print('>>>>> indicator model:', indicator_model)
    if indicator_model == 'xgb':
        if isinstance(model, xgb.core.Booster):
            pred_prob = model.predict(xgb.DMatrix(x))
            print('>>>>> Raw predict_proba (logistic): ',pred_prob)
            pred = pred_prob.copy()
            pred[pred >= threshold] = 1
            pred[pred < threshold] = 0
            pred_prob = round(float(pred_prob), 2)
            print('>>>>> Result: ',pred_prob, 'proba: ', pred)
        elif isinstance(model, xgb.XGBClassifier):
            pred = model.predict(x)
            pred_prob = model.predict_proba(x)
            print('>>>>> Raw predict_proba (logistic): ',pred_prob)
            pred_prob = round(float(np.max(pred_prob)), 2)
            print('>>>>> Result: ',pred_prob, 'proba: ', pred)
        else:
            raise ValueError(f"Unknown objective model")
        
    elif indicator_model == 'lgbm':
        pred_prob = model.predict(x)
        print('>>>>> Raw predict_proba (logistic): ',pred_prob)
        if isinstance(model, lgb.basic.Booster):
            pred = pred_prob.copy()
            pred[pred >= threshold] = 1
            pred[pred < threshold] = 0
            pred_prob = round(float(pred_prob), 2)
            print('>>>>> Result: ',pred_prob, 'proba: ', pred)
        elif isinstance(model, lgb.LGBMClassifier):
            pred = model.predict(x)
            pred_prob = model.predict_proba(x)
            pred_prob = round(float(np.max(pred_prob)), 2 )
            print('>>>>> Result',pred_prob)
        else:
            raise ValueError(f"Unknown model type")
    elif indicator_model == 'superlearner':
            pred = model.predict(x)
            pred_prob = model.predict_proba(x)
            print('>>>>> Raw predict_proba (logistic): ',pred_prob)
            pred_prob = round(float(np.max(pred_prob)), 2 )
            print('>>>>> Result',pred_prob)
    else:
        raise ValueError(f"Unknown model type")
    return int(pred[0]), pred_prob

def predict_quantitative_model(quanti_features, name_indicator):
    
    if 'Base_Quantitative' == name_indicator:
        quanti_model = base_model_quantitative
        quanti_info = base_brand_quantitative
    elif 'Adaptive_Quantitative' == name_indicator:
        quanti_model = airflow_model_quantitative
        quanti_info = airflow_brand_quantitative
        
    result_predict = dict()
    for taget in ['lad', 'lcx', 'rca', 'patient']:
        # check name model 
        if 'Base_Quantitative' == name_indicator:
            print(f'>>>>> Start predict taget: {taget}')
            predict, predict_prob = predict_quantitative_label(quanti_model[taget], quanti_features, quanti_info[taget])
            result_predict[f'predict_prob_{taget}'] = predict_prob
            result_predict[f'predict_{taget}'] = predict
        elif 'Adaptive_Quantitative' == name_indicator:
            print(f'>>>>> Start predict taget: {taget}')
            predict, predict_prob = predict_quantitative_label(quanti_model[taget], quanti_features, quanti_info[taget])
            result_predict[f'predict_prob_{taget}'] = predict_prob
            result_predict[f'predict_{taget}'] = predict

    print("*"*10, "predict_quantitative", "*"*10,"\n",
          result_predict,"\n",
          "*"*40)

    return result_predict