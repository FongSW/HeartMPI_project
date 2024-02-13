import pandas as pd
import numpy as np
import psycopg2
import os, shutil
from pathlib import Path



def execute_sql(con_database, con_user, con_password, con_host, con_port, sql_stmt):
    try:   
        conn = psycopg2.connect(
            database=con_database, 
            user=con_user, 
            password=con_password, 
            host=con_host, 
            port=con_port)
        mycursor = conn.cursor()
        mycursor.execute(sql_stmt)
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error: 
        raise Exception(f"Cannot execute update data form DB. Reason: {error}")
    
def delect_temp_file():
    # Delect file in data_temp folder and model_temp folder 'data_temp', 
    list_folder = ['model_temp', 'data_temp']
    for folder in list_folder:
        print(f"--------------deleting files in {folder} folder-----------------------")
        dir = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], f'{folder}')

        # Find file name
        list_file_name = os.listdir(dir)

        # Delect file
        if len(list_file_name) != 0:
            for filename in list_file_name:
                file_path = os.path.join(dir, filename)
                try: # Check file or directory 
                    if os.path.isfile(file_path): 
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
            print(f"{filename} deleted using remove() function")
        else:
            print(f"Not found data  in {folder} folder")
    print("-----------------------------success---------------------------------")

def main():
    # URL to connect to the DB
    conn_staging_db = os.environ['DEMO_STAGING_DB']
    conn_database = os.environ['DEMO_STAGING_DB_DATABASE']
    conn_user = os.environ['DEMO_STAGING_DB_USER']
    conn_password = os.environ['DEMO_STAGING_DB_PASSWORD']
    conn_host = os.environ['DEMO_STAGING_DB_HOST']
    conn_port = os.environ['DEMO_STAGING_DB_PORT']

    # Read the CSV to check for updated staging data used to train the model.
    df_result_best_model = pd.read_csv(os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'],'data_temp/result_best_model.csv'))
    update_target = df_result_best_model.query("type_evaluate != 'current_model'")

    # Loop through and update staging data
    for target in update_target.target.values:
        df_train_set = pd.read_csv(os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], f'data_temp/all_untrain_set_{target.lower()}.csv'))
        used_to_train_id = tuple(int(i) for i in df_train_set.mpi_test_id) # geting mpi Id

        # Create Sql update train data
        if len(used_to_train_id) == 1:
            sql_stmt = f"UPDATE used_by_incremental SET {target.lower()}_quanti = True WHERE mpi_test_id = {used_to_train_id[0]};"
        else:
            sql_stmt = f"UPDATE used_by_incremental SET {target.lower()}_quanti = True WHERE mpi_test_id in {used_to_train_id};"
        
        # Execute update data
        execute_sql(conn_database, conn_user, conn_password, conn_host, conn_port, sql_stmt)
        print(f"Update train data({target}) in used_by_incremental table: {used_to_train_id} mpi_test_id")

    # Delect temporary file in folder data_temp and model_temp
    delect_temp_file()
