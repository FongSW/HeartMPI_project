# Import


# Import model utility function
from utility_function.qualitative.experimental.model_util import test_gpu, load_data_set, search_best_hyperparam, train_model, eval_model, save_eval_result

def fully_retrain():

    # 0. test gpu
    test_gpu()

    # 1. load split data set all_data and test_data
    X_train, y_train, X_test, y_test = load_data_set(train="all_train_data")

    # 2. search best hyperparameters for each vessels with keras-tuner
    for vessel in ['lad', 'lcx', 'patient', 'rca']:

        # 2.1 search best hyperparameters
        model, best_hps = search_best_hyperparam(X_train[vessel], y_train[vessel], X_test[vessel], y_test[vessel], vessel, "Fully Re-train")

        # 2.2 train model with all_train_data (new_data 70% + previously_data)
        save_path, version, dt = train_model(model, X_train[vessel], y_train[vessel], X_test[vessel], y_test[vessel], vessel, "Fully Re-train")

        # 2.3 evaluate model (model structure + weight --> eval new_data_test)
        eval_val = eval_model("Fully Re-train", vessel, version, dt, save_path, X_test[vessel], y_test[vessel])

        # 2.4 save evaluate result
        save_eval_result(vessel, eval_val)