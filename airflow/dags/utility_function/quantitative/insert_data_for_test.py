from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import psycopg2
import os
import random



def execute_query_sql(sql_stmt, conn_path):
    """ 
    This function is used to query data from a database.
    Input: SQL statement (str), connection URL of the database
    Output: Dataframe
    """
    try: 
        engine = create_engine(conn_path)
        with engine.connect() as conn:
            df = pd.read_sql(sql_stmt, conn)
    except:
        raise Exception("Cannot execute data form DB")

    return df

def execute_insert_data(conn_path, df, table_name):
    """
    This function is used to insert data into a database table.
    Input: Connection URL of the database, Dataframe, Table name
    """
    try:
        engine = create_engine(conn_path)
        with engine.begin() as conn:
            df.to_sql(table_name, conn, if_exists="append", index=False)
    except Exception as e:
        raise Exception(f"Cannot insert data to Staging DB: {e}") from e

def main():
    def re_name_table_stress(n):
        if 'S_MaxPerfusion' in n:
            return n.replace("S_MaxPerfusion","max_perfusion").lower()
        elif 'S_Intervals' in n:
            return n.replace("S_Intervals","interval").lower()
        elif 'S_' in n:
            return n.replace("S_","").lower()
        else:
            if 'LAD' in n:
                n = 'lad'+ (n.replace("LAD",""))
            elif 'LCX' in n:
                n = 'lcx'+ (n.replace("LCX",""))
            elif 'RCA' in n:
                n = 'rca'+ (n.replace("RCA",""))
            elif 'TOT' in n:
                n = 'tot'+ (n.replace("TOT",""))
            if 'Perfusion' in n:
                n = n.replace("Perfusion","") + '_perf_'
            elif 'WallThickening' in n:
                n = n.replace("WallThickening","") + '_wt_'
            elif 'WallMotion' in n:
                n = n.replace("WallMotion","") + '_wm_'
            if 'SM_' in n:
                n = n.replace("SM_","") +'mean'
            elif 'SSD_' in n:
                n = n.replace("SSD_","") +'sd'
            elif 'SE_' in n:
                n = n.replace("SE_","") +'ext'
            elif 'SSEV_' in n:
                n = n.replace("SSEV_","") +'sev'
            return n
    def re_name_table_rest(n):
        if 'R_MaxPerfusion' in n:
            return n.replace("R_MaxPerfusion","max_perfusion").lower()
        elif 'R_Intervals' in n:
            return n.replace("R_Intervals","interval").lower()
        elif 'R_' in n:
            return n.replace("R_","").lower()
        else:
            if 'LAD' in n:
                n = 'lad'+ (n.replace("LAD",""))
            elif 'LCX' in n:
                n = 'lcx'+ (n.replace("LCX",""))
            elif 'RCA' in n:
                n = 'rca'+ (n.replace("RCA",""))
            elif 'TOT' in n:
                n = 'tot'+ (n.replace("TOT",""))
            if 'Perfusion' in n:
                n = n.replace("Perfusion","") + '_perf_'
            elif 'WallThickening' in n:
                n = n.replace("WallThickening","") + '_wt_'
            elif 'WallMotion' in n:
                n = n.replace("WallMotion","") + '_wm_'
            if 'RM_' in n:
                n = n.replace("RM_","") +'mean'
            elif 'RSD_' in n:
                n = n.replace("RSD_","") +'sd'
            elif 'RE_' in n:
                n = n.replace("RE_","") +'ext'
            elif 'RSEV_' in n:
                n = n.replace("RSEV_","") +'sev'
            return n
    # load test data:
    name_file = 'data_merged.csv'
    df = pd.read_csv(f'/opt/airflow/dags/utility_function/quantitative/data_temp/{name_file}')
    date_now = datetime.now() + timedelta(hours=7)
    print('>>>>> current_time: ', date_now)
    conn_staging_db = os.environ['DEMO_STAGING_DB']
    df = df.copy()
    # add mpi_test
    df.loc[:, 'mpi_test_id'] = [n + 500 for n in list(range(0,df.shape[0]))]
    df.loc[:, 'id'] = [n + 500 for n in list(range(0,df.shape[0]))]

    #rename col other
    df.rename(columns={'CAG':'patient_predict',
           'LADCAG':'lad_predict',
           'LCXCAG':'lcx_predict',
           'RCACAG':'rca_predict',
           'BMI': 'bmi',
           'DM': 'dm',
           'HT': 'ht',
           'DLP': 'dlp',
           'CKD': 'ckd',
           'Age': 'age',
           'Gender': 'gender',
           'SSS': 'stress_sss',
           'S_STS':'stress_sts',
           'S_SMS': 'stress_sms',
           'SRS': 'rest_srs',
           'R_STS': 'rest_sts',
           'R_SMS': 'rest_sms'}, inplace=True)
  
    # dm ht dlp ckd change {"negative","positive"}
    df.replace({'dm': {0: 'negative', 1: 'positive'},
            'ht': {0: 'negative', 1: 'positive'},
            'dlp': {0: 'negative', 1: 'positive'},
            'ckd': {0: 'negative', 1: 'positive'},
            'gender': {'M': 'male', 'F': 'female'}}, inplace=True)

    # mock up hn_number
    df.loc[:, 'hn_number'] = ["000000-00" for n in list(range(0,df.shape[0]))]

    # mock up weight
    df.loc[:, 'weight'] = [str(random.randint(30,100)) for n in list(range(0,df.shape[0]))]

    # mock up height
    df.loc[:, 'height'] = [str(random.randint(70,200)) for n in list(range(0,df.shape[0]))]

    # mock up created_at
    date_now = datetime.now() + timedelta(hours=7)
    df.loc[:, 'created_at'] = [date_now for n in list(range(0,df.shape[0]))]

    # mock up mpi_exam_date
    df.loc[:, 'mpi_exam_date'] = [date_now for n in list(range(0,df.shape[0]))]

    # Insert staging data in used_by_incremental
    df.loc[:, ['patient_quanti', 'patient_quali', 'lad_quanti', 'lad_quali',
                                       'lcx_quanti', 'lcx_quali', 'rca_quanti', 'rca_quali']] = False

    # Insert staging data in mpi_crop_img 
    df.loc[:, ['stress_perfusion_dpath', 'rest_perfusion_dpath', 'stress_severity_dpath', 'rest_severity_dpath',
                                       'stress_blackout_dpath', 'rest_blackout_dpath', 'stress_def_sev_dpath', 'rest_def_sev_dpath']] = '-'

    # Insert data
    # Insert staging data in doctor_diag, mpi_crop_img, rest_quanti, stress_quanti, tpd_17_seg 
    related_table = ['mpi_test', 'doctor_diag', 'mpi_crop_img', 'tpd_17_seg', 'used_by_incremental', 'stress_quanti', 'rest_quanti']

    # Query related table where mpi_test_id in new_data.id 
    for table in related_table:
        use_cols = execute_query_sql(f"SELECT * FROM {table} LIMIT 0;", conn_staging_db).columns.tolist()
        df_staging = df.copy()
        if table == 'stress_quanti':
            df_staging = df_staging.filter(regex=("S_|SM_|SSD_|SE_|SSEV_|mpi_test_id"),axis=1)
            df_staging.columns = [re_name_table_stress(n) for n in df_staging.columns.tolist()]
            df_staging.rename(columns={'ef':'lvef'}, inplace=True)
            df_staging = df_staging.loc[:, use_cols]
        elif table == 'rest_quanti':
            df_staging =df_staging.filter(regex=("R_|RM_|RSD_|RE_|RSEV_|mpi_test_id"),axis=1)
            df_staging.columns = [re_name_table_rest(n) for n in df_staging.columns.tolist()]
            df_staging.rename(columns={'ef':'lvef'}, inplace=True)
            df_staging = df_staging.loc[:, use_cols]
        else:
            df_staging = df_staging.loc[:, use_cols]

        execute_insert_data(conn_staging_db, df_staging.loc[151:,], table)
        
    print("insert")



    
