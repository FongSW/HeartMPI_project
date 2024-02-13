import shutil, os
import pandas as pd
from datetime import datetime, timedelta

# import utility function
from utility_function.qualitative.get_data import create_connection

def insert_new_data(**kwargs):

    # 0. connect db
    con_staging, con_main = create_connection()

    # 1. check staging directory
    staging_dir = os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "data_temp", "staging")
    is_exist = os.path.exists(staging_dir)

    if is_exist:
        # 2. insert new data for each tables
        for table in ['mpi_test', 'doctor_diag', 'mpi_crop_img', 'rest_quanti', 'stress_quanti', 'tpd_17_seg', 'used_by_incremental']:
            
            # read data
            df = pd.read_csv(f"{staging_dir}/staging_{table}.csv")

            # insert data
            insert = df.to_sql(name=table, con=con_staging, if_exists='append', index=False)
            print(f">>>>> Insert new {insert} row(s) to table {table}.")

        # 3. delete temp files
        for f in os.listdir(staging_dir):
            if f != "staging_mpi_test.csv": os.remove(os.path.join(staging_dir, f))
        # shutil.rmtree(staging_dir)
        print(f">>>>> Deleted staging folder.")

        ti = kwargs['ti']
        next_job = ti.xcom_pull(key='new_data', task_ids='get_data_from_mainDB')

        # case new data < 40 rows
        if next_job == ["verify_api"]:

            # create previous untrain data in case new data < 40 rows
            prev_untrain_path = os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "data_temp", "previous_untrain_data")
            os.mkdir(prev_untrain_path)
            
            for f in os.listdir(staging_dir):

                # move staging data to previous untrain data
                shutil.copy(os.path.join(staging_dir, f), os.path.join(prev_untrain_path, f))
                print(f'>>>>> Moved "{staging_dir}/{f}" to "{prev_untrain_path}/{f}".')

            shutil.rmtree(staging_dir)

    else:
        print(">>>>> Have no new data.")