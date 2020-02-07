import numpy as np
import itertools as it
import matplotlib.pyplot as plt
import random as rng
import math
from functools import reduce, wraps
import multiprocessing as mp

import pyswarms as ps

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

@particlefy 
def target_function(parameters):
   net = SnakeNet()
   apply_parameters_to_model(net, parameters)
   points = []
   moves = []
   tries = 5

   for t in range(tries):
      pts, mvs, avg_moves = play(
         display=False,
         step_time=0,
         collision=True,
         moves_to_lose=100,
         net=net
         )
      points.append(pts)
      moves.append(mvs)
   # pool = mp.Pool(processes=3)
   # args = it.repeat(parameters, tries)
   # results = pool.map(worker_function, args)

   # points = [r[0] for r in results]
   # moves = [r[1] for r in results]
   
   avg_points = sum(points) / len(points)
   avg_moves = sum(moves) / len(moves)

   return cost_function(avg_points, avg_moves)

def worker_function(parameters):
   net = SnakeNet()
   apply_parameters_to_model(net, parameters)
   pts, mvs, avg_moves = play(
      display=False,
      step_time=0,
      collision=True,
      moves_to_lose=100,
      net=net
      )
   return pts, mvs

def cost_function(points, moves):
   # minus sign for minimization
   result = - 1 * points * points * math.exp(points) \
            - moves + points * math.sqrt(moves)
   return result

@particlefy 
def target_collision_function(parameters):
   apply_parameters_to_model(parameters)
   points, moves = play(
   display=False,
   step_time=0,
   collision=True,
   moves_to_lose=1000
   )

   # minus sign for minimization
   return - moves * moves

@particlefy
def target_apple_function(parameters):
   apply_parameters_to_model(parameters)
   points, moves = play(
   display=False,
   step_time=0,
   collision=False,
   moves_to_lose=20
   )

   # minus sign for minimization
   return -1 * points * math.exp(points)

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

def randomize_positions(dimensions, particles):
   particle_positions = []
   for p in range(particles):
      random_table = 4 * np.random.rand(dimensions) - 2
      particle_positions.append(random_table)

   result = np.array(particle_positions)
   return result

def randomize_old_positions(previous_best, particles):
   particle_positions = []

   for p in range(particles):
      random_table = 0.4 * np.random.rand(len(previous_best)) + 0.8
      randomized_pos = np.multiply(previous_best, random_table)
      particle_positions.append(randomized_pos)

   result = np.array(particle_positions)
   return result

def get_previous_best_pos(net):
   flattened_weights = []
   best_weights = net.model.get_weights()
   for layer_weights in best_weights:
      flattened_weights += (layer_weights.flatten().tolist())

   return np.array(flattened_weights)

def run_optimisation(net, target_function, iterations=10, particles=15, use_old_pos=True):
   dimensions = total_parameters(net.get_model_weight_shapes())
   options = {'c1': 0.5 , 'c2': 0.3, 'w': 0.9}
   

   if use_old_pos:
      net.load_weights()
      old_positions = get_previous_best_pos(net)
      optimizer = ps.single.GlobalBestPSO(
         n_particles=particles,
         dimensions=dimensions,
         options=options,
         init_pos=randomize_old_positions(old_positions, particles)
         )
   else:
      optimizer = ps.single.GlobalBestPSO(
         n_particles=particles,
         dimensions=dimensions,
         options=options,
         init_pos=randomize_positions(dimensions, particles)
         )
   try:
      cost, pos = optimizer.optimize(target_function, iters=iterations, n_processes=3)
   except KeyboardInterrupt:
      cost = final_best_cost = optimizer.swarm.best_cost.copy()
      pos = optimizer.swarm.pbest_pos[optimizer.swarm.pbest_cost.argmin()].copy()
   
   return cost, pos

def plot_history(history):
   plt.plot(history)
   plt.title("Cost history")
   plt.xlabel("Iterations")
   plt.ylabel("Cost")
   plt.show()

if __name__ == "__main__":
   mp.set_start_method('spawn', force=True)
   net = SnakeNet()
   cost, pos = run_optimisation(
      net,
      target_function,
      iterations=4,
      particles=1,
      use_old_pos=True
   )

   print("BEST COST: {}".format(cost))
   apply_parameters_to_model(net, pos)
   net.model.save_weights('./model/best_weights')

