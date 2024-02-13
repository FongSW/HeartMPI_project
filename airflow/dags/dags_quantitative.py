from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.task_group import TaskGroup
from dotenv.main import load_dotenv
import os
import pandas as pd

# load .env variables
load_dotenv()

from utility_function.quantitative.staging_data import main as staging_data
from utility_function.quantitative.get_datas import main as get_data_for_train_model
from utility_function.quantitative.prepare_quanti_data_processing import main as prepare_data 
from utility_function.quantitative.re_train_model import lad_xgb_re_train, lcx_xgb_re_train, rca_xgb_re_train, patient_xgb_re_train
from utility_function.quantitative.re_train_model import lad_lgbm_re_train, lcx_lgbm_re_train, rca_lgbm_re_train, patient_lgbm_re_train
from utility_function.quantitative.re_train_model import lad_superlearner_re_train, lcx_superlearner_re_train, rca_superlearner_re_train, patient_superlearner_re_train
from utility_function.quantitative.train_incremental_model import lad_train_incre_model, lcx_train_incre_model, rca_train_incre_model, patient_train_incre_model
from utility_function.quantitative.evaluate_current_model import lad_evaluate_model, lcx_evaluate_model, rca_evaluate_model, patient_evaluate_model
from utility_function.quantitative.fully_train_model import lad_fully_train_model, lcx_fully_train_model, rca_fully_train_model, patient_fully_train_model

from utility_function.quantitative.query_update_model_db import query_info_model, main as save_info_model
from utility_function.quantitative.update_dpath_model import update_dpath_model
from utility_function.quantitative.compare_model import main as compare_model # main
from utility_function.quantitative.update_train_data import main as update_train_data
from utility_function.quantitative.insert_data_for_test import main as insert_function
# compare_retrain_model


# Simple DAG
with DAG(
    "quantitative", 
    schedule_interval=None, 
    start_date=datetime(2023, 3, 6), 
    catchup=False, 
    tags=['quantitative']
) as dag:
        
    def branch_check_untrain_data(**kwargs):
        ti = kwargs['ti']
        #
        status = ti.xcom_pull(key='status_log', task_ids='staging_data')
        print('>>--status: ',status)
        if status == 'have_enough_data':
           next_job = 'get_datas_and_split_datas'
           print('>>>>>-- next_task: ',next_job)
           return [next_job]
        else:
           next_job = 'verify_api'
           print('>>>>>-- next_task: ',next_job)
           return [next_job] 

    def branch_choose_check_best_model(**kwargs):
        ti = kwargs['ti']      
        status = ti.xcom_pull(key='status_log', task_ids='compare_performance_of_mode')
        print(f"status_log: {status}")
        if status == 'Have_new_best_model':
            next_job = 'restart_api'
        else:
            next_job = 'verify_api'
        print('\n>>--choose_branch_2\n>>-- next_task: ',next_job)
        return [next_job]
    
    def branch_choose_target_fully_train_model(**kwargs): 
        path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
        df_best_model = pd.read_csv(os.path.join(path_data_temp, "result_best_model.csv"))
        list_fully_train = df_best_model.loc[df_best_model.type_evaluate != 'current_model', 'target'].tolist()
        list_task = [f'fully_train_model.{target.lower()}' for target in list_fully_train]
        print(f'>>>>> list fully retrain task:{list_task}')
        if len(list_task) == 0:
            list_task = ['updated_dpath_model']
        return list_task

    # Task: Staging datas staging_data
    staging_datas = PythonOperator(
        task_id='staging_data',
        python_callable=staging_data
    )

    # Branch: Check Untrain datas
    branching_1 = BranchPythonOperator(
        task_id='check_untrain_data',
        python_callable=branch_check_untrain_data,
        dag=dag
    )

    # Task: Get datas for train model
    get_datas = PythonOperator(
        task_id='get_datas_and_split_datas',
        python_callable=get_data_for_train_model
    )

    # Task: Prepare datas
    prepare_data = PythonOperator(
        task_id='prepare_data',
        python_callable=prepare_data
    )

    # Task: Load current model
    load_best_model = PythonOperator(
        task_id='load_info_model',
        python_callable=query_info_model
    )
    
    # Task: Re-train model
    with TaskGroup('re_train_model_patient') as patient_re_train_model:
        patient_retrain_xgb = PythonOperator(
                task_id='xgb',
                python_callable=patient_xgb_re_train
            )
        patient_retrain_lgbm = PythonOperator(
                task_id='lgbm',
                python_callable=patient_lgbm_re_train
            )
        patient_retrain_super = PythonOperator(
                task_id='superlearner',
                python_callable=patient_superlearner_re_train
            )
    with TaskGroup('re_train_model_lad') as lad_re_train_model:
        lad_retrain_xgb = PythonOperator(
                task_id='xgb',
                python_callable=lad_xgb_re_train
            )
        lad_retrain_lgbm = PythonOperator(
                task_id='lgbm',
                python_callable=lad_lgbm_re_train
            )
        lad_retrain_super = PythonOperator(
                task_id='superlearner',
                python_callable=lad_superlearner_re_train
            )
    with TaskGroup('re_train_model_lcx') as lcx_re_train_model:
        lcx_retrain_xgb = PythonOperator(
                task_id='xgb',
                python_callable=lcx_xgb_re_train
            )
        lcx_retrain_lgbm = PythonOperator(
                task_id='lgbm',
                python_callable=lcx_lgbm_re_train
            )
        lcx_retrain_super = PythonOperator(
                task_id='superlearner',
                python_callable=lcx_superlearner_re_train
            )
    with TaskGroup('re_train_model_rca') as rca_re_train_model:
        rca_retrain_xgb = PythonOperator(
                task_id='xgb',
                python_callable=rca_xgb_re_train
            )
        rca_retrain_lgbm = PythonOperator(
                task_id='lgbm',
                python_callable=rca_lgbm_re_train
            )
        rca_retrain_super = PythonOperator(
                task_id='superlearner',
                python_callable=rca_superlearner_re_train
            )

    # Task: Train incremental model   
    with TaskGroup('incremental_learning') as incre_model:
        incre_patient = PythonOperator(
            task_id='patient',
            python_callable=patient_train_incre_model
        )
        incre_lad = PythonOperator(
            task_id='lad',
            python_callable=lad_train_incre_model
        )
        incre_lcx = PythonOperator(
            task_id='lcx',
            python_callable=lcx_train_incre_model
        )
        incre_rca = PythonOperator(
            task_id='rca',
            python_callable=rca_train_incre_model
        )
    
    # Task: Evaluate current model  
    with TaskGroup('evaluate_current_model') as eval_model:
        eval_xgb = PythonOperator(
            task_id='patient',
            python_callable=patient_evaluate_model
        )
        eval_lad = PythonOperator(
            task_id='lad',
            python_callable=lad_evaluate_model
        )
        eval_lcx = PythonOperator(
            task_id='lcx',
            python_callable=lcx_evaluate_model
        )
        eval_rca = PythonOperator(
            task_id='rca',
            python_callable=rca_evaluate_model
        )

    # Task: Compare model performance  compare_retrain_model    
    result_model = PythonOperator(
        task_id='compare_performance_of_mode',
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
        python_callable=compare_model
    )
    
    # Branch: Check fully retrain model
    branching_2 = BranchPythonOperator(
        task_id='branch_check_fully_train_model',
        python_callable=branch_choose_target_fully_train_model,
        dag=dag
    )

    with TaskGroup('fully_train_model') as fully_train_model:
        lad_train_task = PythonOperator(
            task_id=f'lad',
            python_callable=lad_fully_train_model
        )
        lcx_train_task = PythonOperator(
            task_id=f'lcx',
            python_callable=lcx_fully_train_model
        )
        rca_train_task = PythonOperator(
            task_id=f'rca',
            python_callable=rca_fully_train_model
        )
        patient_train_task = PythonOperator(
            task_id=f'patient',
            python_callable=patient_fully_train_model
        )

    # Task: Update dpath model
    update_dpath = PythonOperator(
        task_id='updated_dpath_model',
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS, 
        python_callable=update_dpath_model,
    )

    # Task: Save_evaluate_and_info_model in Database
    save_model = PythonOperator(
        task_id='save_info_model',
        python_callable=save_info_model
    )

    # Task: Update train data
    update_data = PythonOperator(
        task_id='update_train_data',
        python_callable=update_train_data,
    )

    # Branch: Check new best model 
    branching_3 = BranchPythonOperator(
        task_id='check_new_best_model',
        python_callable=branch_choose_check_best_model, 
        dag=dag
    )

    # Task: Restart API
    restart_api = SimpleHttpOperator(
        task_id='restart_api',
        http_conn_id='heart_mini_api',
        endpoint='/restrat',
        method='GET'
    )
    
    # Task: Verify API
    vetify_api = HttpSensor(
        task_id = 'verify_api',
        http_conn_id = 'api_connection', 
        endpoint='/',
        trigger_rule = TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

# Create workflow
staging_datas
staging_datas >> branching_1
branching_1 >> vetify_api
branching_1 >> get_datas >> prepare_data >> load_best_model >> \
patient_retrain_xgb >> patient_retrain_lgbm >> patient_retrain_super >> \
lad_retrain_xgb >> lad_retrain_lgbm >> lad_retrain_super >> \
lcx_retrain_xgb >> lcx_retrain_lgbm >> lcx_retrain_super >> \
rca_retrain_xgb >> rca_retrain_lgbm >> rca_retrain_super >> \
incre_patient >> incre_lad >> incre_lcx >> incre_rca >> \
eval_model >> result_model >> branching_2

branching_2 >> fully_train_model >> update_dpath >> save_model >> update_data >> branching_3
branching_2 >> update_dpath >> save_model >> update_data >> branching_3

branching_3  >> restart_api >> vetify_api
branching_3 >> vetify_api
