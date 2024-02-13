import pandas as pd
import pickle
import numpy as np
import psycopg2
import os, glob
from airflow.models.xcom import XCom
from collections import Counter

from sklearn import preprocessing
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import train_test_split


def save_file_pickle(dict_file, name_file):
    # Get variable environment
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')

    with open(os.path.join(path_data_temp, f'{name_file}.pickle'), 'wb') as handle:
        pickle.dump(dict_file, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_prepare_data(target):
    """ This function is used to load preparation data. There are 4 files.
     lad_train_model.pickle, lcx_train_model.pickle,  rca_train_model.pickle, patient_train_model.pickle
     input: target data set (lad, lcx, rca, patient)
     output: dict data set
    In data set:
        {'X_untrain': X_untrain,
         'y_untrain': y_untrain,
        'X_train': X_train,
        'y_train': y_train,
        'X_test': X_test,
        'y_test': y_test,}
    """
    # Get variable environment
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    data_set = pickle.load(open(os.path.join(path_data_temp,f'{target}_train_model.pickle'), 'rb'))
    print('>>>>> data_set', open(os.path.join(path_data_temp,f'{target}_train_model.pickle')))
    return data_set


def pre_processing_quantitative(target):
    # Get variable environment
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')

    def load_data(target):
        if target == 'patient_predict':
            name = 'patient'
        elif target == 'lad_predict':
            name = 'lad'
        elif target == 'lcx_predict':
            name = 'lcx'
        elif target == 'rca_predict':
            name = 'rca'

        df_untrain = pd.read_csv(os.path.join(path_data_temp, f"train_incre_{name}.csv"))
        df_train = pd.read_csv(os.path.join(path_data_temp, f"train_set_{name}.csv"))
        df_test = pd.read_csv(os.path.join(path_data_temp, f"test_set_{name}.csv"))
        df_all_data = pd.read_csv(os.path.join(path_data_temp, f"all_train_set.csv"))
        df_all_untrain = pd.read_csv(os.path.join(path_data_temp, f"all_untrain_set_{name}.csv"))

        return df_train, df_untrain, df_test, df_all_data, df_all_untrain

    def partition_data(df_train, df_untrain, df_test, df_all_data, df_all_untrain, target):
        # if target == 'patient_predict':
        #     not_use_columns = ['mpi_test_id','hn_number','mpi_exam_date','created_at','lad_predict','lcx_predict','rca_predict','patient_predict']
        # elif target == 'lad_predict':
        #     not_use_columns = ['mpi_test_id','hn_number','mpi_exam_date','created_at','lad_predict','lcx_predict','rca_predict','patient_predict']
        # elif target == 'lcx_predict':
        #     not_use_columns = ['mpi_test_id','hn_number','mpi_exam_date','created_at','lad_predict','lcx_predict','rca_predict','patient_predict']
        # elif target == 'rca_predict':
        #     not_use_columns = ['mpi_test_id','hn_number','mpi_exam_date','created_at','lad_predict','lcx_predict','rca_predict','patient_predict']
        # Define column names
        # not_use_columns = ['mpi_test_id', 'hn_number', 'mpi_exam_date', 'weight', 'height', 'created_at', 'lad_predict', 'lcx_predict', 'rca_predict', 'patient_predict', 'patient_quanti', 'patient_quali', 'lad_quanti', 'lad_quali', 'lcx_quanti', 'lcx_quali', 'rca_quanti', 'rca_quali']
        # X = df_train[[c for c in df_train if c not in not_use_columns]]
        # X2 = df_untrain[[c for c in df_untrain if c not in not_use_columns]]
        # X3 = df_test[[c for c in df_test if c not in not_use_columns]]

        # Define column names
        column_names = [
            "s_max_perfusion", "s_interval", "s_ed", "s_es", "s_lvef", "s_lad_perf_mean", "s_lad_perf_sd",
            "s_lcx_perf_mean", "s_lcx_perf_sd", "s_rca_perf_mean", "s_rca_perf_sd", "s_tot_perf_mean",
            "s_tot_perf_sd", "s_lad_wt_mean", "s_lad_wt_sd", "s_lcx_wt_mean", "s_lcx_wt_sd", "s_rca_wt_mean",
            "s_rca_wt_sd", "s_tot_wt_mean", "s_tot_wt_sd", "s_lad_wm_mean", "s_lad_wm_sd", "s_lcx_wm_mean",
            "s_lcx_wm_sd", "s_rca_wm_mean", "s_rca_wm_sd", "s_tot_wm_mean", "s_tot_wm_sd", "s_lad_perf_ext",
            "s_lcx_perf_ext", "s_rca_perf_ext", "s_tot_perf_ext", "s_lad_wt_ext", "s_lcx_wt_ext", "s_rca_wt_ext",
            "s_tot_wt_ext", "s_lad_wm_ext", "s_lcx_wm_ext", "s_rca_wm_ext", "s_tot_wm_ext", "s_lad_perf_sev",
            "s_lcx_perf_sev", "s_rca_perf_sev", "s_tot_perf_sev", "s_lad_wt_sev", "s_lcx_wt_sev", "s_rca_wt_sev",
            "s_tot_wt_sev", "s_lad_wm_sev", "s_lcx_wm_sev", "s_rca_wm_sev", "s_tot_wm_sev", "r_max_perfusion",
            "r_interval", "r_ed", "r_es", "r_lvef", "r_lad_perf_mean", "r_lad_perf_sd", "r_lcx_perf_mean",
            "r_lcx_perf_sd", "r_rca_perf_mean", "r_rca_perf_sd", "r_tot_perf_mean", "r_tot_perf_sd", "r_lad_wt_mean",
            "r_lad_wt_sd", "r_lcx_wt_mean", "r_lcx_wt_sd", "r_rca_wt_mean", "r_rca_wt_sd", "r_tot_wt_mean",
            "r_tot_wt_sd", "r_lad_wm_mean", "r_lad_wm_sd", "r_lcx_wm_mean", "r_lcx_wm_sd", "r_rca_wm_mean",
            "r_rca_wm_sd", "r_tot_wm_mean", "r_tot_wm_sd", "r_lad_perf_ext", "r_lcx_perf_ext", "r_rca_perf_ext",
            "r_tot_perf_ext", "r_lad_wt_ext", "r_lcx_wt_ext", "r_rca_wt_ext", "r_tot_wt_ext", "r_lad_wm_ext",
            "r_lcx_wm_ext", "r_rca_wm_ext", "r_tot_wm_ext", "r_lad_perf_sev", "r_lcx_perf_sev", "r_rca_perf_sev",
            "r_tot_perf_sev", "r_lad_wt_sev", "r_lcx_wt_sev", "r_rca_wt_sev", "r_tot_wt_sev", "r_lad_wm_sev",
            "r_lcx_wm_sev", "r_rca_wm_sev", "r_tot_wm_sev", "stress_sss", "stress_sts", 'stress_sms', 'rest_srs',
            'rest_sts', 'rest_sms', "age", "gender", "bmi", "dm", "ht", "dlp", "ckd"
        ]

        # Filter columns
        X = df_train[column_names]
        X2 = df_untrain[column_names]
        X3 = df_test[column_names]
        X4 = df_all_data[column_names]
        X5 = df_all_untrain[column_names]

        X = X.replace({'dm': {'negative': 0, 'positive': 1}, 'ht': {'negative': 0, 'positive': 1},'dlp': {'negative': 0, 'positive': 1}, 'ckd': {'negative': 0, 'positive': 1}})
        X2 = X2.replace({'dm': {'negative': 0, 'positive': 1}, 'ht': {'negative': 0, 'positive': 1},'dlp': {'negative': 0, 'positive': 1}, 'ckd': {'negative': 0, 'positive': 1}})
        X3 = X3.replace({'dm': {'negative': 0, 'positive': 1}, 'ht': {'negative': 0, 'positive': 1},'dlp': {'negative': 0, 'positive': 1}, 'ckd': {'negative': 0, 'positive': 1}})
        X4 = X4.replace({'dm': {'negative': 0, 'positive': 1}, 'ht': {'negative': 0, 'positive': 1},'dlp': {'negative': 0, 'positive': 1}, 'ckd': {'negative': 0, 'positive': 1}})
        X5 = X5.replace({'dm': {'negative': 0, 'positive': 1}, 'ht': {'negative': 0, 'positive': 1},'dlp': {'negative': 0, 'positive': 1}, 'ckd': {'negative': 0, 'positive': 1}})

        Y = np.array(df_train.replace({target: {'negative': 0, 'positive': 1}})[target])
        Y2 = np.array(df_untrain.replace({target: {'negative': 0, 'positive': 1}})[target])
        Y3 = np.array(df_test.replace({target: {'negative': 0, 'positive': 1}})[target])
        Y4 = np.array(df_all_data.replace({target: {'negative': 0, 'positive': 1}})[target])
        Y5 = np.array(df_all_untrain.replace({target: {'negative': 0, 'positive': 1}})[target])
        return X, X2, X3, X4, X5, Y, Y2, Y3, Y4, Y5

    def extractFeat(df_X):
        featX = df_X.copy()
        init_feat = init_feature(featX)
        sex_feat = getOnehotencoderSex(featX['gender'])
        print(sex_feat)

        #concat features
        featX.reset_index(drop=True, inplace=True)
        featX = pd.concat([init_feat, sex_feat], axis=1)
        if "female" not in list(featX.columns):
            featX['male'] = featX['male'].astype(int)
            featX['female'] = 0
        elif "male" not in list(featX.columns):
            featX['female'] = featX['female'].astype(int)
            featX['male'] = 0
        else:
            featX['female'] = featX['female'].astype(int)
            featX['male'] = featX['male'].astype(int)

        return featX

    def init_feature(df_X): 
        #mpi feature
        initFeature = df_X[[c for c in df_X if c not in ['gender']]]
        return initFeature

    def getOnehotencoderSex(df_X):
        sexDummy = pd.get_dummies(df_X)
        return sexDummy 
    def standard_scale(df, column):
        if(type(column) != str):
            X = df.values
            scaler = preprocessing.Normalizer()
            scaler.fit(X)
            X_scaled = scaler.transform(X)
            df = pd.DataFrame(data = X_scaled, columns=column)
        return df

    def min_max_scale(df, column):
        if(type(column) != str):
            X = df.values
            scaler = preprocessing.Normalizer()
            scaler.fit(X)
            X_scaled = scaler.transform(X)
            df = pd.DataFrame(data = X_scaled, columns=column)
        return df

    def normalize(df, column):
        if(type(column) != str):
            X = df.values
            scaler = preprocessing.Normalizer()
            scaler.fit(X)
            X_scaled = scaler.transform(X)
            df = pd.DataFrame(data = X_scaled, columns=column)
        return df

    def normalize_data(feat):
        feat_scale = feat.copy().astype(float)
        feat_scale_normalize = normalize(feat_scale, feat_scale.columns)
        feat_scale_log = log_transform(feat_scale, feat_scale.columns)
        feat_scale_concat = pd.concat([feat_scale_normalize, feat_scale_log], axis=1)
        return feat_scale_concat


    def log_transform(df, column):
        # run["sys/tags"].add('log_transform')
        print(df)
        X = abs(df.values)
        scaler = FunctionTransformer(np.log)
        scaler.fit(X)
        X_scaled = scaler.transform(X +1)
        column = [str(col) + '_log' for col in column]
        df = pd.DataFrame(data = X_scaled, columns=column)
        return df
   
    # Load data
    df_train, df_untrain, df_test, df_all_data, df_all_untrain = load_data(target)

    # Arrang
    # df_train.rename(columns={"cag": "CAG", "ladcag": "LADCAG", "lcxcag": "LCXCAG", "rcacag": "RCACAG"}, errors="raise", inplace=True)
    # df_untrain.rename(columns={"cag": "CAG", "ladcag": "LADCAG", "lcxcag": "LCXCAG", "rcacag": "RCACAG"}, errors="raise", inplace=True)
    # df_test.rename(columns={"cag": "CAG", "ladcag": "LADCAG", "lcxcag": "LCXCAG", "rcacag": "RCACAG"}, errors="raise", inplace=True)
    
    print(target," All data set: ", Counter(df_all_data[target]))
    print(f'shape data: {df_all_data.shape}')
    print(target," Train set: ", Counter(df_train[target]))
    print(f'shape data: {df_train.shape}')
    print(target," All untrain set: ", Counter(df_train[target]))
    print(f'shape data: {df_all_untrain.shape}')
    print(target," Untrain set: ", Counter(df_untrain[target]))
    print(f'shape data: {df_untrain.shape}')
    print(target," Test set: ", Counter(df_test[target]))
    print(f'shape data: {df_test.shape}')

    # Partition data
    X_train, X_untrain, X_test, X_all, X_all_untrain, y_train, y_untrain, y_test, y_all, y_all_untrain = partition_data(df_train, df_untrain, df_test, df_all_data, df_all_untrain, target)

    #5. extract features
    feat_train = extractFeat(X_train)
    feat_untrain = extractFeat(X_untrain)
    feat_test = extractFeat(X_test)
    feat_all = extractFeat(X_all)
    feat_all_untrain = extractFeat(X_all_untrain)

    #6. normalize
    feat_scale_train = feat_train.copy()
    feat_scale_untrain = feat_untrain.copy()
    feat_scale_test = feat_test.copy()
    feat_scale_all = feat_all.copy()
    feat_scale_all_untrain = feat_all_untrain.copy()
    feat_normalize_train = normalize_data(feat_scale_train)
    feat_normalize_untrain = normalize_data(feat_scale_untrain)
    feat_normalize_test = normalize_data(feat_scale_test)
    feat_normalize_all = normalize_data(feat_scale_all)
    feat_normalize_all_untrain = normalize_data(feat_scale_all_untrain)

    #7. df to numpy arrays
    X_train = np.array(feat_normalize_train)
    X_untrain = np.array(feat_normalize_untrain)
    X_test = np.array(feat_normalize_test)
    X_all = np.array(feat_normalize_all)
    X_all_untrain = np.array(feat_normalize_all_untrain)

    dict_data_set = {'X_untrain': X_untrain,
                 'y_untrain': y_untrain,
                 'X_train': X_train,
                 'y_train': y_train,
                 'X_test': X_test,
                 'y_test': y_test,
                 'X_all': X_all,
                 'y_all': y_all,
                 'X_all_untrain': X_all_untrain,
                 'y_all_untrain': y_all_untrain
                }

    return dict_data_set

def main(**kwargs):
    # prepare data
    dict_lad_set = pre_processing_quantitative(target="lad_predict")
    dict_lcx_set = pre_processing_quantitative(target="lcx_predict")
    dict_rca_set = pre_processing_quantitative(target="rca_predict")
    dict_patient_set = pre_processing_quantitative(target="patient_predict")

    # save data
    save_file_pickle(dict_file = dict_lad_set, name_file = "lad_train_model")
    save_file_pickle(dict_file = dict_lcx_set, name_file = "lcx_train_model")
    save_file_pickle(dict_file = dict_rca_set, name_file = "rca_train_model")
    save_file_pickle(dict_file = dict_patient_set, name_file = "patient_train_model")

