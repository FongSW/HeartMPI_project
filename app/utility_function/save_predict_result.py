import pandas as pd
from datetime import datetime

# import ml_diag table schema
from app.schema.patient_info import ml_diag

# import database connection
from app.config.connection_db import con_db

# import ml_model (df)
from app.utility_function.query_ml_model import ml_model

def insert_result_prediction(series_result_predict):

    insert_data = ml_diag.insert().values(
        mpi_test_id = series_result_predict.mpi_test_id,

        lad_ml_model_id = series_result_predict.lad_ml_model_id,
        lcx_ml_model_id = series_result_predict.lcx_ml_model_id,
        rca_ml_model_id = series_result_predict.rca_ml_model_id,
        patient_ml_model_id = series_result_predict.patient_ml_model_id,

        lad_predict = series_result_predict.predict_lad.lower(),
        lcx_predict = series_result_predict.predict_lcx.lower(),
        rca_predict = series_result_predict.predict_rca.lower(),
        patient_predict = series_result_predict.predict_patient.lower(),

        lad_predict_proba = series_result_predict.predict_prob_lad,
        lcx_predict_proba = series_result_predict.predict_prob_lcx,
        rca_predict_proba = series_result_predict.predict_prob_rca,
        patient_predict_proba = series_result_predict.predict_prob_patient,

        created_at = series_result_predict.created_at,
        updated_at = series_result_predict.created_at,
        updated_by = series_result_predict.updated_by,
    )
    # execute
    con_db.execute(insert_data)


def get_ml_model_dresciption(sr, vessel):
    
    # split pre-fix, sub-fix for query
    pre_fix, sub_fix = sr.split("_")[0].capitalize(), sr.split("_")[1].capitalize()
    if pre_fix == 'Airflow': pre_fix = 'Adaptive'
    
    # query ml_model_id
    if pre_fix == "Base":
        ml_model_id = ml_model.query(f"name=='Base' & indicator=='{sub_fix}' & target=='{vessel}'").id.values[0]
    else:
        ml_model_id = ml_model.query(f"indicator=='{sub_fix}' & target=='{vessel}' & is_best=={True}").id.values[0]

    return ml_model_id

def prepare_to_insert(account_user_id, mpi_test_id, predict_result, inference_name):

    # copy predict_result
    predict_result_copy = predict_result.copy()

    # working datetime
    dt = datetime.now()

    # check result case all-inference
    if len(predict_result_copy.keys()) <= 3:
        df = pd.DataFrame.from_dict(data=predict_result_copy, orient='index').reset_index()
        for vessel in ['LAD', 'LCX', 'RCA', 'PATIENT']:
            df[f'predict_{vessel.lower()}'] = df[f'predict_{vessel.lower()}'].apply(lambda x: "positive" if x == 1 else "negative")
            df[f'{vessel.lower()}_ml_model_id'] = df["index"].apply(get_ml_model_dresciption, args=(vessel,))

        # dataframe to dict 
        predict_result_copy = df.set_index('index').drop(['lad_ml_model_id', 'lcx_ml_model_id', 'rca_ml_model_id', 'patient_ml_model_id'], axis='columns').to_dict('index')
            
    else:
        # set query ml_model condition
        pre_fix, sub_fix = inference_name.split("_")[0].capitalize(), inference_name.split("_")[1].capitalize()

        # chage data type of values from int/float --> "positive" or "negative"
        for i, j in predict_result.items(): 
            if not("_prob_" in i):
                predict_result_copy[i] = "positive" if j == 1 else "negative"
        df = pd.DataFrame(predict_result_copy, index=[0])

        # insert related columns
        for vessel in ['LAD', 'LCX', 'RCA', 'PATIENT']:

            # base
            if pre_fix == "Base":
                df[f"{vessel.lower()}_ml_model_id"] = ml_model.query(f"name=='Base' & indicator=='{sub_fix}' & target=='{vessel}'").id.values[0]

            # airflow
            elif pre_fix == "Adaptive":
                df[f"{vessel.lower()}_ml_model_id"] = ml_model.query(f"indicator=='{sub_fix}' & target=='{vessel}' & is_best=={True}").id.values[0]
        
    df['mpi_test_id']   = [mpi_test_id for _ in range(df.shape[0])]
    df['created_at']    = [dt for _ in range(df.shape[0])]
    df['updated_at']    = [dt for _ in range(df.shape[0])]
    df['updated_by']    = [account_user_id for _ in range(df.shape[0])]

    # insert prediction result to ml_diag table
    print("-" * 25, "Insert prediction result to ml_diag", "-" * 25)
    df.apply(insert_result_prediction, axis=1)
    print(f"The inserted result mpi_test_id {mpi_test_id}. ({inference_name})")

    # return dict prediction 
    print('>>>>> return', predict_result_copy)
    return predict_result_copy

# ------------------------- update result prediction -------------------------------------
def update_result_prediction(series_result_predict):
    condition = ml_diag.c.id == int(series_result_predict.ml_diag_id)
    update_data = ml_diag.update().where(condition).values(
        lad_ml_model_id = series_result_predict.lad_ml_model_id,
        lcx_ml_model_id = series_result_predict.lcx_ml_model_id,
        rca_ml_model_id = series_result_predict.rca_ml_model_id,
        patient_ml_model_id = series_result_predict.patient_ml_model_id,

        lad_predict = series_result_predict.predict_lad.lower(),
        lcx_predict = series_result_predict.predict_lcx.lower(),
        rca_predict = series_result_predict.predict_rca.lower(),
        patient_predict = series_result_predict.predict_patient.lower(),

        lad_predict_proba = series_result_predict.predict_prob_lad,
        lcx_predict_proba = series_result_predict.predict_prob_lcx,
        rca_predict_proba = series_result_predict.predict_prob_rca,
        patient_predict_proba = series_result_predict.predict_prob_patient,

        updated_at = series_result_predict.updated_at
    )
    # execute
    con_db.execute(update_data)



def prepare_to_update(ml_diag_id, predict_result, inference_name):

    # copy predict_result
    predict_result_copy = predict_result.copy()
    # working datetime
    dt = datetime.now()

    # check result case all-inference
    if len(predict_result_copy.keys()) <= 3:
        df = pd.DataFrame.from_dict(data=predict_result_copy, orient='index').reset_index()
        for vessel in ['LAD', 'LCX', 'RCA', 'PATIENT']:
            df[f'predict_{vessel.lower()}'] = df[f'predict_{vessel.lower()}'].apply(lambda x: "positive" if x == 1 else "negative")
            df[f'{vessel.lower()}_ml_model_id'] = df["index"].apply(get_ml_model_dresciption, args=(vessel,))

        # dataframe to dict 
        predict_result_copy = df.set_index('index').drop(['lad_ml_model_id', 'lcx_ml_model_id', 'rca_ml_model_id', 'patient_ml_model_id'], axis='columns').to_dict('index')
            
    else:
        # set query ml_model condition
        pre_fix, sub_fix = inference_name.split("_")[0].capitalize(), inference_name.split("_")[1].capitalize()

        # chage data type of values from int/float --> "positive" or "negative"
        for i, j in predict_result.items(): 
            if not("_prob_" in i):
                predict_result_copy[i] = "positive" if j == 1 else "negative"
        df = pd.DataFrame(predict_result_copy, index=[0])

        # insert related columns
        for vessel in ['LAD', 'LCX', 'RCA', 'PATIENT']:

            # base
            if pre_fix == "Base":
                df[f"{vessel.lower()}_ml_model_id"] = ml_model.query(f"name=='Base' & indicator=='{sub_fix}' & target=='{vessel}'").id.values[0]

            # airflow
            elif pre_fix == "Adaptive":
                df[f"{vessel.lower()}_ml_model_id"] = ml_model.query(f"indicator=='{sub_fix}' & target=='{vessel}' & is_best=={True}").id.values[0]

    #df['ml_diag_id']   = [ml_diag_id for _ in range(df.shape[0])]
    df['ml_diag_id']   = ml_diag_id
    df['updated_at']    = [dt for _ in range(df.shape[0])]

    # insert prediction result to ml_diag table
    print("-" * 25, "Updated prediction result to ml_diag", "-" * 25)
    df.apply(update_result_prediction, axis=1)
    print(f"The updated result ml_diag_id {ml_diag_id}. ({inference_name})")

    # return dict prediction 
    print('>>>>> return', predict_result_copy)
    return predict_result_copy