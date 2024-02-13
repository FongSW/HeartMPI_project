# Import
import os, random
import pandas as pd
import numpy as np
import tensorflow as tf
import keras_tuner as kt
from glob import glob
from tensorflow.keras.models import load_model
from datetime import datetime, timedelta
from keras import backend as K

# Test GPU
def test_gpu():

    print(f'TensorFlow version: {tf.__version__}')
    print(f'kerasTuner version: {kt.__version__}')
    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    print(tf.reduce_sum(tf.random.normal([1000, 1000])))



# Load data set
def load_data_set(train):

    """
        parameter
            train: "all_data" or "untrain_data"

        This function return load data set in dict format. 
            Example: X_train = {'lad': np_array, 'lcx': np_array, 'patient': np_array, 'rca': np_array}
    """
    print("*" * 25, "Load dataset", "*" * 25)

    # data dict
    X_train, y_train = dict(), dict()
    X_test, y_test = dict(), dict()

    # load dataset  all in format array
    dataset_path = "dags/utility_function/qualitative/data_temp/split_data"

    for data in [train, 'new_data_test']:
        for vessel in ['lad', 'lcx', 'patient', 'rca']:
            for f in glob(os.path.join(dataset_path, data, vessel,"*.npy")):

                # load test set
                if data == 'new_data_test':
                    if "X" in f: 
                        X_test[vessel] = np.load(f)
                    else: 
                        y_test[vessel] = np.load(f)

                # load train set
                else:
                    if "X" in f: 
                        X_train[vessel] = np.load(f)
                    else: 
                        y_train[vessel] = np.load(f)

    # check loading result
    tr_keyword = "train" if train == "all_data" else "untrain"
    for k in [[X_train, f"X_{tr_keyword}"], [y_train, f"y_{tr_keyword}"], [X_test, "X_test"], [y_test, "y_test"]]:
        print(f"*** {k[1]} ***")
        for i, j in k[0].items():
            print(f">>>>> {i}: {j.shape}")
        print()
    
    # return
    if train != "":
        return X_train, y_train, X_test, y_test
    else:
        return X_test, y_test



# compile metrics
def recall_m(y_true, y_pred): # พยากรณ์ว่าป่วยเท่าไหร่ จากผู้ป่วยจริงทั้งหมด
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def specificity_m(y_true, y_pred): # [จำนวนคนไม่ป่วยที่ทำนายถูก / จำนวนคนที่ไม่ป่วยจริงทั้งหมด]
    neg_y_true = 1 - y_true
    neg_y_pred = 1 - y_pred
    fp = K.sum(neg_y_true * y_pred)
    tn = K.sum(neg_y_true * neg_y_pred)
    specificity = tn / (tn + fp + K.epsilon())
    return specificity

def precision_m(y_true, y_pred): # TP / (TP + FP) [จำนวนของคนป่วยที่ทำนายถูก / จำนวนที่ทำนายว่าเป็นคนป่วยทั้งหมด]
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def fnr_m(y_true, y_pred): # FN / (FN + TP) [จำนวนคนป่วยที่ทำนายผิด / จำนวนคนที่ป่วยจริงทั้งหมด]
    fn = K.sum(K.round(K.clip(y_true * (1 - y_pred), 0, 1)))
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    fnr = fn / (fn + true_positives + K.epsilon())
    return fnr

def tpr_m(y_true, y_pred): # TN / (TN + FP) [จำนวนคนไม่ป่วยที่ทำนายถูก / จำนวนคนที่ไม่ป่วยจริงทั้งหมด]
    tn = K.sum(K.round(K.clip((1 - y_true) * (1 - y_pred), 0, 1)))
    fp = K.sum(K.round(K.clip((1 - y_true) * y_pred, 0, 1)))
    return tn / (tn + fp + K.epsilon())

def fpr_m(y_true, y_pred): # FP / (TN + FP) [จำนวนคนไม่ป่วยที่ทำนายผิด / จำนวนคนที่ไม่ป่วยจริงทั้งหมด]
    tn = K.sum(K.round(K.clip((1 - y_true) * (1 - y_pred), 0, 1)))
    fp = K.sum(K.round(K.clip((1 - y_true) * y_pred, 0, 1)))
    return fp / (tn + fp + K.epsilon())



class tune_transfer_model(kt.HyperModel):

  def __init__(self, model_structure, opt):
    self.model = model_structure
    self.opt = opt
    # self.optimizer = opt

  def build(self, hp):
    # hyperparameters
    # hp_optimizer = hp.Choice('optimizer', values=["Adam", "SGD", "RMSprop"])
    hp_lr = hp.Choice('learning_rate', values=[1.0, 0.75, 0.5, 0.25, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7])

    # compiler
    if self.opt == "Adam":
      optimizer = Adam(learning_rate=hp_lr)
    elif self.opt == "SGD":
      optimizer = SGD(learning_rate=hp_lr)
    elif self.opt == "RMSprop":
      optimizer = RMSprop(learning_rate=hp_lr)

    self.model.compile(
      optimizer=optimizer,
      loss='categorical_crossentropy',
      metrics=['accuracy', specificity_m, precision_m, recall_m, f1_m, fnr_m, tpr_m, fpr_m]
    )

    return self.model



# mockup build model for tuning
def build_model(hp):
    print("build model")
    # # build model and assign hyperparameter while tuning model with keras-tuner
    # # hyperparameters
    # hp_conv = hp.Choice('conv', values=['Xception', 'InceptionResNetV2', 'EfficientNetV2M'])
    # hp_layer_1 = hp.Choice('nn_layer_1', values=[2**i for i in range(1, 10)])
    # hp_layer_2 = hp.Choice('nn_layer_2', values=[4**i for i in range(1, 7)])
    # hp_init_weight = hp.Choice('init_weight', values=['zero', 'he_normal', 'glorot_uniform', 'glorot_normal'])
    # hp_activation = hp.Choice('activation', values=['relu', 'tanh'])
    # hp_optimizer = hp.Choice('optimizer', values=['SGD', 'Adam', 'RMSprop'])
    # hp_lr = hp.Choice('learning_rate', values=[1e-1, 1e-2, 1e-3, 1e-4, 1e-5])


    # # input layer
    # input = Input(shape=(224,224,3))

    # # convolution layer
    # if hp_conv == 'Xception':
    #     conv_layer = Xception(weights='imagenet', include_top=False, input_tensor=input)
    # elif hp_conv == 'InceptionResNetV2':
    #     conv_layer = InceptionResNetV2(weights='imagenet', include_top=False, input_tensor=input)
    # elif hp_conv == 'EfficientNetV2M':
    #     conv_layer = EfficientNetV2M(weights='imagenet', include_top = False, input_tensor=input)

    # # freeze layers
    # for layer in conv_layer.layers[:100]:
    #     layer.trainable = False

    # # hidden layers
    # model = Sequential()
    # model.add(conv_layer)
    # model.add(Flatten())
    # model.add(BatchNormalization())
    # model.add(Dense(units=hp_layer_1, activation=hp_activation, kernel_initializer=hp_init_weight))
    # model.add(BatchNormalization())
    # model.add(Dense(units=hp_layer_2, activation=hp_activation, kernel_initializer=hp_init_weight))
    # model.add(BatchNormalization())

    # # output layer
    # model.add(Dense(2, activation='softmax', kernel_initializer=hp_init_weight))

    # # complier
    # model.compile(
    #     optimizer=optimizer,
    #     loss='categorical_crossentropy',
    #     metrics=['accuracy', specificity_m, precision_m, recall_m, f1_m, fnr_m, tpr_m, fpr_m]
    # )

    # return model



# Search best hyperparameters (Fully re-train)
def search_best_hyperparam(X_train, y_train, X_test, y_test, vessel, experimental_type):

    # print
    print("*" * 25, f"Tune hyperparmeters for {experimental_type}: {vessel} model", "*" * 25)

    if experimental_type == "Fully Re-train":
        # # search best hyperparameters with keras-tuner
        # tuner = kt.Hyperband(
        #     hypermodel=build_model,
        #     objective='val_accuracy',
        #     max_epochs=30,
        #     factor=3,
        #     hyperband_iterations=1,
        #     seed=99,
        #     directory = 'dags/utility_function/qualitative/model_temp', # save tune log directory
        #     project_name = f'find_best_{vessel}_retrain_model_log' # folder name
        # )

        # stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', mode='max', patience=5)
        # tuner.search(X_train, y_train, epochs=30, batch_size=4, validation_data=(X_test, y_test), callbacks=[stop_early])

        # # build model with best hyperparameters
        # best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
        # model = tuner.hypermodel.build(best_hps)

        pass

    else:

        # load current best model structure and weight
        ml_model = pd.read_csv(os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "model_temp", "ml_model.csv"))
        current_best_dpath = get_current_best_model(ml_model, vessel)
        # model = load_model_structure(glob(current_best_dpath + '/*.h5'))
        # model = load_model(glob(current_best_dpath + '/*.h5'))
        # model.load_weights(glob(current_best_dpath + '/*.h5'))

        # # Get the optimizer name
        # current_optimizer = model.optimizer.__class__.__name__

        # # search best hyperparameters with keras-tuner
        # tuner = kt.Hyperband(
        #     hypermodel=tune_transfer_model(model, current_optimizer),
        #     objective='val_accuracy',
        #     max_epochs=30,
        #     factor=3,
        #     hyperband_iterations=1,
        #     seed=99,
        #     directory = '/dags/utility_function/qualitative/model_temp', # save tune log directory,
        #     project_name = f'find_best_{vessel}_incremental_model_log' # folder name
        # )

        # tuner.search(X_train, y_train, epochs=30, batch_size=4, validation_data=(X_test, y_test), workers=2024)

        # # get best hyperparameters
        # best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]

        # # set tuning compiler to current best model
        # if current_optimizer == "Adam":
        #     optimizer = Adam(learning_rate=best_hps.values['learning_rate'])
        # elif current_optimizer == "SGD":
        #     optimizer = SGD(learning_rate=best_hps.values['learning_rate'])
        # elif current_optimizer == "RMSprop":
        #     optimizer = RMSprop(learning_rate=best_hps.values['learning_rate'])

        # # train model with best params 
        # model.compile(
        #     optimizer=optimizer,
        #     loss='categorical_crossentropy',
        #     metrics=['accuracy', specificity_m, precision_m, recall_m, f1_m, fnr_m, tpr_m, fpr_m]
        # )

    # real return
    # return model, best_hps.values

    # mockup return 
    return f"{vessel}_model_structure", f"{vessel}_hyperparameters"



def train_model(model, X_train, y_train, X_test, y_test, vessel, experimental_type):

    print("*" * 25, f"Train {experimental_type}:{vessel} model", "*" * 25)

    model_temp_dir = os.path.join(os.environ['AIRFLOW_QUALITATIVE_PATH'], "model_temp")

    # create training model directory (f"dags/utility_function/qualitative/model_temp/{experimental_type}/")
    if not (os.path.exists(os.path.join(model_temp_dir, experimental_type))):
        os.mkdir(os.path.join(model_temp_dir, experimental_type))

    # create save path (f"dags/utility_function/qualitative/model_temp/{experimental_type}/{vessel}")
    save_dir = os.path.join(model_temp_dir, experimental_type, vessel)
    if  os.path.exists(save_dir):
        print(f">>>>> This directory: {save_dir} is exit.")
    else:
        os.mkdir(save_dir)
        print(f">>>>> Create save model directory: {save_dir}")

    # naming model
    dt = datetime.now() + timedelta(hours=7)
    version = f"{dt.strftime('%d')}.{dt.strftime('%m')}.{dt.strftime('%Y')}" # dd.mm.yyyy
    model_name = f"airflow_{vessel}_qualitative_{version}"
    print(f">>>>> Model name: {model_name}")

    # # # train model
    # # model.fit(
    # #     X_train, y_train, 
    # #     batch_size=4,
    # #     epochs=300, 
    # #     validation_data=(X_test, y_test),
    # #     workers=512,
    # #     callbacks=[
    # #         EarlyStopping(monitor='val_accuracy', mode='max', verbose=1, patience=50),
    # #         ModelCheckpoint(
    # #             filepath=f"{save_dir}/{model_name}.h5", 
    # #             monitor='val_accuracy',
    # #             mode='max',
    # #             verbose=1, 
    # #             save_best_only=True,
    # #             save_weights_only=False
    # #         )
    # #     ]
    # # )

    # mockup save model
    with open(f"{save_dir}/{model_name}.txt", 'w+') as write_obj:
        write_obj.write(f'mockup model: {model_name}')

    # # # real return 
    # # return f"{save_dir}/{model_name}.h5"

    # mockup return
    return f"{save_dir}/{model_name}.txt", version, dt



def eval_model(experimental_type, vessel, version, dt, file_path, X_test, y_test):
    print(f">>>>> Model name: {file_path}")
    # model = custom_model(h_params) [ในอนาคตอาจจะไม่ได้ใช้]
    # model = load_model(file_path)
    # model.load_weights(file_path)
    # eval_model = model.evaluate(X_test, y_test)

    # mockup eval model
    tpr = random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])
    tnr = random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])

    eval_model = {
        "id": [None],
        "experimental_type": [experimental_type],
        "target": [vessel.upper()],
        "version": [version],
        "created_at": [dt],
        "updated_at": [dt],
        "val_acc": [random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])],
        "val_specificity": [random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])],
        "val_precision": [random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])],
        "val_recall": [random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])],
        "val_f1": [random.choice([1.00, 0.98, 0.92, 0.88, 0.80, 0.75, 0.68, 0.55])],
        "val_fnr": [1-tnr],
        "val_tpr": [tpr],
        "val_tnr": [tnr],
        "val_fpr": [1-tpr], # val_fpr
        "status": [None]
    }

    return pd.DataFrame(eval_model)



# save evaluate result
def save_eval_result(vessel, eval_result):

    # csv compare path
    file_name = f"{vessel}_model_performance.csv"
    save_dir = f"dags/utility_function/qualitative/model_temp/{file_name}"
    # print(os.path.isfile(save_dir))

    # check is csv file exit
    if os.path.isfile(save_dir):
        print(f">>>>> This csv compare model performance: {save_dir} is exit.")
        eval_result.to_csv(save_dir, mode='a+', header=False, index=False)
    else:
        print(f">>>>> Create csv compare model performance: {save_dir}")
        eval_result.to_csv(save_dir, header=True, index=False)


# get current best model for incremental and current best
def get_current_best_model(ml_model, vessel):

    # model path from mounting
    model_base_path, model_airflow_path = f"{os.environ['MODEL_PATH']}/base/qualitative/{vessel.upper()}", f"{os.environ['MODEL_PATH']}/airflow/qualitative/best_model/{vessel.upper()}"

    # query model for each vessel
    c_best = ml_model.query(f"target=='{vessel.upper()}' & is_best=={True}")

    # get model dpath
    if "base" in c_best.model_dpath.values[0]:
        print(f">>>>> Base model is best model id: {c_best.id.values}")
        return model_base_path
    else:
        print(f">>>>> Adaptive model is best model id: {c_best.id.values}")
        return model_airflow_path