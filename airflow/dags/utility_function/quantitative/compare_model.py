import pandas as pd 
import os

def main(**kwargs):
    # Get variable environment
    ti = kwargs['ti']
    path_data_temp = os.path.join(os.getenv('AIRFLOW_QUANTITATIVE_PATH'), 'data_temp')
    print('>>>>> path_data_temp', path_data_temp)

    # Create empty DataFrames for saving model info
    columns_name =['type', 'target', 'val_acc', 'val_specificity', 'val_precision',
               'val_recall', 'val_f1', 'val_fnr', 'val_tpr', 'val_tnr', 'val_fpr',
               'brand_quanti_model', 'model_dpath', 'type_evaluate']
    result_current_model = pd.DataFrame(columns=columns_name)
    result_best_model = pd.DataFrame(columns=columns_name)

    # Get Best re-train model for each target
    df_result_retrain = compare_retrain_model(ti, columns_name)
    status_next_job = 'Not_found_new_model' 

    for target in ['lad', 'lcx', 'rca', 'patient']:
        # Get result evaluation for current model and incremental learning 
        target_current = pd.DataFrame(ti.xcom_pull(key='evaluate_model', task_ids=f'evaluate_current_model.{target}'), index=[0])
        target_incremental = pd.DataFrame(ti.xcom_pull(key='evaluate_model', task_ids=f'incremental_learning.{target}'), index=[0])
        target_retrain = df_result_retrain.query(f"target == '{target.upper()}'")

        # Check brand_quanti_model and then concatenate result evaluation for each target
        if target_incremental.brand_quanti_model.values[0] in ['xgb', 'lgbm']:
            result_train_target = pd.concat([target_current, target_incremental, target_retrain], ignore_index=True)
        else:
            result_train_target = pd.concat([target_current, target_retrain], ignore_index=True)

        # Find the best model for each target
        eval_result_sort = result_train_target.sort_values(by=["val_acc", "val_precision", "val_specificity", "val_f1",
                                               "val_tpr", "val_tnr", "val_recall", "val_fpr", "val_fnr"],
                                          ascending=[False, False, False, False, False, False, False, True, True]).reset_index(drop=True)
        # Pick the best model for the target
        row_best_model = eval_result_sort.loc[0:0]
        print(f">>>>> Sorted models for {target}:", eval_result_sort.loc[:, ['type_evaluate', 'val_acc', 'target', 'brand_quanti_model']])

        # Append best model
        result_best_model = pd.concat([row_best_model, result_best_model], ignore_index=True)
        result_current_model = pd.concat([target_current, result_current_model], ignore_index=True)

    # Check if there is a new model
    list_type_evaluate = result_best_model.type_evaluate.values.tolist()
    if 'incremental_model' in list_type_evaluate or 're-train_model' in list_type_evaluate:
        status_next_job= 'Have_new_best_model'

    print('status log task: ', status_next_job)
    print('current model: ',result_current_model.loc[:, ['type_evaluate', 'val_acc', 'target', 'brand_quanti_model']])
    print('best model: ',result_best_model.loc[:, ['type_evaluate', 'val_acc', 'target', 'brand_quanti_model']])

        
    # Push status and save data to CSV files
    result_best_model.to_csv(os.path.join(path_data_temp,f"result_best_model.csv"), index=False)
    result_current_model.to_csv(os.path.join(path_data_temp,f"result_current_model.csv"), index=False)

    ti.xcom_push(key='status_log', value = status_next_job)

def compare_retrain_model(ti, columns_name):
    # Create emtey dataframe for conllect result evaluate re-train model
    columns_name =['type', 'target', 'val_acc', 'val_specificity', 'val_precision',
               'val_recall', 'val_f1', 'val_fnr', 'val_tpr', 'val_tnr', 'val_fpr',
               'brand_quanti_model', 'model_dpath', 'type_evaluate']
    df_result_retrain = pd.DataFrame(columns=columns_name)

    # Loop to compare and save model info
    for target in ['patient', 'lad', 'lcx', 'rca']:

        result_retrain_target = pd.DataFrame(columns=columns_name)
        for brand in ['lgbm', 'xgb', 'superlearner']:
            result_eval = ti.xcom_pull(key='evaluate_model', task_ids=f're_train_model_{target}.{brand}')
            result_retrain_target = pd.concat([pd.DataFrame(result_eval, index=[0]), result_retrain_target], ignore_index=True)

        # Find best acc each target re-train model
        eval_result_sort = result_retrain_target.sort_values(by=["val_acc", "val_recall", "val_specificity", "val_precision", "val_f1",
                                               "val_tpr", "val_tnr", "val_fpr", "val_fnr"],
                                          ascending=[False, False, False, True, False, False, False, True, True]).reset_index(drop=True)
        print(f'score evaluate retrain model ({target.upper()}):', eval_result_sort.loc[:, ['type_evaluate', 'val_acc', 'target', 'brand_quanti_model']])
        df_result_retrain = pd.concat([eval_result_sort.loc[0:0], df_result_retrain], ignore_index=True)


    # Push the best re-train models
    print('best retrain model: ', df_result_retrain.loc[:, ['type_evaluate', 'val_acc', 'target', 'brand_quanti_model']])

    return df_result_retrain
