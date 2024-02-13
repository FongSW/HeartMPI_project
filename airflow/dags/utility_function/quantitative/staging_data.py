from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import psycopg2
import os

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
    
def execute_update_data(conn_path, df, table_name):
    """
    This function is used to update data into a database table.
    Input: Connection URL of the database, Dataframe, Table name
    """
    try:
        engine = create_engine(conn_path)
        with engine.begin() as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
    except Exception as e:
        raise Exception(f"Cannot update data to Staging DB: {e}") from e
    
def insert_staging_data(df_new_data, conn_path_main, conn_staging):
    """
    Insert staging data into various tables based on the provided dataframe.
    Input: df_new_data (Dataframe), conn_path_main (str), conn_staging (str), date_now (str)
    """
    try:
        # Create query condition
        mpi_test_id = df_new_data.mpi_test_id
        if len(mpi_test_id) == 1:
            query_condition = f"mpi_test_id = {mpi_test_id.values[0]}"
        else:
            query_condition = f"mpi_test_id IN {tuple(mpi_test_id)}"

        # Insert staging data in mpi_test table by id mpi_test
        col_mpi_test = execute_query_sql(f"SELECT * FROM mpi_test LIMIT 0;", conn_staging).columns.tolist()
        query_mpi_test = query_condition.replace("mpi_test_id", "mt.id")
        sql_query_staging_mpi_test = f"SELECT mt.*, p.gender FROM mpi_test as mt INNER JOIN patient AS p ON mt.hn_number = p.hn_number\
                                    WHERE {query_mpi_test};"
        df_staging_mpi_test = execute_query_sql(sql_query_staging_mpi_test, conn_path_main)
        df_staging_mpi_test.loc[:, 'created_at'] =  df_staging_mpi_test.loc[:, 'updated_at']
        execute_insert_data(conn_staging, df_staging_mpi_test.loc[:, col_mpi_test], 'mpi_test')

        # Insert staging data in doctor_diag, mpi_crop_img, rest_quanti, stress_quanti, tpd_17_seg 
        related_table = ['doctor_diag', 'mpi_crop_img', 'rest_quanti', 'stress_quanti', 'tpd_17_seg']

        # Query related table where mpi_test_id in new_data.id 
        for table in related_table:
            use_cols = ",".join(execute_query_sql(f"SELECT * FROM {table} LIMIT 0;", conn_staging).columns.tolist())
            df_query = execute_query_sql(f"SELECT {use_cols} FROM {table} WHERE {query_condition};", conn_path_main)
            execute_insert_data(conn_staging, df_query, table)

        # Insert staging data in used_by_incremental execute_update_data
        df_used_by_incremental = df_new_data.loc[:, ['mpi_test_id']]
        df_used_by_incremental.loc[:, ['patient_quanti', 'patient_quali', 'lad_quanti', 'lad_quali',
                                       'lcx_quanti', 'lcx_quali', 'rca_quanti', 'rca_quali']] = False
        execute_insert_data(conn_staging, df_used_by_incremental, 'used_by_incremental')
    except Exception as e:
        raise Exception(f"Cannot insert staging data: {e}") from e
    
def update_staging_data(df_update_data, conn_path_main, conn_staging):
    """
    Update staging data into various tables based on the provided dataframe.
    Input: df_update_data (Dataframe), conn_path_main (str), conn_staging (str), date_now (str)
    """
    try:
        # Create query condition
        mpi_test_id = df_update_data.mpi_test_id
        if len(mpi_test_id) == 1:
            query_condition = f"mpi_test_id = {mpi_test_id.values[0]}"
        else:
            query_condition = f"mpi_test_id IN {tuple(mpi_test_id)}"
        
        related_table_delete_data = ['doctor_diag', 'mpi_crop_img', 'rest_quanti', 'stress_quanti', 'tpd_17_seg', 'used_by_incremental', 'mpi_test']
        
        # Delect row for updating data mpi_test 
        engine = create_engine(conn_staging)
        connection = engine.connect()
        for table_name in related_table_delete_data:
            sql_scripts_delect_data = f"""
                DELETE FROM {table_name} 
                WHERE {query_condition}
                """
            if table_name == 'mpi_test':
                sql_scripts_delect_data = f"""
                DELETE FROM {table_name} 
                WHERE {query_condition.replace("mpi_test_id", "id")}
                """
            connection.execute(sql_scripts_delect_data)
        connection.close()
        
        # Update staging data in mpi_test table by id mpi_test
        col_mpi_test = execute_query_sql(f"SELECT * FROM mpi_test LIMIT 0;", conn_staging).columns.tolist()
        query_mpi_test = query_condition.replace("mpi_test_id", "mt.id")
        sql_query_staging_mpi_test = f"SELECT mt.*, p.gender FROM mpi_test as mt INNER JOIN patient AS p ON mt.hn_number = p.hn_number\
                                    WHERE {query_mpi_test};"
        df_staging_mpi_test = execute_query_sql(sql_query_staging_mpi_test, conn_path_main)
        df_staging_mpi_test.loc[:, 'created_at'] =  df_staging_mpi_test.loc[:, 'updated_at']
        execute_insert_data(conn_staging, df_staging_mpi_test.loc[:, col_mpi_test], 'mpi_test')

        # Insert staging data in doctor_diag, mpi_crop_img, rest_quanti, stress_quanti, tpd_17_seg 
        related_table = ['doctor_diag', 'mpi_crop_img', 'rest_quanti', 'stress_quanti', 'tpd_17_seg']

        # Query related table where mpi_test_id in new_data.id 
        for table in related_table:
            use_cols = ",".join(execute_query_sql(f"SELECT * FROM {table} LIMIT 0;", conn_staging).columns.tolist())
            df_query = execute_query_sql(f"SELECT {use_cols} FROM {table} WHERE {query_condition};", conn_path_main)
            execute_insert_data(conn_staging, df_query, table)

        # Insert staging data in used_by_incremental
        df_used_by_incremental = df_update_data.loc[:, ['mpi_test_id']]
        df_used_by_incremental.loc[:, ['patient_quanti', 'patient_quali', 'lad_quanti', 'lad_quali',
                                       'lcx_quanti', 'lcx_quali', 'rca_quanti', 'rca_quali']] = False
        execute_insert_data(conn_staging, df_used_by_incremental, 'used_by_incremental')
    except Exception as e:
        raise Exception(f"Cannot insert staging data: {e}") from e

# ---------------------------------------------------------------------------------------------------------------------------------
def main(**kwargs):
    """
    This file is used to stage data from the main Database.
    """
    try:
        # Airflow arg
        ti = kwargs['ti']

        # Create datetime
        date_now = datetime.now() + timedelta(hours=7)
        date_before_one_mouth = datetime.now() + timedelta(hours=7) - timedelta(days = 30)
        print('>>>>> current_time: ', date_now)

        # Get environment URL connect DB variables DEMO_
        conn_main_db = os.environ['DEMO_MAIN_DB']
        conn_staging_db = os.environ['DEMO_STAGING_DB']

        # Sql statement AND (date BETWEEN '{date_before_week}' AND '{date_now}')
        query_patient_data_within_1_month = f"SELECT mt.id as mpi_test_id, updated_at  FROM mpi_test AS mt WHERE mt.is_ocr_approved = true and (mt.updated_at BETWEEN '{date_before_one_mouth}' AND '{date_now}');"
        query_staging = "SELECT mt.id as mpi_test_id, created_at FROM mpi_test as mt;"

        # Execute query to get IDs from Main DB and Staging DB
        df_patient = execute_query_sql(query_patient_data_within_1_month, conn_main_db)
        df_staging = execute_query_sql(query_staging, conn_staging_db)
        path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
        df_patient.to_csv(os.path.join(path_data_temp, f"train_set.csv"))
        print(df_patient)
        print(f">>>>> main db mpi_test.id: {df_patient.mpi_test_id.tolist()}, Shape: {df_patient.shape}")

        # Execute query to get IDs from Main DB and Staging DB for check new data and update data
        df_new_data = pd.merge(df_patient, df_staging, on=['mpi_test_id'], how="outer", indicator=True).query('_merge=="left_only" and updated_at != created_at')
        df_new_data.reset_index(inplace = True)
        
        df_update_data = pd.merge(df_patient, df_staging, on=['mpi_test_id'], how="inner", indicator=True).query('updated_at != created_at')
        df_update_data.reset_index(inplace = True)
        print(f">>>>> new data mpi_test.id: {df_new_data.mpi_test_id.tolist()}, Shape: {df_new_data.shape}")
        print(f">>>>> update data mpi_test.id: {df_update_data.mpi_test_id.tolist()}, Shape: {df_update_data.shape}")

        # Update data process    
        if df_update_data.shape[0] != 0:#bug (or 1)
            # Insert staging data
            update_staging_data(df_update_data, conn_main_db, conn_staging_db)
            
        # Staging process
        if df_new_data.shape[0] != 0:#bug (or 1)
            # Insert staging data
            insert_staging_data(df_new_data, conn_main_db, conn_staging_db)
            
            # Check all staging data which is enough for training data and Summary job
            query_all_mpi_test = "SELECT * FROM public.used_by_incremental;"
            df_check = execute_query_sql(query_all_mpi_test, conn_staging_db)
            count_untrain_patient = len(df_check.loc[(df_check.patient_quanti == False)])
            count_untrain_lad = len(df_check.loc[(df_check.lad_quanti == False)])
            count_untrain_lcx = len(df_check.loc[(df_check.lcx_quanti == False)])
            count_untrain_rca = len(df_check.loc[(df_check.rca_quanti == False)])
            print(f'>>>>> count untrain_patient data: {count_untrain_patient}\n\
            count untrain_lad data: {count_untrain_lad}\n\
            count untrain_lcx data: {count_untrain_lcx}\n\
            count untrain_rca data: {count_untrain_rca}\n\
            ')
            # Summary next job and check if there is enough data for training the model
            if min(count_untrain_patient, count_untrain_lad, count_untrain_lcx, count_untrain_rca) >= 40:
                status_log = "have_enough_data"
                print(f"status_log:  {status_log}")
                ti.xcom_push(key='status_log', value=status_log)
            else:
                status_log = "not_enough_data"
                print(f"status_log:  {status_log}")
                ti.xcom_push(key='status_log', value=status_log)

        else:
            status_log = "not_enough_data"
            print(f"status_log:  {status_log}")
            ti.xcom_push(key='status_log', value=status_log)


    except Exception as e:
        raise Exception(f"An error occurred in the main function: {e}") from e
