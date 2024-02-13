# import
import os
import pandas as pd

# function
def compare_model_performance(**kwargs):
    
    # exeprimental type
    exp_type = dict()

    # compare model performance...
    path = os.path.join(os.environ["AIRFLOW_QUALITATIVE_PATH"], "model_temp")

    for vessel in ['lad', 'lcx', 'rca', 'patient']:
        df = pd.read_csv(path + f'/{vessel}_model_performance.csv')
        df = df.sort_values(
            by=["val_specificity", "val_f1", "val_fnr", "val_tpr", "val_fpr", "val_acc"], 
            ascending=[False, False, True, False, True, False]
        )

        # check, has current been being best model after sorting
        # test = "current_model" # new_model
        if df.status.values[0] == "Current best model":
            experimental = {"exp": df.experimental_type.values[0], "status": "current_model", "version": df.version.values[0]}
        else:
            experimental = {"exp": df.experimental_type.values[0], "status": "new_model", "version": df.version.values[0]}

        exp_type[vessel] = experimental
        print(f">>>>> {vessel.upper()} : {experimental}")

    
    ti = kwargs['ti']
    ti.xcom_push(key='exp_type', value=exp_type)