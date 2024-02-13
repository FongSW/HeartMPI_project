import pandas as pd
import numpy as np
from utility_function.quantitative.staging_data import execute_query_sql
import os

def main(**kwargs):
    """
     This function is used to get staging and split data from the database and save it as CSV files.
     Output: file csv 
     train data (retrain model): test_set_{TARGET}.csv
     train data (incremental model): train_set_{TARGET}.csv
     test data: train_incre_{TARGET}.csv
    """
    try:
        ti = kwargs['ti']
        # Get variable environment
        conn_staging_db = os.environ['DEMO_STAGING_DB']
        path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
        print('>>>>> Path Data Temp:', path_data_temp)
    
        # Create query SQL
        query_mpi_test = "SELECT * FROM mpi_test as mt\
                        INNER JOIN doctor_diag as dd  ON mt.id = dd.mpi_test_id\
                        INNER JOIN tpd_17_seg as tpd  ON mt.id = tpd.mpi_test_id\
                        INNER JOIN used_by_incremental as ubi ON mt.id = ubi.mpi_test_id"
        query_stress_quanti = "SELECT * FROM stress_quanti"
        query_rest_quanti = "SELECT * FROM rest_quanti"

        # Query data from tables: stress_quanti, rest_quanti, mpi_test, tpd_17_seg {male, female}                 
        df_mpi_test = execute_query_sql(query_mpi_test, conn_staging_db).drop(columns=['mpi_test_id']).rename(columns={'id':'mpi_test_id'}).set_index(['mpi_test_id'])
        df_stress_quanti = execute_query_sql(query_stress_quanti, conn_staging_db).set_index(['mpi_test_id'])
        df_rest_quanti = execute_query_sql(query_rest_quanti, conn_staging_db).set_index(['mpi_test_id'])
        df_stress_quanti.columns = ['s_'+ str(col)for col in df_stress_quanti.columns]
        df_rest_quanti.columns = ['r_'+ str(col)for col in df_rest_quanti.columns]

        # Join data
        df_all_data = df_mpi_test.join([df_stress_quanti, df_rest_quanti])
        df_all_data.to_csv(os.path.join(path_data_temp, f"all_train_set.csv"))
        print(f'>>>>> Count all data: {df_all_data.shape[0]}')
        
        # Split data for training models
        for t in ['lad', 'lcx', 'rca', 'patient']:
            # Split untrained data
            df_untrain_target = df_all_data.loc[(df_all_data[f'{t}_quanti'] == False)]

            # Create a train set with 70% for training the incremental model
            df_train_incre_target = df_untrain_target.sample(frac = 0.7, random_state=42)
            print(f'>>>>> Count untrain_set_{t} data: {df_train_incre_target.shape[0]}')

            # Creating a test set with 30%
            df_test_set_target = df_untrain_target.drop(df_train_incre_target.index)
            print(f'>>>>> Count test_set_{t} data: {df_test_set_target.shape[0]}')

            # Creating a train set for train re-train model
            df_train_set_target = df_all_data.drop(df_test_set_target.index)
            print(f'>>>>> Count re_train_set_{t} data: {df_train_set_target.shape[0]}')

            # Save dataframe
            df_train_incre_target.to_csv(os.path.join(path_data_temp, f"train_incre_{t}.csv"))
            df_test_set_target.to_csv(os.path.join(path_data_temp, f"test_set_{t}.csv"))
            df_train_set_target.to_csv(os.path.join(path_data_temp, f"train_set_{t}.csv"))
            df_untrain_target.to_csv(os.path.join(path_data_temp, f"all_untrain_set_{t}.csv"))
    except Exception as e:
        raise Exception(f"An error occurred in the main function: {e}") from e
