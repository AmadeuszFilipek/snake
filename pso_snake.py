from functools import reduce
import numpy as np
import math
import matplotlib.pyplot as plt
import pyswarms as ps

from snake import play
import neural_net as net

def particlefy(function):
   def wrapper(particled_weights):
      particles = []
      for particle in particled_weights:
         particles.append(function(particle))
      return particles
   return wrapper


def apply_parameters_to_model(parameters):
   shapes = net.get_model_weight_shapes()
   weights = shape_parameters(shapes, parameters)
   net.model.set_weights(weights)

@particlefy 
def target_function(parameters):
   apply_parameters_to_model(parameters)
   points, moves = play(display=False, step_time=0, collision=False)

   # minus sign for minimization
   return -1 * points # * math.exp(points)

def debug_function(x):
   particles = []
   for particle in x:
      particles.append(particle[0] * particle[0] + particle[1] * particle[1])
   return particles

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

def run_optimisation():
   dimensions = total_parameters(net.get_model_weight_shapes())
   options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
   bounds = create_bounds(dimensions)

   # try:
   #    initial_position = 1
   # except Exception e:
   #    print(e)

   optimizer = ps.single.GlobalBestPSO(
      n_particles=10, dimensions=dimensions,
      options=options)
   cost, pos = optimizer.optimize(target_function, iters=100)
   plot_history(optimizer.cost_history)

   return cost, pos

def plot_history(history):
   plt.plot(history)
   plt.title("Cost history")
   plt.xlabel("Iterations")
   plt.ylabel("Cost")
   plt.show()

if __name__ == "__main__":
   cost, pos = run_optimisation()

   print("BEST COST: {}".format(cost))
   apply_parameters_to_model(pos)
   net.model.save_weights('best_weights')

