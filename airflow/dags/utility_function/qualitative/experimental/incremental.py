# Import

# Import model utility function
from utility_function.qualitative.experimental.model_util import test_gpu, load_data_set, search_best_hyperparam, train_model, eval_model, save_eval_result

def incremental():

    # 0. test gpu
    test_gpu()

    # 1. load split data set all_data and test_data
    X_train, y_train, X_test, y_test = load_data_set(train="new_data_train")

    # 2. search best hyperparameters for each vessels with keras-tuner
    for vessel in ['lad', 'lcx', 'patient', 'rca']:

        # 2.1 search best hyperparameters only compiler
        model, best_hps = search_best_hyperparam(X_train[vessel], y_train[vessel], X_test[vessel], y_test[vessel], vessel, "Incremental")

        # 2.2 train model
        save_path, version, dt = train_model(model, X_train[vessel], y_train[vessel], X_test[vessel], y_test[vessel], vessel, "Incremental")

        # 2.3 evaluate model (model structure + weight --> eval test_set)
        eval_val = eval_model("Incremental", vessel, version, dt, save_path, X_test[vessel], y_test[vessel])

        # 2.4 save evaluate result
        save_eval_result(vessel, eval_val)