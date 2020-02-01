import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # disable tensorflow debug info

import tensorflow as tf
import tensorflowjs as tfjs
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np

# elu, tanh, softplus
model = models.Sequential()
model.add(layers.Dense(22, activation='tanh',input_shape=(22,)))
model.add(layers.Dense(16, activation='tanh'))
model.add(layers.Dense(8, activation='tanh'))
model.add(layers.Dense(4, activation='softmax'))

model.summary()

try:
   model.load_weights('best_weights')
   tfjs.converters.save_keras_model(model, './model')
except ValueError as e:
   print("No weights loaded: incompatible model structures.")

def predict_next_move(features):
   prepared_features = prepare_features(features)
   result = model.predict(prepared_features)
   return result[0].tolist()

def prepare_features(features):
   wrap_batches = np.array([features]) # single batch
   return wrap_batches

def get_model_weight_shapes():
   weights = model.get_weights()
   shapes = []
   for layer_weights in weights:
      shapes.append(layer_weights.shape)
   return shapes

if __name__ == "__main__":
    model.load_weights('best_weights')
    tfjs.converters.save_keras_model(model, './model')