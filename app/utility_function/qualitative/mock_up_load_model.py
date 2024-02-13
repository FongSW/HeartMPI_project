# import numpy as np
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import Input, Sequential, initializers
# from tensorflow.keras.layers import Dense, Flatten, BatchNormalization, Dropout
# from keras import backend as K
# from keras.models import load_model
# from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
# from keras.utils.data_utils import Sequence
# from keras.applications.vgg19 import VGG19


# def recall_m(y_true, y_pred):
#     true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
#     possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
#     recall = true_positives / (possible_positives + K.epsilon())
#     return recall

# def specificity_m(y_true, y_pred):
#     neg_y_true = 1 - y_true
#     neg_y_pred = 1 - y_pred
#     fp = K.sum(neg_y_true * y_pred)
#     tn = K.sum(neg_y_true * neg_y_pred)
#     specificity = tn / (tn + fp + K.epsilon())
#     return specificity
    
# def precision_m(y_true, y_pred):
#     true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
#     predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
#     precision = true_positives / (predicted_positives + K.epsilon())
#     return precision

# def f1_m(y_true, y_pred):
#     precision = precision_m(y_true, y_pred)
#     recall = recall_m(y_true, y_pred)
#     return 2*((precision*recall)/(precision+recall+K.epsilon()))
  
# def fnr_m(y_true, y_pred):
#     fn = K.sum(K.round(K.clip(y_true * (1 - y_pred), 0, 1)))
#     true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
#     fnr = fn / (fn + true_positives + K.epsilon())
#     return fnr

# def tpr_m(y_true, y_pred):
#     tn = K.sum(K.round(K.clip((1 - y_true) * (1 - y_pred), 0, 1)))
#     fp = K.sum(K.round(K.clip((1 - y_true) * y_pred, 0, 1)))
#     return tn / (tn + fp + K.epsilon())

# def fpt_m(y_true, y_pred):
#     tn = K.sum(K.round(K.clip((1 - y_true) * (1 - y_pred), 0, 1)))
#     fp = K.sum(K.round(K.clip((1 - y_true) * y_pred, 0, 1)))
#     return fp / (tn + fp + K.epsilon())

# def Vgg19model():
#     parameters = {
#         'data_set': 'Pfs_str',
#         'Fine-tuning': 'Freeze layers[:100]',
#         'tf_model': 'VGG19',
#         'dense_units_layer1': 4096,
#         'dense_units_layer2': 2048,
#         'activation': 'ReLU',
#         'dropout': 'None',
#         'learning_rate': 0.001,
#         'batch_size': 4,
#         'n_epochs': 300,
#         'test_size': 0.2
#     }

#     input = Input(shape=(224,224,3))
#     vgg = VGG19(weights='imagenet', include_top = False, input_tensor = input)

#     #freeze
#     if parameters['Fine-tuning'] != 'Freeze layers[:100]':
#         vgg.trainable = False
#     else:
#         for layer in vgg.layers[:100]:
#             layer.trainable = False

#     model = Sequential()
#     model.add(vgg)
#     model.add(Flatten())
#     model.add(BatchNormalization())
#     initializer = tf.keras.initializers.HeNormal()

#     model.add(Dense(4096, activation=parameters['activation'] ,kernel_initializer=tf.keras.initializers.HeNormal()))

#     model.add(BatchNormalization())

#     if parameters['dropout'] == 0.5:
#         model.add(Dropout(parameters['dropout']))

#     initializer2 = tf.keras.initializers.HeNormal()
#     model.add(Dense(2048, activation=parameters['activation'],kernel_initializer=tf.keras.initializers.HeNormal()))

#     model.add(BatchNormalization())
#     model.add(Dense(2, activation='softmax'))

#     model.compile(
#         optimizer=tf.keras.optimizers.Adam(parameters['learning_rate']), 
#         loss='categorical_crossentropy', 
#         metrics=['accuracy', specificity_m, precision_m, recall_m, f1_m, fnr_m, tpr_m, fpt_m]
#     )
#     return model