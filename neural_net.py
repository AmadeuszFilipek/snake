import os
import numpy as np
import glob
import json
from functools import reduce
import pathlib

def alternate(i):
    i = iter(i)
    while True:
        yield(i.__next__(), i.__next__())

def relu(x):
   return x * (x > 0)

def sigmoid(x):
   return 1 / (1 + np.exp(-x))

def softmax(x):
   distribution = np.exp(x)
   return distribution / np.sum(distribution)

def flatten_shaped_parameters(shaped_parameters):
   ''' return flattened and appended list of parameters '''
   raise DeprecationWarning
   flattened_weights = []
      
   for layer in shaped_parameters:
      flattened_weights += (layer.flatten().tolist())

   return flattened_weights

def shape_parameters(shapes, parameters):
   raise DeprecationWarning
   ''' return parameters shaped accordingly as numpy arrays'''
   total = total_parameters(shapes)
   if len(parameters) < total:
      raise ValueError("Parameters list is too short {}".format(len(parameters)))
   
   shaped_arrays = []
   for shape in shapes:
      chunk_length = reduce(lambda x,y: x * y, shape)
      parameter_chunk = parameters[0:chunk_length]
      parameters = parameters[chunk_length:]
      shaped_slice = np.reshape(parameter_chunk, shape)
      shaped_arrays.append(shaped_slice)

   return shaped_arrays

def total_parameters(shapes):
   ''' calculate all parameters from their shapes '''
   parameters = 0
   for shape in shapes:
      parameters += reduce(lambda x,y: x * y, shape)
   return parameters

NAME_TO_FUNCTION = {'relu': relu, 'softmax': softmax, 'sigmoid': sigmoid}

class SnakeNet:

   def __init__(self):
      # shapes: [(32, 20), (20,), (20, 12), (12,), (12, 4), (4,)]
      layer_1      = {'activation':'relu', 'neurons': 20, 'weights': np.ones((32,20)), 'bias': np.ones(20,)}
      layer_2      = {'activation':'relu', 'neurons': 12, 'weights': np.ones((20,12)), 'bias': np.ones(12,)}
      output_layer = {'activation':'softmax', 'neurons': 4, 'weights': np.ones((12,4)), 'bias': np.ones(4,)}

      self.layers = [layer_1, layer_2, output_layer]

   def _predict(self, x):
      propagated_signal = x

      for layer in self.layers:
         weights_matrix = layer['weights']
         bias_vector = layer['bias']
         activation_function = NAME_TO_FUNCTION[layer['activation']]
         aggregated_signal = np.dot(propagated_signal, weights_matrix) + bias_vector
         propagated_signal = activation_function(aggregated_signal)

      return propagated_signal

   def save_weights(self, path):
      if not os.path.exists(path):
         path_obj = pathlib.Path(path)
         path_obj.parent.mkdir(parents=True, exist_ok=True)
      with open(path, 'w+') as file:
         json.dump(self.get_weights(), file)

   def load_weights(self, path):
      if not os.path.exists(path):
         raise ValueError("Path does not exist")
      with open(path, 'r') as file:
         data = json.load(file)
      self.set_weights(data)

   def predict_next_move(self, features):
      result = self._predict(np.array(features))
      return result.tolist()

   def get_model_weight_shapes(self):
      shapes = []
      for layer in self.layers:
         weights_shape = layer['weights'].shape
         bias_shape = layer['bias'].shape
         shapes.append(weights_shape)
         shapes.append(bias_shape)
      return shapes

   def set_weights(self, weights_table):
      for layer, (weights, bias) in zip(self.layers, alternate(weights_table)):
         layer['weights'] = np.array(weights)
         layer['bias'] = np.array(bias)

   def get_weights(self):
      weights = []
      
      for layer in self.layers:
         layer_weight = layer['weights']
         layer_bias = layer['bias']
         weights.append(layer_weight.tolist())
         weights.append(layer_bias.tolist())

      return weights

   # def apply_parameters(self, parameters):
   #    shapes = self.get_model_weight_shapes()
   #    weights = shape_parameters(shapes, parameters)
   #    self.set_weights(weights)

   def total_parameters(self):
      return total_parameters(self.get_model_weight_shapes())

if __name__ == "__main__":
   pass
