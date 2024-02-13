# Import
import os
import numpy as np
from glob import glob
from keras.callbacks import EarlyStopping, ModelCheckpoint

# Functions
def get_vessel(training_type, **kwargs):
    ti = kwargs['ti']
    exp_type = ti.xcom_pull(key='exp_type', task_ids='compare_model_performance')

    lst_vessel = []

    for vessel, val in exp_type.items():

        if ('new_model' in  val.values()) and (training_type in  val.values()):
            lst_vessel.append(vessel)
            # print(vessel)
            # print('\t', val.values())

    return lst_vessel

def load_dataset(training_type, vessel_lst, dataset_path):

    print("-" * 25, f"Load dall data for {training_type}")

    X, y = {}, {}

    for vessel in vessel_lst:
        for f in glob(os.path.join(dataset_path, vessel,"*.npy")):

            if 'X' in f: 
                X[vessel] = np.load(f)
            else:
                y[vessel] = np.load(f)

    for k in X.keys():
        print(f"\t{k}")
        print(f"\t\tX: {X[k].shape} \ty: {y[k].shape}")
    print("\n")

    return X, y

def load_tuned_model(training_type, vessel):

    print("-" * 25, f"Load tuned model for {training_type}:{vessel}")

    tuned_model_path    = glob(os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "model_temp", training_type, vessel) + "/*.txt")[0]
    model_name          = tuned_model_path.split('/')[-1]
    print(f"Model name: {model_name}\n")

    model = 1
    # model = load_model(tuned_model_path)
    # model.load_weights(tuned_model_path)

    # mock up return
    return model_name, tuned_model_path, model

    # # real return
    # return model

def train_model(training_type, vessel, model, X, y, save_dir, model_name):

    print("-" * 25, f"Train model {training_type}:{vessel}")

    save_dir = "/".join(save_dir.split("/")[:-1])

    # model.fit(
    #     X, y, 
    #     batch_size=4,
    #     epochs=300, 
    #     workers=512,
    #     callbacks=[
    #         EarlyStopping(monitor='val_accuracy', mode='max', verbose=1, patience=50),
    #         ModelCheckpoint(
    #             filepath=f"{save_dir}/{model_name}.h5", 
    #             monitor='val_accuracy',
    #             mode='max',
    #             verbose=1, 
    #             save_best_only=True,
    #             save_weights_only=False
    #         )
    #     ]
    # )

    # mockup train model and save model
    with open(f"{save_dir}/{model_name}", 'w+') as write_obj:
        write_obj.write(f'mockup model with 100% new data: {model_name} + {training_type}')
    

def train_model_fully_retrain(ti):

    # 1. get vessels from training type
    vessel_lst = get_vessel(training_type="Fully Re-train", ti=ti)

    # 2. defind data path
    dataset_path = os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "data_temp", "split_data", "all_data")

    # 3. load dataset
    X, y = load_dataset("Fully Re-train", vessel_lst, dataset_path)

    # 4. train model for each vessel
    for vessel in vessel_lst:

        # 4.1. load tuned model + weight
        model_name, model_path, model = load_tuned_model("Fully Re-train", vessel)

        # 4.2. get dataset
        X_train, y_train = X[vessel], y[vessel]
        print(f"{vessel}:\tX_train:{X_train.shape}\ty_train:{y_train.shape}")

        # 4.3. train model
        train_model("Fully Re-train", vessel, model, X_train, y_train, model_path, model_name)


def train_model_incremental(ti):

    # 1. get vessels from training type
    vessel_lst = get_vessel(training_type="Incremental", ti=ti)

    # 2. defind data path
    dataset_path = os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "data_temp", "split_data", "new_untrain_data")

    # 3. load dataset
    X, y = load_dataset("Incremental", vessel_lst, dataset_path)

    # 4. train model for each vessel
    for vessel in vessel_lst:

        # 4.1. load tuned model + weight
        model_name, model_path, model = load_tuned_model("Incremental", vessel)

        # 4.2. get dataset
        X_train, y_train = X[vessel], y[vessel]
        print(f"{vessel}:\tX_train:{X_train.shape}\ty_train:{y_train.shape}")

        # 4.3. train model
        train_model("Incremental", vessel, model, X_train, y_train, model_path, model_name)