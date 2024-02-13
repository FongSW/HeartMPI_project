import os, random, shutil
import pandas as pd

# import utility function
from utility_function.qualitative.get_data import create_connection

def query_new_data(new_data_id) -> pd.DataFrame:

    # 0. connect db
    con_staging, con_main = create_connection()
    
    # query condition
    if len(new_data_id) == 1:   query_condition = f"mpi_crop_img.mpi_test_id = {new_data_id}"
    else:                       query_condition = f"mpi_crop_img.mpi_test_id IN {new_data_id}"

    # query all data from staging database mpi_crop_img used_by_incremental doctor_diag
    df = (
        pd
        .read_sql(
            f'''
                SELECT * 
                FROM mpi_crop_img 
                JOIN used_by_incremental ON mpi_crop_img.mpi_test_id = used_by_incremental.mpi_test_id
                JOIN doctor_diag ON mpi_crop_img.mpi_test_id = doctor_diag.mpi_test_id
                WHERE {query_condition};
            ''', 
            con_staging
        )
        .drop(columns=['patient_quanti', 'lad_quanti', 'lcx_quanti', 'rca_quanti'])
    )

    # drop duplicated columns
    df = df.loc[:, ~df.columns.duplicated()]

    # segmentation data by vessels
    new_data = {
        'patient': df.drop(columns=['lad_quali', 'lcx_quali', 'rca_quali', 'lad_predict', 'lcx_predict', 'rca_predict']),
        'lad': df.drop(columns=['patient_quali', 'lcx_quali', 'rca_quali', 'patient_predict', 'lcx_predict', 'rca_predict']),
        'lcx': df.drop(columns=['patient_quali', 'lad_quali', 'rca_quali', 'patient_predict', 'lad_predict', 'rca_predict']),
        'rca': df.drop(columns=['patient_quali', 'lad_quali', 'lcx_quali', 'patient_predict', 'lad_predict', 'lcx_predict'])
    }

    return new_data
    
def concat_data(previously_data, new_data_tr) -> dict:

    print("-" * 25, "Previously data + New data", "-" * 25)

    all_data = dict()
    
    for vessel in new_data_tr.keys():
        all_data[vessel] = pd.concat([previously_data[vessel], new_data_tr[vessel]], axis=0)

        print(f"{vessel}: {all_data[vessel].shape}")
    
    return all_data

def adjust_train_data_incremental(previously_data, new_data_tr)-> dict:

    print("-" * 25, "Untrain previously data + New data", "-" * 25)

    new_untrain_data = dict()

    # query untrain data from all previously_data
    for vessel in new_data_tr.keys():

        # query untrain data from all previously_data
        untrain_data = previously_data[vessel].loc[previously_data[vessel][f"{vessel}_quali"] == False]

        # concat untrain with new data
        new_untrain_data[vessel] = pd.concat([untrain_data, new_data_tr[vessel]], axis=0)

        print(f"{vessel}: {new_untrain_data[vessel].shape}")

    return new_untrain_data

def query_all_data(new_data_id) -> dict:

    # 0. connect db
    con_staging, con_main = create_connection()
    
    # query condition
    if len(new_data_id) == 1:
        query_condition = f"mpi_crop_img.mpi_test_id != {new_data_id}"
    else:
        query_condition = f"mpi_crop_img.mpi_test_id NOT IN {new_data_id}"

    # query all data from staging database mpi_crop_img used_by_incremental doctor_diag
    df = (
        pd
        .read_sql(
            f'''
                SELECT * 
                FROM mpi_crop_img 
                JOIN used_by_incremental ON mpi_crop_img.mpi_test_id = used_by_incremental.mpi_test_id
                JOIN doctor_diag ON mpi_crop_img.mpi_test_id = doctor_diag.mpi_test_id
                WHERE {query_condition};
            ''', 
            con_staging
        )
        .drop(columns=['patient_quanti', 'lad_quanti', 'lcx_quanti', 'rca_quanti'])
    )

    # drop duplicated columns
    df = df.loc[:, ~df.columns.duplicated()]

    # segmentation data by vessels
    all_data = {
        'patient': df.drop(columns=['lad_quali', 'lcx_quali', 'rca_quali', 'lad_predict', 'lcx_predict', 'rca_predict']),
        'lad': df.drop(columns=['patient_quali', 'lcx_quali', 'rca_quali', 'patient_predict', 'lcx_predict', 'rca_predict']),
        'lcx': df.drop(columns=['patient_quali', 'lad_quali', 'rca_quali', 'patient_predict', 'lad_predict', 'rca_predict']),
        'rca': df.drop(columns=['patient_quali', 'lad_quali', 'lcx_quali', 'patient_predict', 'lad_predict', 'lcx_predict'])
    }

    return all_data

def query_untrain_data(all_data) -> dict:

    print("*"*25, "Untrain data", "*"*25)

    # untrain dat dict
    untrain_data = dict()

    # query untrain data from all data
    for vessel, df in all_data.items():
        untrain_data[vessel] = df[df[f"{vessel}_quali"] == False]
        print(f"Untrain data {vessel.upper()}: {untrain_data[vessel].shape}")

    return untrain_data

def train_test_split(untrain_data) -> tuple:

    print("-"*25, "Train / Test split New data", "-"*25)

    # variable
    untrain_set, test_set = dict(), dict()
    
    # split
    for vessel, df in untrain_data.items():
        test_data  = df.sample(frac = 0.3, random_state = random.choice([1, 42, 99, 200, 434]))
        train_data = df.drop(test_data.index)
        test_set[vessel] = test_data
        untrain_set[vessel] = train_data

        print(f"{vessel.upper()}: Train data{train_data.shape}, Test data{test_data.shape}")

    return untrain_set, test_set

def drop_test_set(all_data, test_set) -> dict:

    # all data with out test set
    all_data_train = dict()

    # drop test set from all data
    for vessel in all_data.keys():
        all_data_train[vessel] = all_data[vessel].drop(test_set[vessel].index)

    return all_data_train

def save_split_data(data):

    # create directory for save staging temp data
    parent_dir = os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "data_temp", "split_data")
    os.mkdir(parent_dir)

    for data_set, vessel_dict in data.items():

        # create sub-folder
        data_set_dir = os.path.join(parent_dir, data_set)
        os.mkdir(data_set_dir)

        # save data
        for vessel, df in vessel_dict.items():

            # create root path
            root_path = os.path.join(data_set_dir, vessel)
            os.mkdir(root_path)

            # save file
            df.to_csv(os.path.join(root_path, f"{vessel}.csv"), index=False)

def split_data():

    # query all data (dict)
    all_data = query_all_data()

    # query untrain data from all data
    untrain_data = query_untrain_data(all_data)
    
    # split train / test data set (90:10)
    untrain_set, test_set = train_test_split(untrain_data)

    # all data with out test set
    all_data = drop_test_set(all_data, test_set)

    # save all data, untrain data, test data --> csv
    save_split_data({"all_data": all_data, "untrain_data": untrain_set, "test_data": test_set})


def split_data_v2():

    # 1. defind new data
    new_data_path = os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "data_temp", "staging")
    new_data_id = tuple((pd.read_csv(os.path.join(new_data_path, "staging_mpi_test.csv"), usecols=['id']))['id'].values)
    shutil.rmtree(new_data_path)

    # create previous untrain data in case new data < 40 rows
    prev_untrain_path = os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "data_temp", "previous_untrain_data")
    if os.path.exists(prev_untrain_path):
        prev_untrain_id = tuple(pd.read_csv(os.path.join(prev_untrain_path, "staging_mpi_test.csv"), usecols=['id']).id.values.tolist())
        new_data_id += prev_untrain_id

        shutil.rmtree(prev_untrain_path)
        print(f">>>>> Deleted previous untrain folder.")

    print("-" * 25, "New Data", "-" * 25)
    print(f">>>>> New data id: {new_data_id}")

    # 2. query new data
    new_data = query_new_data(new_data_id)

    # 3. query previously data (exclude new data)
    previously_data = query_all_data(new_data_id)

    # 4. split new data (70:30)
    new_data_tr, new_data_te = train_test_split(new_data)

    # 5. new_data 70% + untrain data (previously data that un-used by incremental) --> experimental.incremental
    new_untrain_data_tr = adjust_train_data_incremental(previously_data, new_data_tr)

    # 6. create all data (previously_data + new_data_tr 70%) --> experimental.fully-retrain
    all_train_data = concat_data(previously_data, new_data_tr)

    # 7. new_data 100% + previously data --> train_new_model.fully-retrain
    all_data = concat_data(previously_data, new_data)

    # 8. new_data 100% + untrain data (previously data that un-used by incremental) --> train_new_model.incremental
    new_untrain_data = adjust_train_data_incremental(previously_data, new_data)

    # 8. save all data, untrain data, test data --> csv
    save_split_data(
        {
            "all_data": all_data,                   # train_new_model.fully-retrain
            "all_train_data": all_train_data,       # experimental.fully-retrain
            "new_untrain_data": new_untrain_data,   # train_new_model.incremental
            "new_data_train": new_untrain_data_tr,  # experimental.incremental
            "new_data_test": new_data_te            # test set for all experimental
        }
    )