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

PARENT_RATE = 0.3
MUTATION_PROBABILITY = 0.2
MUTATION_DEVIATION = 0.1
BINARY_RESOLUTION = 5

FLIP_BIT = {'0': '1', '1': '0'}

def value_to_binary(genome, bounds):
   binary_integer = 0
   for i in range(BINARY_RESOLUTION - 1, 0 - 1, -1):
      value = 2 ** i
      number_to_check = integer_to_value(binary_integer + value, bounds)
      if number_to_check < genome:
         binary_integer += value
      
   binary_string = bin(binary_integer)
   binary_string = binary_string[2:].zfill(BINARY_RESOLUTION)
   return binary_string

def integer_to_value(binary_integer, bounds):
   span = bounds.max - bounds.min
   value = bounds.min + binary_integer * span / (2 ** BINARY_RESOLUTION - 1)
   return value

def binary_to_value(binary_genome, bounds):
   binary_integer = int(binary_genome, 2)
   value = integer_to_value(binary_integer, bounds)

   return value

def generate_individual(dimensions, bounds, binary=True):
   if bounds.max < bounds.min:
      raise ValueError("Invalid bounds: {}".format(bounds))
   
   if binary:
      random_table = np.random.rand(dimensions) * (2 ** BINARY_RESOLUTION - 1)
      random_table = np.around(random_table)
      random_table = list(map(lambda x: integer_to_value(x, bounds), random_table))
   else:
      span = bounds.max - bounds.min
      random_table = span * np.random.rand(dimensions) + bounds.min
      random_table = random_table.tolist()

   return Individual(gene=random_table, cost=0)

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
   parents = []
   candidates = population.copy()

   for _ in range(parents_pool_size):
      bins = construct_bins(candidates)

      random = rng.random()
      for i in range(len(candidates)):
         if number_in_bin(random, bins[i]):
            selected_individual_id = i
            break

      parents.append(candidates[selected_individual_id])
      candidates.pop(selected_individual_id)
      
   return parents

def gamma_weighted_crossover(father, mother):
   ''' gamma parameter is randomly generated (0, 1) for each genome '''
   boy_gene = []
   girl_gene = []
   tau = 5

   for f_genome, m_genome in zip(father.gene, mother.gene):

      gamma = rng.random()
      if gamma > 0.5:
         gamma = gamma ** (1 / tau)
      else:
         gamma = gamma ** tau

      boy_genome  = 0.5 * ((1 + gamma) * f_genome + (1 - gamma) * m_genome)
      girl_genome = 0.5 * ((1 - gamma) * f_genome + (1 + gamma) * m_genome)

      boy_gene.append(boy_genome)
      girl_gene.append(girl_genome)
   
   boy = Individual(gene=boy_gene, cost=0)
   girl = Individual(gene=girl_gene, cost=0)

   return boy, girl

def single_point_binary_crossover(father, mother, bounds):
   boy_gene = []
   girl_gene = []

   for f_genome, m_genome in zip(father.gene, mother.gene):

      binary_father_genome = value_to_binary(f_genome, bounds)
      binary_mother_genome = value_to_binary(m_genome, bounds)

      point = int(rng.random() * BINARY_RESOLUTION)

      binary_boy_genome  = binary_father_genome[point:] + binary_mother_genome[:point]
      binary_girl_genome = binary_father_genome[:point] + binary_mother_genome[point:]
      
      boy_genome = binary_to_value(binary_boy_genome, bounds)
      girl_genome = binary_to_value(binary_girl_genome, bounds)

      boy_gene.append(boy_genome)
      girl_gene.append(girl_genome)
   
   boy = Individual(gene=boy_gene, cost=0)
   girl = Individual(gene=girl_gene, cost=0)

   return boy, girl

def crossover(parents, offspring_size, bounds, binary=True):
   if offspring_size % 2 == 1:
      raise ValueError("Requested offspring size not even.")
   
   children = []
   
   for _ in range(offspring_size // 2):
      father, mother = rng.sample(parents, k=2) 
      
      if binary:
         boy, girl = single_point_binary_crossover(father, mother, bounds)
      else:
         boy, girl = gamma_weighted_crossover(father, mother)

      children.append(boy)
      children.append(girl)

   return children

def evaluate_fitness(target, population, workers=1):
   
   updated_population = []

   genes = gene_iterator(population)
   if workers > 1:
      with Pool(processes=workers) as pool:
         results = pool.map(target, genes)
   else:
      results = [target(g) for g in genes]

   # build new specimens with their cost and changed genes
   for cost, parameters in results:
      new_specimen = Individual(gene=parameters, cost=cost)
      updated_population.append(new_specimen)

   return updated_population

def mutate(population):

   for mutant in population:
      gene_length = len(mutant.gene)
      
      for genome_id in range(gene_length):
         is_mutated = rng.random() < MUTATION_PROBABILITY
         if (is_mutated):
            mutagen = rng.normalvariate(mu=0, sigma=MUTATION_DEVIATION)
            mutant.gene[genome_id] += mutagen

def binary_mutate(population, bounds):

   for mutant in population:
      gene_length = len(mutant.gene)

      for genome_id in range(gene_length):
         is_mutated = rng.random() < MUTATION_PROBABILITY
         if (is_mutated):
            genome = mutant.gene[genome_id]
            binary_genome = list(value_to_binary(genome, bounds))

            bit_to_mutate = int(rng.random() * BINARY_RESOLUTION)
            old_bit = binary_genome[bit_to_mutate]
            new_bit = FLIP_BIT[old_bit]
            binary_genome[bit_to_mutate] = new_bit
            new_genome = binary_to_value(''.join(binary_genome), bounds)

            mutant.gene[genome_id] = new_genome
         
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
      save_directory=None,
      binary=False,
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
      population = [generate_individual(dimensions, bounds, binary) for _ in range(population_size)]

   best_individual = population[0]
   children = population
   parents = []

   # main generation loop
   for gen in range(generations):

      # evaluate fitness
      children = evaluate_fitness(target, children, workers=workers)
      population = children + parents

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
      parents = select_mating_pool(population, parent_pool_size - 1)
      parents.append(best_individual)

      children = crossover(parents, offspring_size, bounds, binary)
      
      binary_mutate(children, bounds) if binary else mutate(children)

      population = parents + children

   return best_individual

