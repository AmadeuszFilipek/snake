import numpy as np
import itertools as it
import random as rng
import math
import multiprocessing as mp

from evolution import evolution_optimise, Bounds
import crossover_operators as xso
import mutation_operators as mo

from snake import play
from neural_net import SnakeNet

def target_function(parameters):

   net = SnakeNet()
   net.apply_parameters(parameters)
   points = []
   moves = []
   tries = 100

   for t in range(tries):
      pts, mvs, avg_moves = play(
         display=False,
         # step_time=0.1,
         collision=True,
         moves_to_lose=100,
         net=net
         )
      points.append(pts)
      moves.append(mvs)
   
   avg_points = sum(points) / len(points)
   avg_moves = sum(moves) / len(moves)
   
   cost = cost_function(avg_points, avg_moves)

   return cost

def cost_function(points, moves):
   # minus sign for minimization
   # result = - (moves + 2 ** points + (points ** 2.1) * 500 + (((0.25 * moves) ** 1.3) * (points ** 1.2)))
   # result = - points * points * math.exp(points) \
   #          - moves + points * math.sqrt(moves)
   result = - math.exp(points) # lets just see points, roulette wont be so hard on priority
   # result = - points
   # result = - moves - points ** points + math.sqrt(moves) * math.sqrt(points)
   # result = - math.pow(result, 2)
   return result

if __name__ == "__main__":
   mp.set_start_method('spawn', force=True)
   net = SnakeNet()
   net_shape = net.get_model_weight_shapes()
   dimensions = net.total_parameters()

   crossover_operators = [
      xso.gamma_weighted_crossover(tau=100),
      xso.neural_crossover(net_shape),
      # xso.identity_crossover(),
      # xso.neural_layer_crossover(net_shape),
      # xso.average_crossover(ratio=0.9),
      # xso.single_point_crossover(),
      # xso.average_crossover(ratio=0.01),
      # xso.shuffle_crossover(mixing_rate=0.5),
      # xso.shuffle_crossover(mixing_rate=0.5),
   ]

   mutation_operators = [
      mo.gauss_mutate(mu=0, sigma=0.2),
      # mo.identity_mutate(),
      # mo.gauss_rate_mutate(0.01),
      # mo.null_mutate()
      # mo.gauss_mutate(mu=0, sigma=0.2),
      # mo.gauss_mutate(mu=0, sigma=0.2),
      # mo.gauss_mutate(mu=0, sigma=0.1),
      # mo.gauss_mutate(mu=0, sigma=0.1),
      # mo.univariate_mutate(mu=0, sigma=1),
      # mo.spike_mutate(bounds=Bounds(min=-1, max=1)),
      # mo.negate_mutate(),
   ]
   
   best_snake = evolution_optimise(
      target_function,
      dimensions,
      crossover_operators=crossover_operators,
      mutation_operators=mutation_operators,
      population_size=1000,
      generations=100,
      should_load_population=True,
      load_directory='population_2020_11_07', #'population_2020_11_03', # #'big_population_2',
      should_save_population=True,
      save_directory='population_2020_11_07',
      workers=16,
      allowed_seconds= 60 * 60 * 8
   )

   cost, pos = best_snake.cost, best_snake.gene

   print("BEST COST: {}".format(cost))
   net.apply_parameters(pos)
   net.save_weights('./my_model/best_weights.json')

