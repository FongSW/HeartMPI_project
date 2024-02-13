import os, shutil, psycopg2
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta


def create_connection_psycopg():
    # con_staging = psycopg2.connect(
    #     database=os.environ["STAGING_DB_DATABASE"], 
    #     user=os.environ["STAGING_DB_USER"], 
    #     password=os.environ["STAGING_DB_PASSWORD"], 
    #     host=os.environ["STAGING_DB_HOST"], 
    #     port=os.environ["STAGING_DB_PORT"]
    # )

    # con_main = psycopg2.connect(
    #     database=os.environ["MAIN_DB_DATABASE"], 
    #     user=os.environ["MAIN_DB_USER"], 
    #     password=os.environ["MAIN_DB_PASSWORD"], 
    #     host=os.environ["MAIN_DB_HOST"], 
    #     port=os.environ["MAIN_DB_PORT"]
    # )

    con_staging = psycopg2.connect(
        database=os.environ["DEMO_STAGING_DB_DATABASE"], 
        user=os.environ["DEMO_STAGING_DB_USER"], 
        password=os.environ["DEMO_STAGING_DB_PASSWORD"], 
        host=os.environ["DEMO_STAGING_DB_HOST"], 
        port=os.environ["DEMO_STAGING_DB_PORT"]
    )

    con_main = psycopg2.connect(
        database=os.environ["DEMO_MAIN_DB_DATABASE"], 
        user=os.environ["DEMO_MAIN_DB_USER"], 
        password=os.environ["DEMO_MAIN_DB_PASSWORD"], 
        host=os.environ["DEMO_MAIN_DB_HOST"], 
        port=os.environ["DEMO_MAIN_DB_PORT"]
    )

    return con_staging, con_main

def create_connection():

    # # connect staging database
    # engine_staging = create_engine(os.environ['STAGING_DB'])
    # con_staging = engine_staging.connect()

    # # connect main database
    # engine_main = create_engine(os.environ['MAIN_DB'])
    # con_main = engine_main.connect()

    # connect staging database
    engine_staging = create_engine(os.environ['DEMO_STAGING_DB'])
    con_staging = engine_staging.connect()

    # connect main database
    engine_main = create_engine(os.environ['DEMO_MAIN_DB'])
    con_main = engine_main.connect()

    return con_staging, con_main

def query_maindb(con_main) -> pd.DataFrame:

    # range of data (filter by date)
    end_date = datetime.now() + timedelta(hours=7)
    start_date = end_date - timedelta(days=30)
    print(f">>>>> Strat date: {start_date}\tEnd date: {end_date}")

    # use columns from mpi_test
    use_cols = ",".join(["" + f"mpi_test.{i}" for i in pd.read_sql(f'''SELECT * FROM mpi_test LIMIT 0;''', con_main).columns.tolist()]) + "," + "patient.gender"
    
    # query mpi_test inner join patient (get all data from mainDB.patient)
    mpi_test = pd.read_sql(f'''SELECT {use_cols} FROM mpi_test JOIN patient ON mpi_test.hn_number = patient.hn_number;''', con_main)

    return start_date, end_date, mpi_test

def query_related_table(con_main, con_staging, mpi_test_id, staging_dir):

    # create query condition
    if len(mpi_test_id) == 1:
        query_condition = f"mpi_test_id = {mpi_test_id.values[0]}"
    else:
        query_condition = f"mpi_test_id IN {tuple(mpi_test_id)}"
    
    # related table name
    related_table = ['doctor_diag', 'mpi_crop_img', 'rest_quanti', 'stress_quanti', 'tpd_17_seg']

    # query related table where mpi_test_id in new_data.id 
    for table in related_table:
        use_cols = ",".join(pd.read_sql(f'''SELECT * FROM {table} LIMIT 0;''', con_staging).columns.tolist())
        query = pd.read_sql(f'''SELECT {use_cols} FROM {table} WHERE {query_condition};''', con_main)
        query.to_csv(f"{staging_dir}/staging_{table}.csv", index=False)

def create_used_by_incremental(mpi_test_id, staging_dir):

    # create data
    is_used = [False for _ in range(len(mpi_test_id))]
    used_by_incremental = pd.DataFrame({
        "mpi_test_id": mpi_test_id.tolist(),
        "patient_quanti": is_used,
        "patient_quali": is_used,
        "lad_quanti": is_used,
        "lad_quali": is_used,
        "lcx_quanti": is_used,
        "lcx_quali": is_used,
        "rca_quanti": is_used,
        "rca_quali": is_used,
    })

    used_by_incremental.to_csv(f"{staging_dir}/staging_used_by_incremental.csv", index=False)


def update_sync_data(con_staging):

    # psycop conn
    psycopg_con_staging, psycopg_con_main = create_connection_psycopg()

    # 1. check staging directory
    dir = os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "data_temp", "sync_data")
    is_exist = os.path.exists(dir)

    if is_exist:
        # 2. insert new data for each tables
        for table in ['mpi_test', 'doctor_diag', 'mpi_crop_img', 'rest_quanti', 'stress_quanti', 'tpd_17_seg', 'used_by_incremental']:

            # read data
            use_cols = pd.read_sql(f'''SELECT * FROM {table} LIMIT 0;''', con_staging).columns.tolist()
            df_new = pd.read_csv(f"{dir}/staging_{table}.csv")[use_cols]
            
            # drop old data
            if table == 'mpi_test':
                # Connect to the database
                cursor = psycopg_con_staging.cursor()

                # Create the SQL query
                ids_str = ", ".join(str(id) for id in df_new.id.values)
                query = f"DELETE FROM mpi_test WHERE id IN ({ids_str})"

                # Execute the query
                cursor.execute(query)
                psycopg_con_staging.commit()
            
            # update
            df_new.to_sql(name=table, con=con_staging, if_exists='append', index=False)
            print(f">>>>> Sync update {df_new.shape[0]} row(s) to table {table}.")

        # 3. delete temp files
        shutil.rmtree(dir)
        print(f">>>>> Deleted sync_data folder.")

def sync_update_data(df_heart_mpi, staging_mpi_test, con_staging, con_main, start_date, end_date):

    print("-"*25, "Sync update data process", "-"*25)
    
    if staging_mpi_test.shape[0] == 0:
        print(f">>>>> Have no sync update data between HeartMPI and  Staging")

    else:
        # define save path
        sync_data_dir = os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "data_temp", "sync_data")
        os.mkdir(sync_data_dir)

        # # query updated data id from HeartMPI V1
        # query_condition_1 = df_heart_mpi.id.isin(staging_mpi_test)
        # query_condition_2 = (df_heart_mpi.updated_at >= start_date) & (df_heart_mpi.updated_at <= end_date)
        # query_update_data_id = df_heart_mpi.loc[query_condition_1 & query_condition_2].id
        # print(f">>>>> Have update data in HeartMPI: {len(query_update_data_id)} row(s)")

        # query updated data id from HeartMPI V2
        query = (
            df_heart_mpi
            .merge(staging_mpi_test, how='inner', on='id', suffixes=('_left', '_right'))
            .query("updated_at != created_at_right")
        )
        
        query_update_data_id = query.id
        print(f">>>>> Have update data in HeartMPI: {len(query_update_data_id)} row(s)")

        if len(query_update_data_id) == 0: 
            try:
                shutil.rmtree(os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "data_temp", "sync_data"))
            except:
                pass
            finally:
                return None

        # save mpi_test table tocsv
        (
            df_heart_mpi
            .loc[df_heart_mpi.id.isin(query_update_data_id)]
            .drop(columns=["created_at"])
            .rename(columns={"updated_at": "created_at"})
            .to_csv(f"{sync_data_dir}/staging_mpi_test.csv", index=False)
        )

        if len(query_update_data_id) == 1:
            df_used_by_incremental = pd.read_sql(f'''SELECT * FROM used_by_incremental WHERE mpi_test_id = {query_update_data_id.values[0]};''', con_staging)
        else:
            df_used_by_incremental = pd.read_sql(f'''SELECT * FROM used_by_incremental WHERE mpi_test_id in {tuple(query_update_data_id)};''', con_staging)
        
        df_used_by_incremental.to_csv(f"{sync_data_dir}/staging_used_by_incremental.csv", index=False)

        # query updated data from HeartMPI
        query_related_table(con_main, con_staging, query_update_data_id, sync_data_dir)

        # update Staging
        update_sync_data(con_staging)


def get_data(**kwargs):

    # 0. connect db
    con_staging, con_main = create_connection()

    # 1. query data from main database
    start_date, end_date, mpi_test = query_maindb(con_main)
    # print(f">>>>> Main db mpi_test.id: {sorted(mpi_test.id.tolist())}, Shape: {mpi_test.shape}")

    # 2. query mpi_test.id from staging database (hn_number > created_at)
    staging_mpi_test = pd.read_sql(f'''SELECT id, created_at FROM mpi_test;''', con_staging)

    # 3. sync update data
    sync_update_data(mpi_test, staging_mpi_test, con_staging, con_main, start_date, end_date)

    print("-"*25, "Insert new data process", "-"*25)

    # 4.1. using columns
    use_cols = pd.read_sql(f'''SELECT * FROM mpi_test LIMIT 0;''', con_staging).columns.tolist()
    print(f">>>>> Staging db mpi_test columns: {use_cols}")

    # 4.2. left outer join data from main database & mpi_test.id from staging database
    new_data = (
        pd
        .merge(mpi_test, staging_mpi_test, on="id", how="outer", indicator=True)
        .query("_merge=='left_only'")
        .rename(columns={"updated_at": "created_at"})
    )[use_cols]

    print(f">>>>> New data: {new_data.shape[0]} row(s)")


    if new_data.shape[0] < 1:
        next_job = ["verify_api"]
    else:
        
        # count untrain data
        untrain_data = pd.read_sql(f'''SELECT patient_quali, lad_quali, lcx_quali, rca_quali FROM used_by_incremental;''', con_staging)
        for col in untrain_data.columns: untrain_data[col] = untrain_data[col].map({True: False, False: True})
        untrain_data = min(untrain_data.sum().values)
        # if untrain_data == None: untrain_data = 0

        print(f">>>>> untrain data (only untrain data): {untrain_data} row(s)")
        print(f">>>>> untrain data (untrain_data +  new_data): {untrain_data + new_data.shape[0]} row(s)")

        # on de-buging
        if (untrain_data + new_data.shape[0]) < 40: next_job = ["verify_api"]
        else:  next_job = ["split_data"]

        # 4.3. create directory for save staging temp data
        # parent_dir = "/opt/airflow/dags/utility_function/qualitative/data_temp"
        staging_dir = os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "data_temp", "staging")
        os.mkdir(staging_dir)

        # 4.4. save new data (staging_db.mpi_test) as temp file
        # new_data['created_at'] = datetime.now() + timedelta(hours=7)
        new_data.to_csv(f"{staging_dir}/staging_mpi_test.csv", index=False)

        # 4.5. query related table where mpi_test_id in new_data.id and save as temp file 
        query_related_table(con_main, con_staging, new_data.id, staging_dir)

        # 4.6. create data for used_by_incremental
        create_used_by_incremental(new_data.id, staging_dir)

    # xcom new_data.shape[0]
    ti = kwargs['ti']
    ti.xcom_push(key='new_data', value=next_job)