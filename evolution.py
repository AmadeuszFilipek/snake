import numpy as np
import random as rng
from collections import namedtuple
from multiprocessing import Pool
import itertools as it

Bounds = namedtuple('Bounds', ['min', 'max'])
Bin = namedtuple('Bin', ['min', 'max'])
Individual = namedtuple('Individual', ['gene', 'cost'])

MUTATION_PROBABILITY = 0.2
PARENT_RATE = 0.5
MUTATION_DEVIATION = 0.01

def generate_individual(dimensions, bounds):
   span = bounds.max - bounds.min
   random_table = span * np.random.rand(dimensions) + bounds.min
   return Individual(gene=random_table, cost=0)

def gene_iterator(population):
   for p in population:
      yield p.gene

def cost_iterator(population):
   for p in population:
      yield p.cost

def construct_bins(population):
   cost_sum = sum(cost_iterator(population))
   bin_points = [0] + [abs(i.cost / cost_sum) for i in population]
   
   bins = []
   for i in range(bin_points - 1):
      single_bin = Bin(min=bin_points[i], max=bin_points[i + 1])
      bins.append(single_bin)

   return bins

def select_mating_pool(population, parents_pool_size):
   ''' implementation allows same parent multiple times '''
   # THIS IS FINE
   parents = []

   bins = construct_bins(population)

   for _ in range(parents_pool_size):
      random = rng.random()
      for b, individual in zip(bins, population):
         if random > b.min and random < b.max:
            parents.append(individual)
            break
      
   return parents

def gamma_weighted_crossover(father, mother):
   ''' gamma parameter is randomly generated (0, 1) for each genome '''
   boy_gene = []
   girl_gene = []

   for f_genome, m_genome in zip(father.gene, mother.gene):

      gamma = rng.random()
      boy_genome  = 0.5 * ((1 + gamma) * f_genome + (1 - gamma) * m_genome)
      girl_genome = 0.5 * ((1 - gamma) * f_genome + (1 + gamma) * m_genome)

      boy_gene.append(boy_genome)
      girl_gene.append(girl_genome)
   
   boy = Individual(gene=boy_gene, cost=0)
   girl = Individual(gene=girl_gene, cost=0)

   return boy, girl

def crossover(parents, offspring_size):
   if offspring_size % 2 == 1:
      raise ValueError("Requested offspring size not even.")
   
   children = []
   
   for _ in range(offspring_size / 2):
      father, mother = rng.sample(parents, k=2) 
      
      boy, girl = gamma_weighted_crossover(father, mother)
      children.append(boy)
      children.append(girl)

   return children

def evaluate_fitness(population, workers=1):
   
   genes = gene_iterator(population)
   if workers > 1:
      pool = Pool(processes=3)
      cost = pool.map(target, genes)
   else:
      cost = [target(g) for g in genes]

   # update cost for each specimen
   for i in range(len(population)):
      population[i].cost = cost[i]

def mutate(population, mutated_pool_size):
   ''' mutate whole population by 10% of genome or mutate 10% of population by whole genome ?!?!''' 
   group_to_be_mutated = rng.sample(population, k=mutated_pool_size)
   
   for mutant in group_to_be_mutated:
      for gene in mutant.gene:
         mutagen = rng.normalvariate(mu=0, sigma=MUTATION_DEVIATION)
   
      

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

   if population_size % 2 == 1:
      raise ValueError("Current implementation requires even number of population size")
   
   parent_pool_size = int(population_size * PARENT_RATE / 2) * 2
   offspring_size = population_size - parent_pool_size
   mutated_pool_size = int(population_size * MUTATION_PROBABILITY)

   # inicialize population
   if load_population:
      population = load_population(load_directory)
   else:
      population = [generate_individual(dimensions, bounds) for _ in range(population_size)]

   best_individual = population[0]

   # main generation loop
   for gen in range(generations):

      # evaluate fitness
      evaluate_fitness(population, workers=workers)
      
      # display the results
      # save the population
      # check finish conditions
      # check timer conditions
      
      # continue
   
      parents = select_mating_pool(population, parent_pool_size)

      children = crossover(parents, offspring_size)
      population = parents + children
      
      mutate(population, mutated_pool_size)

   return best_individual