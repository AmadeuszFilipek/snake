import numpy as np
import itertools as it
import matplotlib.pyplot as plt
import random as rng
import math
from functools import reduce, wraps
import multiprocessing as mp

from evolution import evolution_optimise, Bounds
import crossover_operators as xso
import mutation_operators as mo

from snake import play
from neural_net import SnakeNet

def particlefy(function):
   @wraps(function)
   def wrapper(particled_weights):
      particles = []
      for particle in particled_weights:
         particles.append(function(particle))
      return particles
   return wrapper

def apply_parameters_to_model(net, parameters):
   shapes = net.get_model_weight_shapes()
   weights = shape_parameters(shapes, parameters)
   net.model.set_weights(weights)

def target_function(parameters):
   net = SnakeNet()
   apply_parameters_to_model(net, parameters)
   points = []
   moves = []
   tries = 1

   for t in range(tries):
      pts, mvs, avg_moves, sample = play(
         display=False,
         step_time=0,
         collision=True,
         moves_to_lose=100,
         net=net
         )
      points.append(pts)
      moves.append(mvs)

      # if sample:
      #    net.train_on_single_sample(sample)
   
   avg_points = sum(points) / len(points)
   avg_moves = sum(moves) / len(moves)
   
   cost = cost_function(avg_points, avg_moves)
   # new_parameters = get_flat_weights(net)
   net = None

   return cost

def cost_function(points, moves):
   # minus sign for minimization
   # result = - 1 * 500 * points * points * math.exp(points) \
            # - moves + points * math.sqrt(moves)
   result = - points
   return result

def shape_parameters(shapes, parameters):
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

   return np.array(shaped_arrays)
   
def total_parameters(shapes):
   ''' calculate all parameters from their shapes '''
   parameters = 0
   for shape in shapes:
      parameters += reduce(lambda x,y: x * y, shape)
   return parameters

def create_bounds(dimensions):
   max_bound = 5 * np.ones(dimensions)
   min_bound = 0 * max_bound
   bounds = (min_bound, max_bound)

def get_flat_weights(net):
   flattened_weights = []
   weights = net.model.get_weights()
   for layer_weights in weights:
      flattened_weights += (layer_weights.flatten().tolist())

   return flattened_weights

def plot_history(history):
   plt.plot(history)
   plt.title("Cost history")
   plt.xlabel("Iterations")
   plt.ylabel("Cost")
   plt.show()

if __name__ == "__main__":
   mp.set_start_method('spawn', force=True)
   net = SnakeNet()
   dimensions = total_parameters(net.get_model_weight_shapes())

   crossover_operators = [
      xso.shuffle_crossover(mixing_rate=0.1),
      # xso.shuffle_crossover(mixing_rate=0.5),
      # xso.average_crossover(ratio=0.5),
      xso.average_crossover(ratio=0.1),
      xso.single_point_crossover(),
      xso.identity_crossover()
   ]

   mutation_operators = [
      mo.gauss_mutate(mu=0, sigma=0.1),
      mo.univariate_mutate(mu=0, sigma=0.1),
      mo.spike_mutate(bounds=Bounds(min=-10, max=10)),
      mo.negate_mutate(),
      mo.null_mutate()
   ]
   
   best_snake = evolution_optimise(
      target_function,
      dimensions,
      crossover_operators=crossover_operators,
      mutation_operators=mutation_operators,
      population_size=500,
      generations=1000,
      should_load_population=True,
      load_directory='train_32_inputs',
      should_save_population=True,
      save_directory='train_32_inputs_investigation',
      workers=4,
      allowed_seconds= 60 * 60 * 1
   )

   cost, pos = best_snake.cost, best_snake.gene

   print("BEST COST: {}".format(cost))
   apply_parameters_to_model(net, pos)
   net.model.save_weights('./model/best_weights')

