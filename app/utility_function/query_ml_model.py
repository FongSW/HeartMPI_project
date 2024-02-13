import pandas as pd

# import database connection
from app.config.connection_db import con_db

def query_ml_acc():

    print("-" * 25, "Query model accuracy")
    
    # query accuracy best model per vessels
    use_cols = "id, name, indicator, type, target, val_acc"
    query_condition = "(name = 'Base') AND (indicator = 'Quantitative' OR indicator = 'Qualitative')"
    df_ml_model = pd.read_sql(f'''SELECT {use_cols} FROM ml_model WHERE {query_condition};''', con_db)

    # declare variables
    indicators  = ['Quantitative', 'Qualitative']
    vessels     = ['LAD', 'LCX', 'RCA', 'PATIENT']

    for i in indicators:
        for v in vessels:
            query = df_ml_model.query(f"indicator=='{i}' & target=='{v}'").val_acc.values[0]
            print(f"\t>>>>> Indicator: {i}\{v}\tModel accuracy: {query}")

            model_acc_global_cache[f"{i[:6].lower()}_{v.lower()}"] = query

def load_qualitative_model() -> pd.DataFrame:

    # print("-" * 25, "Query best ml model from database")

    # query qualitative base / airflow-best model
    ml_model = pd.read_sql(f'''SELECT * FROM ml_model WHERE (is_best = True) OR (name = 'Base')''', con_db)
    # print(f"\t>>>>> ML model: {ml_model.shape}")

    return ml_model

# ml model
ml_model = load_qualitative_model()

# model accuracy (dict)
# ex: {'quanti_lad': 0.88, 'quanti_lcx': 0.96, 'quanti_rca': 0.88, 'quanti_patient': 0.88, 'qualit_lad': 0.8, 'qualit_lcx': 0.75, 'qualit_rca': 0.75, 'qualit_patient': 0.92}
model_acc_global_cache = {}
print(f"Model accuracy: {model_acc_global_cache}")