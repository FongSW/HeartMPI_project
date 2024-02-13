# import
import pandas as pd

# import utility function
from utility_function.qualitative.save_new_model import clear_model_temp
from utility_function.qualitative.update_train_data import clear_data_temp

# function
def branch_1(**kwargs):
    # Check number of rows data; if data >= x rows then split data
    ti = kwargs['ti']
    next_job = ti.xcom_pull(key='new_data', task_ids='get_data_from_mainDB')
    return next_job
    

def branch_2(**kwargs):
    # check best experimental that each vessel have been using. {"exp": df.type.values[0], "status": "new_model"}
    ti = kwargs['ti']
    exp_type = ti.xcom_pull(key='exp_type', task_ids='compare_model_performance')
    print(exp_type)
    print(exp_type.values())

    exp = [i["status"] for i in exp_type.values()]
    
    if "new_model" in exp:
        print(">>>>> New best")
        return ["train_new_model.fully_re-train", "train_new_model.incremental"]

    else:
        print(">>>>> Only best model")
        clear_model_temp()
        clear_data_temp()
        return ["verify_api"]
    

    

        