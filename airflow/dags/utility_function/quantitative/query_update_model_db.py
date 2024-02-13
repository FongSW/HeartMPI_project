import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from sqlalchemy import create_engine
from utility_function.quantitative.update_train_data import execute_sql
from utility_function.quantitative.staging_data import execute_insert_data

def query_info_model():
    def connect_main_db():
        try:
            conn_main_db = os.environ['DEMO_MAIN_DB']
            engine = create_engine(conn_main_db)
            conn = engine.connect()
        except:
            raise Exception("Cannot connect to the main DB")
        return conn
    
    try:
        # Query qualitative base / airflow-best model
        conn = connect_main_db()
        df_ml_model = pd.read_sql(f'''SELECT * FROM ml_model WHERE is_best = True and indicator = 'Quantitative' and name = 'Adaptive' ''', conn)
        conn.close()
        print(f">>>>> ML model: {df_ml_model.shape}")
        print(df_ml_model.loc[:,['target', 'version', 'name', 'created_at']])
    
        # Save info model
        df_ml_model.to_csv(os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], f"data_temp/info_current_model.csv"), index=False)
    except:
        raise Exception("Cannot query info current quantitative model from the main DB")

def update_unused_model(list_target, df_info_old_model):
    # Get variables
    conn_database = os.environ['DEMO_MAIN_DB_DATABASE']
    conn_user = os.environ['DEMO_MAIN_DB_USER']
    conn_password = os.environ['DEMO_MAIN_DB_PASSWORD']
    conn_host = os.environ['DEMO_MAIN_DB_HOST']
    conn_port = os.environ['DEMO_MAIN_DB_PORT']

    for t in list_target:
        # Update dpath in DB
        row_update = df_info_old_model.loc[(df_info_old_model.target == t)]
        version =  row_update.version.values[0]
        id_model = row_update.id.values[0]
        des_archived = os.path.join(
            '/', os.environ['MODEL_PATH'], f'airflow/quantitative/archived_model/{t}/{version}'
        )
        print(des_archived)

        # Create SQL for update model
        # Case: Adaptive model
        if row_update.type.values[0] != "Base":
            # Check dpath archived_model {des_archived}
            print(f'>>>>> update unused model of target {t}')
            if os.path.exists(des_archived):
                print(f'>>>>> update dpath model id {id_model}: {des_archived}')
                sql_stmt = f"""UPDATE ml_model SET model_dpath = '{des_archived}', is_best = False WHERE is_best = True AND target = '{t}' AND indicator = 'Quantitative';"""
                
            else:
                raise Exception("Cannot Update unused model. Reason: Not found path archived model or it was base model")
        else:
            # Case: Base model
            sql_stmt = f"""UPDATE ml_model SET is_best = False WHERE is_best = True AND target = '{t}' AND indicator = 'Quantitative';"""

        # Execute_query_sql for update current model
        execute_sql(conn_database, conn_user, conn_password, conn_host, conn_port, sql_stmt)

def update_adapt_graph(adapt_graph, target):
    try:
        # Create sql statement
        sql_stmt = f"""UPDATE ml_model SET adapt_graph = '{adapt_graph}' WHERE is_best = True AND target = '{target}';"""

        # Execute_query_sql for update current model
        conn_database = os.environ['DEMO_MAIN_DB_DATABASE']
        conn_user = os.environ['DEMO_MAIN_DB_USER']
        conn_password = os.environ['DEMO_MAIN_DB_PASSWORD']
        conn_host = os.environ['DEMO_MAIN_DB_HOST']
        conn_port = os.environ['DEMO_MAIN_DB_PORT']
        execute_sql(conn_database, conn_user, conn_password, conn_host, conn_port, sql_stmt)
    except:
        raise Exception("Cannot update adapt_graph on the main DB")

def add_child_graph(parent_dict, child):
    if "child" in parent_dict:
        add_child_graph(parent_dict['child'], child) 
    else:  
        parent_dict['child'] = child
    return parent_dict

def update_log_train_model(df_new_model, df_current_model):
    # Copy data
    new_model = df_new_model.copy() 

    # Load info model after update model in DB to get ID
    df_update_model = pd.read_csv(os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp/info_current_model.csv'))

    # Load log data
    df_log = pd.read_csv(os.path.join('/'+ os.environ['MODEL_PATH'], 'airflow/quantitative/log_train_quantitative_model.csv'))
  
    # Update status log model
    version = (datetime.now() + timedelta(hours=7)).strftime('%d.%m.%Y')
    datenow = (datetime.now() + timedelta(hours=7)).strftime('%d/%m/%Y')
    list_target = new_model.target.values.tolist()
    print(list_target)

    # Update status current model
    df_log.loc[df_log['target'].isin(list_target), ['updated_at', 'status']] = datenow, 'Archived'

    # Update evaluate of current model
    col_update = ['val_acc','val_specificity','val_precision','val_recall','val_f1',
        'val_fnr','val_tpr','val_tnr','val_fpr', 'updated_at']
    for t in ['LAD', 'LCX', 'RCA', 'PATIENT']:
        # Update evaluate of current model
        df_target = df_current_model.loc[(df_current_model.target == t)]
        df_log.loc[(df_log.id == df_target.id.values[0]), col_update] =  df_target.val_acc.values[0], df_target.val_specificity.values[0], df_target.val_precision.values[0], df_target.val_recall.values[0], df_target.val_f1.values[0], df_target.val_fnr.values[0], df_target.val_tpr.values[0], df_target.val_tnr.values[0], df_target.val_fpr.values[0], datenow
    
    # Check have new model for update new model
    if len(list_target) != 0: 
        # Prepare info new model 
        new_model = new_model.merge(df_update_model.loc[:,['id', 'target']], how='inner', on='target')
        new_model.rename(columns={'type': 'experimental_type', 'brand_quanti_model': 'brand_model'}, inplace=True)
        new_model.loc[:, ['created_at','updated_at', 'status']] = datenow, datenow, "Best model"

        # Add new model , errors='ignore'
        list_drop_col = ['model_dpath', 'type_evaluate', 'name', 'indicator', 'is_best']
        df_log = pd.concat([df_log, new_model.drop(columns=list_drop_col)], ignore_index=True) 

    # Save log model
    df_log.to_csv(os.path.join('/' + os.environ['MODEL_PATH'], 'airflow/quantitative/log_train_quantitative_model.csv'), index=False)

def update_current_model_in_db(df_update_model):
    """ 
    Update val_acc, val_specificity, val_precision, val_recall, val_f1, val_fnr,
    val_tpr, val_tnr, val_fpr on the current model  
    """
    date_now = datetime.now() + timedelta(hours=7)
    df_update_model.loc[:, ['updated_at']] = date_now

    # Connect to the PostgreSQL database
    conn_database = os.environ['DEMO_MAIN_DB_DATABASE']
    conn_user = os.environ['DEMO_MAIN_DB_USER']
    conn_password = os.environ['DEMO_MAIN_DB_PASSWORD']
    conn_host = os.environ['DEMO_MAIN_DB_HOST']
    conn_port = os.environ['DEMO_MAIN_DB_PORT']
    list_id = df_update_model.id.values.tolist()

    # Update current model for each model
    print(f">>>>> Update evaluation of current model id: {list_id}")
    for id in list_id:
        row_update = df_update_model.loc[(df_update_model.id == id)]

        # Create SQL statement
        sql = f""" UPDATE ml_model
                SET val_acc = {row_update.val_acc.values[0]},
                val_specificity = {row_update.val_specificity.values[0]},
                val_precision = {row_update.val_precision.values[0]},
                val_recall = {row_update.val_recall.values[0]},
                val_f1 = {row_update.val_f1.values[0]},
                val_fnr = {row_update.val_fnr.values[0]},
                val_tpr = {row_update.val_tpr.values[0]},
                val_tnr = {row_update.val_tnr.values[0]},
                val_fpr = {row_update.val_fpr.values[0]},
                updated_at = '{row_update.updated_at.values[0]}'
                WHERE id = {id}"""

        # Execute SQL statement 
        execute_sql(conn_database, conn_user, conn_password, conn_host, conn_port, sql)
        print('ok')


def update_new_model_into_db(df_new_model, list_target_model, df_old_model):
    # Add data in column: name, indicator, version, is_best
    pd.options.mode.chained_assignment = None  # default='warn'
    date_now = datetime.now() + timedelta(hours=7)
    version = date_now.strftime('%d.%m.%Y')
    df_new_model.loc[:, ['name', 'indicator', 'version', 'is_best', 'created_at', 'updated_at']] = 'Adaptive', 'Quantitative', version, True, date_now, date_now

    # Execute Insert info new model
    conn_main_db = os.environ['DEMO_MAIN_DB']
    execute_insert_data(conn_main_db, df_new_model.drop(columns=['type_evaluate']), "ml_model") 

    # Update info model for geting current id model
    query_info_model()
    df_update_model = pd.read_csv(os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp/info_current_model.csv'))

    # Create(Re-train) adapt_graph or update(Incremental) adapt_graph for update new model
    for target  in list_target_model:
        # Get type train model
        type_model = df_new_model.query(f"target == '{target}'").type_evaluate.values[0]
        # Check id model
        id_model = df_update_model.query(f"target == '{target}'").id.values[0]
        # Create adapt_graph
        dict_adapt_graph = {
                "model_id": int(id_model),
                "name": "Adaptive",
                "indicator": "Quantitative",
                "type": "Fully Re-train",
                "version": version
            } 
        # Check type train model
        print(f'target: {target}')
        if type_model != 're-train_model':
            # Case Incremental: update by create key(child) 
            dict_adapt_graph['type'] = 'Incremental'
            dict_old_graph = json.loads((df_old_model.query(f"target == '{target}'").adapt_graph.values[0]).replace("'", '"'))
            dict_adapt_graph = add_child_graph(dict_old_graph, dict_adapt_graph)
        print('current_adapt_graph: ',dict_adapt_graph)
        json_adapt_graph = json.dumps(dict_adapt_graph)
        
        # Update adapt_graph
        update_adapt_graph(json_adapt_graph, target)


# For JSONEncoder
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def main():
    # Get environment URL connect DB variables
    path_data_temp = os.path.join(os.environ['AIRFLOW_QUANTITATIVE_PATH'], 'data_temp')

    # Read csv result evaluate model and info current model
    df_model = pd.read_csv(os.path.join(path_data_temp, 'result_best_model.csv'))
    df_new_model = df_model.query("type_evaluate != 'current_model'")
    df_current_model = pd.read_csv(os.path.join(path_data_temp, 'result_current_model.csv'))
    df_old_model = pd.read_csv(os.path.join(path_data_temp, 'info_current_model.csv'))

    # Merge data for updating evaluate current model
    df_update_current = df_current_model.merge(df_old_model.loc[:,['id', 'target', 'version']], how='inner', on='target')

    # Check new model target
    list_target_model = df_new_model.target.values.tolist()

    # Update evaluation on the current model
    update_current_model_in_db(df_update_current)

    # Check new model
    print(f">>>>> list target update model: {list_target_model}")
    if len(list_target_model) != 0:
        # Update unused model
        update_unused_model(list_target_model, df_old_model)
        # Add new best model into DataBase
        update_new_model_into_db(df_new_model, list_target_model, df_old_model)
        print(">>>>> Update new best model")
    else:
        print(">>>>> No update new best model")
    
    # Copy data into the log_train_model
    update_log_train_model(df_new_model, df_update_current)
