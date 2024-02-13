"""
save new model to folder (new version)
1. if {vessel} use new best model
2. delete all files in each vessel best model folder
3. save new best model
    3.1. save new best model to archived_model/{vessel}/{version}/
    3.2. save new best model to best_model/{vessel}/
4. update model loging (csv)
    4.1. read snapshort ml_model (csv)
    4.2. read current table ml_model (database)
    4.3. get current best model for each vessel data in snapshort ml_model
    4.4. insert 4.3. to 4.2.
    4.5. save csv log
5. delete all files in model_temp folder
"""

# import
import os, shutil
import pandas as pd
from datetime import datetime, timedelta
from glob import glob

# import utility function
from utility_function.qualitative.get_data import create_connection

# function
def clear_folder(current_best_path):
    for f in os.listdir(current_best_path):
        os.remove(os.path.join(current_best_path, f))
        print(f">>>>> Removed file: {f}")

def save_new_model(vessel, current_best_path, new_best_path, arc_version_path):
    os.mkdir(arc_version_path)
    for f in os.listdir(new_best_path):

        # 3.1. save new best model to archived_model/{vessel}/{version}/
        shutil.copy(os.path.join(new_best_path, f), os.path.join(arc_version_path, f))
        print(f'>>>>> Moved new {vessel.upper()} model {f} to {arc_version_path}.')

        # 3.2. save new best model to best_model/{vessel}/
        shutil.copy(os.path.join(new_best_path, f), os.path.join(current_best_path, f))
        print(f'>>>>> Moved new {vessel.upper()} model {f} to {current_best_path}.')

def clear_model_temp():
    print("*"*25, "Removed files and folders in model_temp", "*"*25)
    for f in glob(os.path.join(os.environ["AIRFLOW_QUALITATIVE_PATH"], "model_temp/*")):
        
        try:
            shutil.rmtree(f)
            print(f">>>>> Removed folder: {f}")
        except:
            os.remove(f)
            print(f">>>>> Removed file: {f}")

def update_csv_log():

    # 4.0. connect db
    con_staging, con_main = create_connection()

    # 4.1. read snapshort ml_model (csv) & get current best model for each vessel data in snapshort ml_model
    snapshort = pd.read_csv(os.path.join(os.environ["AIRFLOW_QUALITATIVE_PATH"], "model_temp/ml_model.csv"))
    snapshort = snapshort.query(f"is_best=={True}")
    snapshort['is_best'] = snapshort['is_best'].replace([True], False)
    print(f"snapshort ml_model: {snapshort.shape}")
    print(f"snapshort ml_model vessel: {sorted(snapshort.id.values)}")

    # 4.2. read current table ml_model (database)
    ml_model = pd.read_sql_table(table_name="ml_model", con=con_main)
    print(f"current ml_model: {ml_model.shape}")

    # 4.3. insert 4.1. to 4.2.
    ml_model = pd.concat([ml_model, snapshort]).sort_values(by=['id', 'created_at', 'updated_at'], ascending=[True, True, True])
    print(f"concat ml_model: {ml_model.shape}")

    # 4.4. save csv log
    model_log_path = "/" + os.path.join(os.environ["MODEL_PATH"], "airflow/qualitative/model_loging.csv")
    # model_log_path = "/opt/app/model/airflow/qualitative/model_loging.csv"
    ml_model.to_csv(model_log_path, index=False)
    print(f"save log ml_model to: {model_log_path}")

# main function
def save_model(**kwargs):

    ti = kwargs['ti']
    exp_type = ti.xcom_pull(key='exp_type', task_ids='compare_model_performance')
    print(exp_type)

    for vessel, exp in exp_type.items():

        print("*"*25, f"{vessel.upper()}:{exp['exp']}", "*"*25)
        current_best_path = "/" + os.path.join(os.environ["MODEL_PATH"], f"airflow/qualitative/best_model/{vessel.upper()}")
        archived_path = "/" + os.path.join(os.environ["MODEL_PATH"], f"airflow/qualitative/archived_model/{vessel.upper()}")

        # 1. if {vessel} use new best model
        if exp['status'] == 'new_model':
            print(vessel, exp)

            # 2. delete all files in each vessel best model folder
            clear_folder(current_best_path)

            # 3. save new best model
            # new_best_path = f"/opt/airflow/dags/utility_function/qualitative/model_temp/{exp['exp']}/{vessel}"
            new_best_path = os.path.join(os.environ["AIRFLOW_QUALITATIVE_PATH"], f"model_temp/{exp['exp']}/{vessel}")
            arc_version_path = f"{archived_path}/{exp['version']}"
            save_new_model(vessel, current_best_path, new_best_path, arc_version_path)

    # 4. update model loging (csv)
    update_csv_log()
    
    # 5. delete all files in model_temp folder
    clear_model_temp()