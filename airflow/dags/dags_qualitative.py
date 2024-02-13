# import
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.task_group import TaskGroup
from dotenv.main import load_dotenv

# load .env varibles
load_dotenv()

# import utility function
from utility_function.qualitative.test_function import test_restart_api, ping_api
from utility_function.qualitative.get_data import get_data
from utility_function.qualitative.insert_data import insert_new_data
from utility_function.qualitative.branch_function import branch_1, branch_2
from utility_function.qualitative.split_data import split_data, split_data_v2
from utility_function.qualitative.prepare_data import perpare_data
from utility_function.qualitative.experimental.fully_retrain import fully_retrain
from utility_function.qualitative.experimental.incremental import incremental
from utility_function.qualitative.experimental.current_best import current_best
from utility_function.qualitative.compare_model import compare_model_performance
from utility_function.qualitative.train_model import train_model_fully_retrain, train_model_incremental
from utility_function.qualitative.save_new_model_db import save_new_model_db
from utility_function.qualitative.save_new_model import save_model
from utility_function.qualitative.update_train_data import update_trained_data

# Simple DAG
with DAG(
    "qualitative",
    schedule_interval="@once", 
    # schedule_interval="@monthly", 
    start_date=datetime(2023, 3, 6), 
    catchup=False, 
    tags=['qualitative']
) as dag:
    

    # Task 1: Get data from main database
    task_1 = PythonOperator(
        task_id='get_data_from_mainDB',
        python_callable=get_data
    )

    # Task 2: Insert new data from main database to staging database
    task_2 = PythonOperator(
        task_id='insert_new_data_to_stagingDB',
        python_callable=insert_new_data
    )

    # Task 3 (branch): Check number of rows data
    task_3 = BranchPythonOperator(
        task_id='check_data',
        python_callable=branch_1
    )

    # Task 4: Split data
    task_4 = PythonOperator(
        task_id='split_data',
        python_callable=split_data_v2
    )

    # Task 5: Prepare data
    task_5 = PythonOperator(
        task_id='prepare_data',
        python_callable=perpare_data
    )

    # Task 6: Experimental model
    with TaskGroup('experimental_model') as task_6:

        # Fully re-train model
        task_6a = PythonOperator(task_id='fully_re-train', python_callable=fully_retrain)

        # Incremental learning
        task_6b = PythonOperator(task_id='incremental', python_callable=incremental)

        # Evaluate current best model
        task_6c= PythonOperator(task_id='current_best', python_callable=current_best)

        # Task group ordering (task_6a  >> [task_6b, task_6c, task_6d] >> task_6e)
        [task_6a , task_6b , task_6c]

    # Task 7: Compare model performance
    task_7 = PythonOperator(
        task_id='compare_model_performance',
        python_callable=compare_model_performance
    )

    # Task 8: select optimal model for each vein
    task_8 = BranchPythonOperator(
        task_id='select_optimal_model',
        python_callable=branch_2,
    )

    # Task 9: Train with data 100 %
    with TaskGroup('train_new_model') as task_9:

        # Fully re-train model
        task_9a = PythonOperator(task_id='fully_re-train', python_callable=train_model_fully_retrain)

        # Incremental learning
        task_9b = PythonOperator(task_id='incremental', python_callable=train_model_incremental)

        # Task group ordering
        [task_9a , task_9b]

    # Task 10: Save new best model to main database
    task_10 = PythonOperator(
        task_id='save_new_model_db',
        python_callable=save_new_model_db
    )


    # Task 11: Save new best (save to folder)
    task_11 = PythonOperator(
        task_id='save_new_model',
        python_callable=save_model
    )

    # Task 12: Update trained data
    task_12 = PythonOperator(
        task_id='update_trained_data',
        python_callable=update_trained_data
    )

    # Task 13: Restart API
    task_13 = SimpleHttpOperator(
        task_id = 'restart_api',
        http_conn_id = 'api_connection', # Connection Parameter
        endpoint='/restrat',
        method='GET'
    )

    # Task n: Verify API
    task_n = HttpSensor(
        task_id = 'verify_api',
        http_conn_id = 'api_connection', # Connection Parameter
        endpoint='/', # End of HTTP Path
        trigger_rule = TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

# Create workflow
task_1 >> task_2 >> task_3
task_3 >> task_n

task_3 >> task_4 >> task_5 >> task_6 >> task_7 >> task_8 >> task_9 >> task_10 >> task_11 >> task_12 >> task_13 >> task_n
task_8 >> task_n
