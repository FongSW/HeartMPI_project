# import
import pandas as pd
import psycopg2, shutil, os

# import utility function
from utility_function.qualitative.get_data import create_connection_psycopg


# function
def update_used_by_incremental(update_col, mpi_test_id):

    con_staging, con_main = create_connection_psycopg()
    cursor = con_staging.cursor()

    stmt_1 = f"UPDATE used_by_incremental SET {update_col} WHERE mpi_test_id in {mpi_test_id};"
    cursor.execute(stmt_1)

    # commit your changes in the database
    con_staging.commit()

    # closing the connection
    con_staging.close()

def clear_data_temp():
    shutil.rmtree("/opt/airflow/dags/utility_function/qualitative/data_temp/split_data")
    print(f">>>>> Deleted split_data folder.")

def update_trained_data(**kwargs):

    # 1. pull experimental type
    ti = kwargs['ti']
    exp_type = ti.xcom_pull(key='exp_type', task_ids='compare_model_performance')

    # 2. get best experimental each vessel
    update_col = ""
    for vessel, exp in exp_type.items():
        if exp['exp'] == 'Incremental':
            print(f">>>>> {vessel.upper()} : {exp['exp']}")
            update_col = f"{vessel}_quali={True}"

            print(f">>>>> update columns in table used_by_incremental: {update_col}")

            # 3. get mpi_test_id from untrain_data
            untrain_data_path = os.path.join(os.environ["AIRFLOW_QUALITATIVE_PATH"], "data_temp/split_data/new_untrain_data")
            mpi_test_id = pd.read_csv(f"{untrain_data_path}/{vessel}/{vessel}.csv").mpi_test_id.values
            mpi_test_id = tuple(mpi_test_id)

            # 4. update
            if len(update_col) != 0: update_used_by_incremental(update_col, mpi_test_id)

    # 5. Remove data_temp/split_data
    clear_data_temp()
