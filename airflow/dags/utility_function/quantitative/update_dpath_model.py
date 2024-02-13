import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import os
import shutil

def update_dpath_model():
    """
    This function is used to update the dpath model from the model_temp folder to the archived_model folder.
    """
    # Prepare variable
    path_model_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'model_temp')
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')
    result_best_model = pd.read_csv(os.path.join(path_data_temp,'result_best_model.csv'))
    list_target_model = result_best_model.query("type_evaluate != 'current_model'").target.values.tolist()
    version = (datetime.now() + timedelta(hours=7)).strftime('%d.%m.%Y')

    # Path for archived and best models
    des_archived = os.path.join('/', os.environ['MODEL_PATH'], 'airflow/quantitative/archived_model')
    des_best = os.path.join('/', os.environ['MODEL_PATH'], 'airflow/quantitative/best_model')
    try:
        # Check for new models
        if len(list_target_model) != 0:
            for t in list_target_model:
                # Create dpath for save model
                row_target = result_best_model.loc[(result_best_model.target == t)]
                type_model = row_target.type_evaluate.values[0]
                brand_model = row_target.brand_quanti_model.values[0]

                if type_model == 'incremental_model':
                    dir_target = os.path.join(path_model_temp, f"incremental/{t}")
                else:
                    dir_target = os.path.join(path_model_temp,f"re-train/{t}/{brand_model}")

                des_target_arc = os.path.join(des_archived, f"{t}/{version}")
                des_target_best = os.path.join(des_best, f"{t}")

                # Create directory or clean file in archived model folder
                if os.path.exists(des_target_arc):
                    print(f"Found directory {des_target_arc} is exist")
                    list_file = os.listdir(des_target_arc)
                    if len(list_file) != 0:
                        print(f"Found file in directory {des_target_arc}")
                else:
                    os.makedirs(des_target_arc)
                    print(f"Created directory: {des_target_arc}.")



                # list name file 
                list_old_file = os.listdir(des_target_best)
                list_old_target_arc = os.listdir(des_target_arc)
                list_file_name = os.listdir(dir_target)

                # Clean file in best_model floder 
                if len(list_old_file) != 0:
                    for file in list_old_file:
                        del_file_path = os.path.join(des_target_best, file)
                        os.remove(del_file_path)
                        print(f"Deleted file: {del_file_path} in {dir_target}")
                if len(list_old_target_arc) != 0:
                    for file in list_old_target_arc:
                        del_file_path = os.path.join(des_target_arc, file)
                        os.remove(del_file_path)
                        print(f"Deleted file: {del_file_path} in {dir_target}")
        
                # Copy flie model to archived floder and best floder
                if len(list_file_name) != 0:
                    for file in list_file_name:
                        target_file = os.path.join(dir_target, file)
                        add_file_path_arc = os.path.join(des_target_arc, file)
                        add_file_path_best = os.path.join(des_target_best, file)
                        shutil.copy(target_file, add_file_path_arc)
                        shutil.copy(target_file, add_file_path_best)
                        print(f"Moved file: {file} to {des_archived} and {des_best}")

                # Update dpath in file csv
                result_best_model.loc[(result_best_model.target == t), ['model_dpath']] = des_target_best
        else:
            print("Not have update dpath model")
    except Exception as e:
            raise Exception(f"Failed to update dpath model. Reason: {e}")
        
    # Save the updated file
    result_best_model.to_csv(os.path.join(path_data_temp, f"result_best_model.csv"), index=False)
