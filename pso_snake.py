from functools import reduce
import numpy as np
import math
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
   points, moves = play(display=False, step_time=0)

   # minus sign for minimization
   return -1 * math.exp(points) * math.sqrt(moves)

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

def run_optimisation():
   dimensions = total_parameters(net.get_model_weight_shapes())
   options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}#, 'k': 10, 'p': 2}
   # Call instance of PSO
   optimizer = ps.single.GlobalBestPSO(
      n_particles=20, dimensions=dimensions, options=options)

   # Perform optimization
   cost, pos = optimizer.optimize(target_function, iters=100)
   return cost, pos

if __name__ == "__main__":
   cost, pos = run_optimisation()

   print('BEST COST:{}'.format(cost))
   net.model.save_weights('best_weights')

