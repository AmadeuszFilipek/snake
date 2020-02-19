import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # disable tensorflow debug info

import tensorflow as tf
import tensorflowjs as tfjs
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np

class SnakeNet:

   def __init__(self):
      # elu, tanh, softplus
      self.model = models.Sequential()
      self.model.add(layers.Dense(32, activation='relu',input_shape=(32,)))
      self.model.add(layers.Dense(20, activation='relu'))
      self.model.add(layers.Dense(12, activation='relu'))
      self.model.add(layers.Dense(4, activation='softmax'))

   def summary(self):
      self.model.summary()

   def save_model(path):
      tfjs.converters.save_keras_model(self.model, path)

   def load_weights(self, path):
      try:
         self.model.load_weights(path)
      except ValueError as e:
         print("No weights loaded: incompatible model structures.")

   def predict_next_move(self, features):
      prepared_features = prepare_features(features)
      result = self.model.predict(prepared_features)
      return result[0].tolist()

   def get_model_weight_shapes(self):
      weights = self.model.get_weights()
      shapes = []
      for layer_weights in weights:
         shapes.append(layer_weights.shape)
      return shapes

   def get_weights(self):
      return self.model.get_weights()

def prepare_features(features):
   # single batch
   wrap_batches = np.array([features])
   return wrap_batches

if __name__ == "__main__":
   net = SnakeNet()
   net.load_weights('...')
   tfjs.converters.save_keras_model(model, './model')