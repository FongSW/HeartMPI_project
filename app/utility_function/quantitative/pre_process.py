#other utility packages
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

from sklearn import preprocessing
from sklearn.preprocessing import FunctionTransformer
from sklearn.decomposition import PCA

def init_feature(df_X):
    #mpi feature
    initFeature = df_X[[c for c in df_X if c not in ['gender']]]
    return initFeature

from sklearn.preprocessing import OneHotEncoder

def getOnehotencoderSex(df_X):
  if(df_X.values == "male"):
    sex_list = ["1", "0"]
  else:
    sex_list = ["0", "1"]
  sexDummy = pd.DataFrame(data=[sex_list], columns=["female", "male"])
  return sexDummy

def extractFeat(df_X):
    
    featX = df_X.copy()
    init_feat = init_feature(featX)
    sex_feat = getOnehotencoderSex(featX['gender'])

    #concat features
    featX.reset_index(drop=True, inplace=True)
    init_feat.reset_index(drop=True, inplace=True)
    final_featX = pd.concat([init_feat, sex_feat], axis=1).astype(float) # เพิ่ม.astype(float)
    final_featX['female'] = final_featX['female'].astype(int)
    final_featX['male'] = final_featX['male'].astype(int)
    final_featX = final_featX.loc[:, ~final_featX.columns.str.match('Unnamed')]
    # feat = feat.drop("Gender", axis=1)
    
    return final_featX

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

def log_transform(df, column):
    print(df)
    X = abs(df.values)
    scaler = FunctionTransformer(np.log)
    scaler.fit(X)
    X_scaled = scaler.transform(X +1)
    column = [str(col) + '_log' for col in column]
    df = pd.DataFrame(data = X_scaled, columns=column)
    return df

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

def log_transform(df, column):
    print(df)
    X = abs(df.values)
    scaler = FunctionTransformer(np.log)
    scaler.fit(X)
    X_scaled = scaler.transform(X +1)
    column = [str(col) + '_log' for col in column]
    df = pd.DataFrame(data = X_scaled, columns=column)
    return df

from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD

def decomposition(df, target, algorithm):
  algorithm = algorithm.upper()
  target = target.upper()
  if(algorithm == "PCA"):
    decompose_algo = PCA(n_components=1)
  elif(algorithm == "TNSE"):
    decompose_algo = TSNE(n_components=1)
  elif(algorithm == "LSA"):
    decompose_algo = TruncatedSVD(n_components=1)
  if(target == "PC"):
    split_df = df[[c for c in df if c in ['female', 'male', 'Age', 'BMI', 'DM', 'HT', 'DLP', 'CKD']]]
    components = decompose_algo.fit_transform(split_df.values)
    decompose_df = pd.DataFrame(data = components, columns = [target+'_'+algorithm+'_features'])
  elif(target == "LAD" or target == "LCX" or target == "RCA" or target == "TOT"):
    split_df = [col for col in df.columns if target in col]
    split_df_tnse_columns = df[[c for c in df.columns if c in split_df]]
    components = decompose_algo.fit_transform(split_df_tnse_columns.values)
    decompose_df = pd.DataFrame(data = components, columns = [target+'_'+algorithm+'_features'])
  return decompose_df
  
def pre_processing(df_feat_x):
    
    # 1. chane values of gender: enum("M","F"), dm: enum("negative","positive"), ht: enum("negative","positive"), dlp: enum("negative","positive"), ckd: enum("negative","positive")
    # df_feat_x = df_feat_x.replace({'gender': {'male': 0, 'female ': 1}})
    df_feat_x = df_feat_x.replace({'dm': {'negative': 0, 'positive': 1}})
    df_feat_x = df_feat_x.replace({'ht': {'negative': 0, 'positive': 1}})
    df_feat_x = df_feat_x.replace({'dlp': {'negative': 0, 'positive': 1}})
    df_feat_x = df_feat_x.replace({'ckd': {'negative': 0, 'positive': 1}})

    # 2. get data and arrang
    # columns_name = ["s_max_perfusion", "s_interval", "s_ed", "s_es", "s_lvef", "s_lad_perf_mean", "s_lad_perf_sd", "s_lcx_perf_mean", "s_lcx_perf_sd", "s_rca_perf_mean", "s_rca_perf_sd", "s_tot_perf_mean", "s_tot_perf_sd", "s_lad_wt_mean", "s_lad_wt_sd", "s_lcx_wt_mean", "s_lcx_wt_sd", "s_rca_wt_mean", "s_rca_wt_sd", "s_tot_wt_mean", "s_tot_wt_sd", "s_lad_wm_mean", "s_lad_wm_sd", "s_lcx_wm_mean", "s_lcx_wm_sd", "s_rca_wm_mean", "s_rca_wm_sd", "s_tot_wm_mean", "s_tot_wm_sd", "s_lad_perf_ext", "s_lcx_perf_ext", "s_rca_perf_ext", "s_tot_perf_ext", "s_lad_wt_ext", "s_lcx_wt_ext", "s_rca_wt_ext", "s_tot_wt_ext", "s_lad_wm_ext", "s_lcx_wm_ext", "s_rca_wm_ext", "s_tot_wm_ext", "s_lad_perf_sev", "s_lcx_perf_sev", "s_rca_perf_sev", "s_tot_perf_sev", "s_lad_wt_sev", "s_lcx_wt_sev", "s_rca_wt_sev", "s_tot_wt_sev", "s_lad_wm_sev", "s_lcx_wm_sev", "s_rca_wm_sev", "s_tot_wm_sev", "r_max_perfusion", "r_interval", "r_ed", "r_es", "r_lvef", "r_lad_perf_mean", "r_lad_perf_sd", "r_lcx_perf_mean", "r_lcx_perf_sd", "r_rca_perf_mean", "r_rca_perf_sd", "r_tot_perf_mean", "r_tot_perf_sd", "r_lad_wt_mean", "r_lad_wt_sd", "r_lcx_wt_mean", "r_lcx_wt_sd", "r_rca_wt_mean", "r_rca_wt_sd", "r_tot_wt_mean", "r_tot_wt_sd", "r_lad_wm_mean", "r_lad_wm_sd", "r_lcx_wm_mean", "r_lcx_wm_sd", "r_rca_wm_mean", "r_rca_wm_sd", "r_tot_wm_mean", "r_tot_wm_sd", "r_lad_perf_ext", "r_lcx_perf_ext", "r_rca_perf_ext", "r_tot_perf_ext", "r_lad_wt_ext", "r_lcx_wt_ext", "r_rca_wt_ext", "r_tot_wt_ext", "r_lad_wm_ext", "r_lcx_wm_ext", "r_rca_wm_ext", "r_tot_wm_ext", "r_lad_perf_sev", "r_lcx_perf_sev", "r_rca_perf_sev", "r_tot_perf_sev", "r_lad_wt_sev", "r_lcx_wt_sev", "r_rca_wt_sev", "r_tot_wt_sev", "r_lad_wm_sev", "r_lcx_wm_sev", "r_rca_wm_sev", "r_tot_wm_sev", "stress_sss", "stress_sts", 'stress_sms', 'rest_srs', 'rest_sts', 'rest_sms', "age", "gender", "bmi", "dm", "ht", "dlp", "ckd"]
    # feat_x = df_feat_x[columns_name]
    feat_x = df_feat_x.copy()
    print("********", df_feat_x.columns[df_feat_x.isna().any()].tolist())
    print("df >>>",feat_x.shape)
    # 3. extract features
    feat = extractFeat(feat_x)
    # 4. normalize
    feat_scale = feat.copy()
    print(feat_scale.values)
    feat_scale_normalize = normalize(feat_scale, feat_scale.columns)
    print('*****log_transform*******')
    feat_scale_log = log_transform(feat_scale, feat_scale.columns)
    feat_scale_concat = pd.concat([feat_scale_normalize, feat_scale_log], axis=1)
    # 5. concat feat_x
    print(feat_scale_concat.shape)
    print(feat_scale_concat)
    feat_corr = feat_scale_concat
    
    return feat_corr