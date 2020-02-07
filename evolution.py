import numpy as np
import random as rng
from collections import namedtuple
from multiprocessing import Pool
import itertools as it

Bounds = namedtuple('Bounds', ['min', 'max'])
Individual = namedtuple('Individual', ['gene', 'cost'])

MUTATION_PROBABILITY = 0.2
PARENT_RATE = 0.5

def generate_individual(dimensions, bounds):
   span = bounds.max - bounds.min
   random_table = span * np.random.rand(dimensions) + bounds.min
   return Individual(gene=random_table, cost=np.inf)

def gene_iterator(population):
   for p in population:
      yield p.gene

def cost_iterator(population):
   for p in population:
      yield p.cost

def construct_bins(population):
   cost_sum = sum(cost_iterator(population))
   bin_points = [0] + [i.cost / cost_sum for i in population]
   
   bins = []
   for i in range(bin_points - 1):
      single_bin = (bins[i], bins[i + 1])
      bins.append(single_bin)

   return bins

def select_mating_pool(population):
   ''' implementation allows same parent multiple times '''
   parent_size = len(population) * PARENT_RATE
   parents = []
   # select one parent by roulette
   # the higher the score, the bigger the chance to get picked
   # apply bin for each individual
   # hit [0, 1] and see which bin did I hit
   bins = construct_bins(population)

   for i in range(parent_size):
      random = rng.random()
      



def evolution_optimise(
   target,
   dimensions,
   bounds=Bounds(min=-1, max=1),
   population_size=10,
   generations=10,
   load_population=False,
   load_directory=None,
   workers=1,
   save_population=True
   ):

   # inicialize population
   if load_population:
      population = load_population(load_directory)
   else:
      population = [generate_individual(dimensions, bounds) for _ in range(population_size)]

   best_individual = population[0]

   # main generation loop
   for gen in range(generations):

      # evaluate fitness
      genes = gene_iterator(population)
      if workers > 1:
         pool = Pool(processes=3)
         cost = pool.map(target, genes)
      else:
         cost = [target(g) for g in genes]
      
      # update cost for each specimen
      for i in range(population_size):
         population[i].cost = cost[i]

      # update global best solution
      for p in population:
         if p.cost > best_individual.cost:
            best_individual = p
      
      # display the results
      # save the population
      # check finish conditions
      # check timer conditions
      
      # continue

      # select parents for mating
      parents = select_mating_pool(population)
      children = crossover(parents, offspring_size)
      children = mutate(children)

      population = parents + children
   
   return best_individual