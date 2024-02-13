# Import
import pandas as pd
import os, random
from glob import glob
from datetime import datetime, timedelta

# Import model utility function
from utility_function.qualitative.experimental.model_util import test_gpu, load_data_set, get_current_best_model, save_eval_result

def eval_model(ml_model, X_test, y_test, vessel):
    # print(f">>>>> Model name: {file_path}")
    # load current best model structure and weight
    current_best_dpath = get_current_best_model(ml_model, vessel)
    h_params = glob(current_best_dpath + '/*.csv')

    # model = load_model(glob(current_best_dpath + '/*.h5'))
    # model.load_weights(glob(current_best_dpath + '/*.h5'))
    # eval_model = model.evaluate(X_test, y_test)

    # mockup eval model
    c_best = ml_model.query(f"target=='{vessel.upper()}' & is_best=={True}")
    tpr = random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])
    tnr = random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])

    # create eval current best dataframe
    eval_model = {
        "id": c_best.id.values,
        "experimental_type": c_best.type.values,
        "target": [vessel.upper()],
        "version": c_best.version.values,
        "created_at": c_best.created_at.values,
        "updated_at": [datetime.now() + timedelta(hours=7)],
        "val_acc": [random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])],
        "val_specificity": [random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])],
        "val_precision": [random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])],
        "val_recall": [random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])],
        "val_f1": [random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])],
        "val_fnr": [1-tnr],
        "val_tpr": [tpr],
        "val_tnr": [tnr],
        "val_fpr": [1-tpr],
        "status": ["Current best model"]
    }

    return pd.DataFrame(eval_model)



def current_best():

    # 0. test gpu
    test_gpu()

    # 1. load split data set all_data and test_data
    X_test, y_test = load_data_set(train="")

    # 2. read current best model info from csv
    ml_model = pd.read_csv(os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "model_temp", "ml_model.csv"))

    # 3. evaluate each vessel
    for vessel in ['lad', 'lcx', 'patient', 'rca']:

        print("*" * 25, f"Evaluate {vessel.upper()}", "*" * 25)

        # 3.1 evaluate model (model structure + weight --> eval test_set)
        eval_val = eval_model(ml_model, X_test[vessel], y_test[vessel], vessel)

        # 3.2 save evaluate result
        save_eval_result(vessel, eval_val)
