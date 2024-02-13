import numpy as np
from keras.models import load_model

# import qualitative model structure
from app.utility_function.qualitative.model_utility import *

# import ml_model from query
from app.utility_function.query_ml_model import ml_model

def set_quali_model(quali_base_model, quali_adaptive_model):
    quali_model_global_cache['base'] = quali_base_model
    quali_model_global_cache['adaptive'] = quali_adaptive_model

def validate_is_exists_model():

    print("-" * 25, "Validate loaded models in cache.")

    if ('base' in quali_model_global_cache) and ('adaptive' in quali_model_global_cache):
        quali_base_model = quali_model_global_cache['base']
        quali_adaptive_model = quali_model_global_cache['adaptive']
        print("\t>>>>> Using cached models")

        return quali_base_model, quali_adaptive_model

    else:
        # quali_base_model, quali_adaptive_model = load_qualitative_model_v2(ml_model)
        # quali_model_global_cache['base'] = quali_base_model
        # quali_model_global_cache['adaptive'] = quali_adaptive_model
        print("\t>>>>> Have no models in cache")

def first_burn_gpu(model, vessel):

    print(f"\t{'-' * 3}", f"First burn {vessel}")

    # burn model
    input_size = model.get_config()['layers'][0]['config']['batch_input_shape']
    burned_data = np.random.rand(input_size[1], input_size[2], input_size[3])
    burned_data = np.expand_dims(burned_data, axis=0)
    burn_result = model.predict(burned_data)
    print(f"\t\t>>>>> Burn {vessel} model: {burn_result}")

def load_qualitative_model_v2():

    print("-" * 25, "Load qualitative model")

    # memory growth
    gpus = tf.config.experimental.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(gpus[0], True)

    # query model from db
    base_model_path     = ml_model.query(f"name=='Base' & indicator=='Qualitative' & type=='Base'")
    adaptive_model_path = ml_model.query(f"name=='Adaptive' & indicator=='Qualitative' & is_best=={True}")

    print(f"\t>>>>> Base model id: {base_model_path.id.values}")

    # load model
    quali_base_model, quali_adaptive_model = {}, {}
    for i in ['LAD', 'LCX', 'RCA', 'PATIENT']:

        # load base model and weight
        b_model = load_model(base_model_path.query(f"target=='{i}'").model_dpath.values[0], custom_objects={'specificity_m':specificity_m, 'precision_m':precision_m, 'recall_m':recall_m, 'f1_m':f1_m, 'fnr_m':fnr_m, 'tpr_m':tpr_m, 'tnr_m':tnr_m, 'fpr_m':fpr_m, 'fn_m':fn_m,'tp_m':tp_m,'tn_m':tn_m,'fp_m':fp_m})
        b_model.load_weights(base_model_path.query(f"target=='{i}'").model_dpath.values[0])

        # burn model
        first_burn_gpu(b_model, i)

        quali_base_model[i] = b_model

        # a_model = load_model(adaptive_model_path.query(f"target=={i}").model_dpath.values[0])
        # a_model.load_weights(adaptive_model_path.query(f"target=={i}").model_dpath.values[0])
        # quali_adaptive_model[i] = a_model

    return quali_base_model, quali_adaptive_model


def predict_qualitative_v2(quali_img_data, name):

    # check model variable exists
    quali_base_model, quali_adaptive_model = validate_is_exists_model()

    # choose model type
    if name.lower() == "base": model = quali_base_model
    else: model = quali_adaptive_model

    print("-" * 25, f"Predict {name.capitalize()} qualitative")
    # prediction
    quali_predict_data = dict()
    for k, v in quali_img_data.items():

        predict_vessel = model[k].predict(v)
        quali_predict_data[f'predict_prob_{k.lower()}'] = round( float( np.max( predict_vessel ) ), 2 )
        quali_predict_data[f'predict_{k.lower()}'] = int( np.argmax( predict_vessel, axis=1 ) )

        print(f"\t>>>>> Softmax {k}:\t{predict_vessel}")
        print(f"\t>>>>> Apply np.argmax {k}:\t{int( np.argmax( predict_vessel, axis=1 ) )}")

    for k, v in quali_predict_data.items():
        print(f"\t>>>>> {k}: {v}")

    return quali_predict_data

# Define a global variable
quali_model_global_cache = {}