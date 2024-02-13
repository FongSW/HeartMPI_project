import os
import numpy as np
import pandas as pd
from glob import glob

from utility_function.qualitative.get_data import create_connection

def load_img_array(img_path, vessel):
    
    # 1. change patient to test type (perfusion, severity, def-severity, blackout)
    if vessel not in ['lad', 'lcx', 'rca']: vessel = 'perfusion'

    # 2. edit path
    img_path = img_path.replace("/opt/heartmpi-front-web/data/4dm-mpi/", "/opt/airflow/dags/heartmpi-front-web/data/4dm-mpi/")

    # 3. load npy file with numpy, normlize them and expandimension for vertical stack dataset
    path_file = glob(f'/{img_path}/*{vessel}.npy')[0]
    img = np.load(path_file) / 255
    img = np.expand_dims(img, axis=0)
    return img

def perpare_data():

    # 1. read csv data and get image path
    data_dir = os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "data_temp", "split_data")
    for data in os.listdir(data_dir):
        for target in ['patient', 'lad', 'lcx', 'rca']:

            # 1.1 read csv data and get image path
            path_file = os.path.join(data_dir, data, target, target) + '.csv'
            im_df = pd.read_csv(path_file, usecols=['stress_perfusion_dpath', f'{target}_predict'])

            # 1.2 get crop images by image path (mockup use only perfusion stress) and vertical stacked im_array
            im_array = np.vstack(im_df.stress_perfusion_dpath.apply(load_img_array, args=(target,)))
            
            # 1.3 save npy dataset X, y
            save_X_path = os.path.join(data_dir, data, target, f"X_{target}.npy")
            save_y_path = os.path.join(data_dir, data, target, f"y_{target}.npy")
            np.save(save_X_path, im_array)
            np.save(save_y_path, im_df[f'{target}_predict'].values)

            # 1.4 print result
            print(f'>>>>> {data} {target}: {im_array.shape}')
            print(f'>>>>> Save {data} {target} X, y at: {save_X_path}')
            print(f"-" * 50)

    # 2. pre-query best model for use in docker in docker
    con_staging, con_main = create_connection()
    ml_model = pd.read_sql(sql="SELECT * FROM ml_model WHERE indicator='Qualitative'", con=con_main)
    ml_model.to_csv(os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "model_temp", "ml_model.csv"), index=False)