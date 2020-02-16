import numpy as np
import random as rng
from collections import namedtuple
from multiprocessing import Pool
import itertools as it
import os
import glob
import json
import time
import code

Bounds = namedtuple('Bounds', ['min', 'max'])
Bin = namedtuple('Bin', ['min', 'max'])
Individual = namedtuple('Individual', ['gene', 'cost'])

PARENT_RATE = 0.4
MUTATION_PROBABILITY = 0.2
MUTATION_DEVIATION = 0.4

def generate_individual(dimensions, bounds):
   if bounds.max < bounds.min:
      raise ValueError("Invalid bounds: {}".format(bounds))
   span = bounds.max - bounds.min
   random_table = span * np.random.rand(dimensions) + bounds.min
   return Individual(gene=random_table.tolist(), cost=0)

def gene_iterator(population):
   for p in population:
      yield p.gene

def cost_iterator(population):
   for p in population:
      yield p.cost

def construct_bins(population):
   cost_sum = sum(cost_iterator(population))
   # no weights, uniform probability
   if cost_sum == 0:
      bin_points = [1 / len(population) for i in population]
   else:
      bin_points = [abs(i.cost / cost_sum) for i in population]
   
   bins = [Bin(min=0, max=bin_points[0])]
   for i in range(1, len(bin_points)):
      min_point = bins[i - 1].max
      max_point = min_point + bin_points[i]
      single_bin = Bin(min=min_point, max=max_point)
      bins.append(single_bin)

   return bins

def number_in_bin(n, b):
   return (n > b.min) and (n < b.max)

def select_mating_pool(population, parents_pool_size):
   ''' implementation allows same parent multiple times '''
   parents = []
   bins = construct_bins(population)

   for _ in range(parents_pool_size):
      random = rng.random()
      for b, individual in zip(bins, population):
         if number_in_bin(random, b): 
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
   
   for _ in range(offspring_size // 2):
      father, mother = rng.sample(parents, k=2) 
      
      boy, girl = gamma_weighted_crossover(father, mother)
      children.append(boy)
      children.append(girl)

   return children

def evaluate_fitness(target, population, workers=1):
   
   updated_population = []

   genes = gene_iterator(population)
   if workers > 1:
      with Pool(processes=workers) as pool:
         cost = pool.map(target, genes)
   else:
      cost = [target(g) for g in genes]

   # update cost for each specimen
   for i, p in enumerate(population):
      new_specimen = Individual(gene=p.gene, cost=cost[i])
      updated_population.append(new_specimen)

   return updated_population

def mutate(population):

   for mutant in population:
      gene_length = len(mutant.gene)
      expected_number_of_mutations = int(gene_length * MUTATION_PROBABILITY)
      genome_ids_to_mutate = rng.sample(range(gene_length), k=expected_number_of_mutations)
      
      for genome_id in genome_ids_to_mutate:
         mutagen = rng.normalvariate(mu=0, sigma=MUTATION_DEVIATION)
         mutant.gene[genome_id] += mutagen   

def reconstruct_specimen(data):
   gene = data[0]
   cost = data[1]
   specimen = Individual(gene=gene, cost=cost)
   return specimen

def load_population(load_directory):
   if not os.path.isdir(load_directory):
      raise ValueError('Is not a directory: ' + load_directory)
   
   json_file_paths = glob.glob(load_directory + '/*.json')
   
   population = []
   for file_path in json_file_paths:
      with open(file_path, 'r') as file:
         data = json.load(file)
      
      specimen = reconstruct_specimen(data)
      population.append(specimen)
   
   return population

def save_population(population, directory):
   if not os.path.isdir(directory):
      os.makedirs(directory)

   for i, specimen in enumerate(population):
      name = 'snake_{}.json'.format(i)
      with open(directory + '/' + name, 'w') as file:
         serialized_specimen = json.dump(specimen, file)

def evolution_optimise(
      target,
      dimensions,
      bounds=Bounds(min=-1, max=1),
      population_size=10,
      generations=10,
      should_load_population=False,
      load_directory=None,
      workers=1,
      display=True,
      allowed_seconds=None,
      should_save_population=True,
      save_directory=None
   ):

   if population_size % 2 == 1:
      raise ValueError("Current implementation requires even number of population size")
   
   clock_start = time.time()
   parent_pool_size = int(population_size * PARENT_RATE / 2) * 2
   offspring_size = population_size - parent_pool_size

   # inicialize population
   if should_load_population:
      population = load_population(load_directory)
   else:
      population = [generate_individual(dimensions, bounds) for _ in range(population_size)]

   best_individual = population[0]

   # main generation loop
   for gen in range(generations):

      # evaluate fitness
      population = evaluate_fitness(target, population, workers=workers)

      # find the best one
      for p in population:
         if p.cost < best_individual.cost:
            best_gene = p.gene.copy()
            best_individual = Individual(gene=best_gene, cost=p.cost)
      
      # display the results
      if display:
         print("Generation {}/{}: best cost: {:.2e}".format(gen, generations, best_individual.cost))

      # save the population
      if should_save_population:
         save_population(population, save_directory)

      # check timer conditions
      clock = time.time()
      elapsed_seconds = clock - clock_start 
      if (allowed_seconds is not None) and elapsed_seconds > allowed_seconds:
         if display:
            print("Evolution loop ran out of time. Finishing optimisation. Total runtime: {}".format(elapsed_seconds))
         break

      # continue iteration
      parents = select_mating_pool(population, parent_pool_size)

      children = crossover(parents, offspring_size)
      population = parents + children
      mutate(population)

   return best_individual

