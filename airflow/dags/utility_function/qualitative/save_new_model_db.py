"""
save new model to db (new version)
1. get experimental result from compare_model.py (xcom)
2. update current best model performance
    2.1. if have new best model
        2.1.1. check current best model is in archive_model
        2.1.2. update path model from best_model to archive_model
3. if new best model is Fully retrain or Incremental
    3.1. query new best model for each vessel from model_temp (csv)
    3.2. insert new best model to mainDB
    3.3. create json structure adaptive model chain
    3.4. update json structure for new best model
"""

# import lib
import psycopg2, json, os
import pandas as pd

# import utility function
from utility_function.qualitative.get_data import create_connection, create_connection_psycopg

# function
def update_current_best(data, status):

    # set connection DB
    con_staging, con_main = create_connection_psycopg()
    cursor = con_main.cursor()

    if status == "Current best model":
        sql = f"""
            UPDATE ml_model 
            SET 
                val_acc = {data.val_acc.values[0]},
                val_specificity = {data.val_specificity.values[0]},
                val_precision = {data.val_precision.values[0]},
                val_recall = {data.val_recall.values[0]},
                val_f1 = {data.val_f1.values[0]},
                val_fnr = {data.val_fnr.values[0]},
                val_tpr = {data.val_tpr.values[0]},
                val_tnr = {data.val_tnr.values[0]},
                val_fpr = {data.val_fpr.values[0]},
                updated_at = '{data.updated_at.values[0]}'
            WHERE id = {data.id.values[0]};
        """

    else:

        # 2.1.1. check current best model is in archive_model
        archive_model_path = os.path.join(os.environ["MODEL_PATH"], f"airflow/qualitative/archived_model/{data.target.values[0]}/{data.version.values[0]}")
        if os.path.exists(archive_model_path):
            raise Exception(f"model id {data.id.values[0]} directory doesn't exist.")

        # 2.1.2. update path model from best_model to archive_model
        sql = f"""
            UPDATE ml_model 
            SET 
                val_acc = {data.val_acc.values[0]},
                val_specificity = {data.val_specificity.values[0]},
                val_precision = {data.val_precision.values[0]},
                val_recall = {data.val_recall.values[0]},
                val_f1 = {data.val_f1.values[0]},
                val_fnr = {data.val_fnr.values[0]},
                val_tpr = {data.val_tpr.values[0]},
                val_tnr = {data.val_tnr.values[0]},
                val_fpr = {data.val_fpr.values[0]},
                model_dpath = '/opt/heartmpi-api-airflow/app/model/airflow/qualitative/archived_model/{data.target.values[0]}/{data.version.values[0]}/',
                updated_at = '{data.updated_at.values[0]}'
            WHERE id = {data.id.values[0]};
        """

    cursor.execute(sql)
    print(f">>>>> Update current {data.target.values[0]} best mode: {data.id.values[0]}")

    # commit your changes in the database
    con_main.commit()

    # closing the connection
    con_main.close()

def insert_new_model(con_main, data):

    df = pd.DataFrame({
        "name": ["Adaptive"],
        "indicator": ["Qualitative"],
        "type": data.experimental_type.values,
        "target": data.target.values,
        "version": data.version.values,
        "val_acc": data.val_acc.values,
        "val_specificity": data.val_specificity.values,
        "val_precision": data.val_precision.values,
        "val_recall": data.val_recall.values,
        "val_f1": data.val_f1.values,
        "val_fnr": data.val_fnr.values,
        "val_tpr": data.val_tpr.values,
        "val_tnr": data.val_tnr.values,
        "val_fpr": data.val_fpr.values,
        "adapt_graph": [None],
        "brand_quanti_model": ["-"],
        "model_dpath": [f'/opt/heartmpi-api-airflow/app/model/airflow/qualitative/best_model/{data.target.values[0]}/'],
        "is_best": [False],
        "created_at": data.created_at.values,
        "updated_at": data.updated_at.values
    })

    # insert data
    insert = df.to_sql(name="ml_model", con=con_main, if_exists='append', index=False)
    print(f">>>>> Insert new {insert} row(s) to table ml_model.")

def add_child_graph(parent, child):
    if "child" in parent:
        add_child_graph(parent['child'], child) 
    else:  
        parent['child'] = child
    return parent

def create_json_structure(con_main, vessel, exp):

    # query ml_model from mainDB
    ml_model = pd.read_sql_table(table_name="ml_model", con=con_main)

    # query current best
    query_current_best = ml_model.query(f"name=='Adaptive' & indicator=='Qualitative' & target=='{vessel.upper()}' & is_best=={True}")
    print(f">>>>> current best {vessel}: {query_current_best.id.values}")
    print(f">>>>> current best adapt graph {query_current_best.adapt_graph.values[0]}")

    # query new best and create json
    query_new_best = ml_model.query(f"name=='Adaptive' & indicator=='Qualitative' & target=='{vessel.upper()}' & is_best=={False}").sort_values(by=["id"], ascending=[True])
    print(f">>>>> new model: {query_new_best.id.values}")
    new_json_structure = {"model_id":int(query_new_best.id.values[-1]), "name":"Adaptive", "indicator":"Qualitative", "type":exp, "version":query_new_best.version.values[-1]}

    # case incremental: if best model from incremental
    if exp == "Incremental":

        # query current best adaptive_graph
        current_json_structure = query_current_best.adapt_graph.values[0]

        # create json structure
        new_json_structure = add_child_graph(current_json_structure, new_json_structure)
    
    print(f">>>>> Adapt graph {new_json_structure}")

    return json.dumps(new_json_structure), int(query_new_best.id.values[-1]), query_current_best.id

def update_json_structure(vessel, json_structure, new_best_id, current_best_id):

    con_staging, con_main = create_connection_psycopg()
    cursor = con_main.cursor()

    # sql 1: update current best model to archive
    try: 
        sql_1 = f"UPDATE ml_model SET is_best={False} WHERE id={int(current_best_id.values[0])};"
        cursor.execute(sql_1)
        print(f">>>>> Update current {vessel} best model id: {current_best_id.values[0]} set is_best=False.")
    except Exception as e:
        print(f">>>>> {vessel} current best model isn't exist.")
        print(f">>>>> {e}")

    # sql 2: update adapt graph to new best and update is best
    sql_2 = f"UPDATE ml_model SET adapt_graph='{json_structure}', is_best={True} WHERE id={new_best_id};"
    cursor.execute(sql_2)
    print(f">>>>> Update new {vessel} best model id: {new_best_id} set is_best=True and update json structure adaptive model chain.")

    con_main.commit()
    con_main.close()

# main function
def save_new_model_db(**kwargs):

    # 0. connect db
    con_staging, con_main = create_connection()

    # 1. get experimental result (xcom)
    ti = kwargs['ti']
    exp_type = ti.xcom_pull(key='exp_type', task_ids='compare_model_performance')

    model_temp_path = os.path.join(os.environ["AIRFLOW_QUALITATIVE_PATH"], "model_temp")
    for vessel, exp in exp_type.items():

        print("*"*25, f"{vessel.upper()}:{exp['exp']}", "*"*25)

        df = pd.read_csv(f"{model_temp_path}/{vessel}_model_performance.csv")

        # 2. update current best model performance
        current_best = df.query(f"id.notna() & status=='Current best model'")
        update_current_best(current_best, exp['status'])

        # 3. if new best model is Fully retrain or Incremental
        if exp['status'] != "current_model":
            
            # 3.1. query new best model for each vessel from model_temp (csv)
            new_best = df.query(f"experimental_type=='{exp['exp']}' & status!='Current best model'")

            # 3.2. insert new best model to mainDB
            insert_new_model(con_main, new_best)

            # 3.3. create json structure adaptive model chain
            new_json_structure, new_best_id, current_best_id = create_json_structure(con_main, vessel, exp['exp'])

            # 3.4. update json structure for new best model
            update_json_structure(vessel, new_json_structure, new_best_id, current_best_id)