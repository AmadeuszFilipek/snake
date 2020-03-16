import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # disable tensorflow debug info

import tensorflow as tf
import tensorflowjs as tfjs
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
import glob
import json

class SnakeNet:

   def __init__(self):
      # elu, tanh, softplus
      self.model = models.Sequential()
      # first layer is already a working layer, there is no -single-input layer
      # self.model.add(layers.Dense(28, activation='relu',input_shape=(28,)))
      self.model.add(layers.Dense(20, activation='relu', input_shape=(28,)))
      self.model.add(layers.Dense(12, activation='relu'))
      self.model.add(layers.Dense(4, activation='softmax'))
      
      self.compile()

   def compile(self):
      self.model.compile(
         optimizer='adam',
         loss='mean_squared_error' #tf.keras.losses.SparseCategoricalCrossentropy()
         )

   def load_data(self, directory):
      if not os.path.isdir(directory):
         raise ValueError('Is not a directory: ' + directory)
      
      events_of_interest = ['collision', 'starve']

      json_file_paths = glob.glob(directory + '/*.json')
      
      features_list = []
      labels_list = []
      for file_path in json_file_paths:
         with open(file_path, 'r') as file:
            data = json.load(file)
            label = data['label']
            if label not in events_of_interest:
               continue
            features_list.append(data['features'])
            labels_list.append(data['expected_result'])

      return np.array(features_list), np.array(labels_list)

   def train(self):
      features, labels = self.load_data('moves_dataset')
      self.model.fit(features, labels, epochs=10)

   def train_on_single_sample(self, sample, ignore_events=[]):
      event = sample['label']
      if event in ignore_events:
         return
      features = [sample['features']] # single batch
      features = np.array(features)
      
      labels = [sample['expected_result']] # single batch
      labels = np.array(labels)
      
      self.model.fit(features, labels, epochs=1, verbose=0)

   def summary(self):
      self.model.summary()

   def save_model(self, path):
      tfjs.converters.save_keras_model(self.model, path)
      
   def save_weights(self, path):
      self.model.save_weights(path)

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
   net.summary()
   net.load_weights('./model/best_weights')
   # net.compile()
   net.train()
   net.save_weights('./test_model/model')
   # tfjs.converters.save_keras_model(model, './model')