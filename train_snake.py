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
   net.set_weights(parameters)

   points, moves, avg_moves = play(
         display=False,
         collision=True,
         moves_to_lose=100,
         net=net
   )

   fit = fitness(points, moves)

   return fit, points

def fitness(points, moves):
   # minus sign for minimization
   result = moves + 2 ** points + (points ** 2.1) * 500 - (((0.25 * moves) ** 1.3) * (points ** 1.2))
   return max(result, 0.1)
   # result = - points * points * math.exp(points) \
   #          - moves + points * math.sqrt(moves)
   # result = - math.exp(points) # lets just see points, roulette wont be so hard on priority
   # result = - points
   # result = - moves - points ** points + math.sqrt(moves) * math.sqrt(points)
   # result = - math.pow(result, 2)

if __name__ == "__main__":
   mp.set_start_method('spawn', force=True)
   net = SnakeNet()
   net_shape = net.get_model_weight_shapes()
   dimensions = net.total_parameters()

   crossover_operators = [
      xso.single_point_crossover(),
      xso.gamma_weighted_crossover(tau=100),
      # xso.identity_crossover()
   ]

   mutation_operators = [
      # mo.identity_mutate()
      mo.gauss_mutate(mu=0, scale=0.2),
   ]
   
   best_snake = evolution_optimise(
      target_function,
      net_shape,
      crossover_operators=crossover_operators,
      mutation_operators=mutation_operators,
      population_size=1500,
      generations=100000,
      should_load_population=False,
      load_directory='',
      should_save_population=False,
      save_directory='',
      workers=15,
      allowed_seconds= 60 * 60 * 1
   )

   fitness, pos = best_snake.fitness, best_snake.gene

   print("BEST COST: {}".format(fitness))
   net.set_weights(pos)
   net.save_weights('./my_model/best_weights.json')

