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
import math

import neural_net as net

Bounds = namedtuple('Bounds', ['min', 'max'])
Bin = namedtuple('Bin', ['min', 'max'])
Individual = namedtuple('Individual', ['gene', 'cost'])

PARENT_RATE = 0.05
SPECIMEN_MUTATES_PROBABILITY = 0.1 # single_mutation
SPECIMEN_CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.001 # 0.001 0.005 tested

# MUTATIONS_PER_SPECIMEN = 10
# BINARY_RESOLUTION = 5

# FLIP_BIT = {'0': '1', '1': '0'}

# def value_to_binary(genome, bounds):
#    binary_integer = 0
#    for i in range(BINARY_RESOLUTION - 1, 0 - 1, -1):
#       value = 2 ** i
#       number_to_check = integer_to_value(binary_integer + value, bounds)
#       if number_to_check < genome:
#          binary_integer += value
      
#    binary_string = bin(binary_integer)
#    binary_string = binary_string[2:].zfill(BINARY_RESOLUTION)
#    return binary_string

# def integer_to_value(binary_integer, bounds):
#    span = bounds.max - bounds.min
#    value = bounds.min + binary_integer * span / (2 ** BINARY_RESOLUTION - 1)
#    return value

# def binary_to_value(binary_genome, bounds):
#    binary_integer = int(binary_genome, 2)
#    value = integer_to_value(binary_integer, bounds)

#    return value

def generate_individual(dimensions, bounds, binary=False):
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

# def construct_bins(population):
#    cost_sum = sum(cost_iterator(population))
#    # no weights, uniform probability
#    if cost_sum == 0:
#       bin_points = [1 / len(population) for i in population]
#    else:
#       bin_points = [abs(i.cost / cost_sum) for i in population]
   
#    bins = [Bin(min=0, max=bin_points[0])]
#    for i in range(1, len(bin_points)):
#       min_point = bins[i - 1].max
#       max_point = min_point + bin_points[i]
#       single_bin = Bin(min=min_point, max=max_point)
#       bins.append(single_bin)

#    return bins

# def number_in_bin(n, b):
#    return (n > b.min) and (n < b.max)

def roulette_choose(population):
   wheel = sum(cost_iterator(population))
   shot = rng.uniform(wheel, 0)
   aggregate = 0
   for specimen in population:
      aggregate += specimen.cost
      if shot < aggregate: 
      return specimen

def select_mating_pool(population, parents_pool_size):
   parents = []
   candidates = population.copy()
   candidates.sort(key=lambda x: x.cost)
   parents = candidates[:parents_pool_size]

   return parents

# def single_point_binary_crossover(father, mother, bounds):
#    ''' deprecated and unused '''
#    raise DeprecationWarning

#    boy_gene = []
#    girl_gene = []

#    for f_genome, m_genome in zip(father.gene, mother.gene):

#       binary_father_genome = value_to_binary(f_genome, bounds)
#       binary_mother_genome = value_to_binary(m_genome, bounds)

#       point = int(rng.random() * BINARY_RESOLUTION)

#       binary_boy_genome  = binary_father_genome[point:] + binary_mother_genome[:point]
#       binary_girl_genome = binary_father_genome[:point] + binary_mother_genome[point:]
      
#       boy_genome = binary_to_value(binary_boy_genome, bounds)
#       girl_genome = binary_to_value(binary_girl_genome, bounds)

#       boy_gene.append(boy_genome)
#       girl_gene.append(girl_genome)
   
#    boy = Individual(gene=boy_gene, cost=0)
#    girl = Individual(gene=girl_gene, cost=0)

#    return boy, girl

def crossover(parents, offspring_size, crossover_operators, binary=True):
   if offspring_size % 2 == 1:
      raise ValueError("Requested offspring size not even.")

   children = []
   for _ in range(offspring_size // 2):

      father = roulette_choose(parents)
      mother = roulette_choose(parents)

   for weight and bias of each ...:
      # implement crossover per each weight and bias of parents
      # yeah ... but how, i need shapes to reconstruct (but that would be a waste of time)
      # better to hold the genes as the nested array

      crossover_operator = rng.choice(crossover_operators)
      boy, girl = crossover_operator(father, mother)

      children.append(boy)
      children.append(girl)

   return children

def evaluate_fitness(target, population, workers):
   
   updated_population = []

   genes = gene_iterator(population)

   if workers > 1:
      with Pool(processes=workers,  maxtasksperchild=50) as pool:
         results = pool.map(target, genes)
   else:
      results = [target(g) for g in genes]

   # build new specimens with their cost and changed genes
   for cost, specimen in zip(results, population):
      new_specimen = Individual(gene=specimen.gene, cost=cost)
      updated_population.append(new_specimen)

   return updated_population

def clip(genome, bounds):
   raise DeprecationWarning
   # AF: update implementation
   if genome > bounds.max:
      return bounds.max
   elif genome < bounds.min:
      return bounds.min
   else:
      return genome

def apply_constraints(population, bounds):
   # AF: update this ?
   clipped_population = []

   for gene in gene_iterator(population):
      clipped_gene = [clip(g, bounds) for g in gene]
      clipped_specimen = Individual(gene=clipped_gene, cost=np.inf)
      clipped_population.append(clipped_specimen)
   
   return clipped_population

def single_mutate(population, bounds, mutation_probability, mutation_operators):
   # early dev
   mutated_population = []

   for specimen in population:

      specimen_mutates = rng.random() < SPECIMEN_MUTATES_PROBABILITY

      if (specimen_mutates):
         genome_length = len(specimen.gene)
         mutated_genome_id = rng.randint(0, genome_length - 1)

         mutated_gene = specimen.gene.copy()
         mutation_operator = rng.choice(mutation_operators)
         mutated_gene[mutated_genome_id] = mutation_operator(mutated_gene[mutated_genome_id]) 
      else:
         mutated_gene = specimen.gene

      mutant = Individual(gene=mutated_gene, cost=np.inf)
      mutated_population.append(mutant)
   
   return mutated_population

def mutate(population, bounds, mutation_probability, mutation_operators):
   mutated_population = []

   for specimen in population:

      # mutations = 0
      mutated_gene = []

      specimen_mutates = rng.random() < SPECIMEN_MUTATES_PROBABILITY

      if (specimen_mutates):
         for genome in specimen.gene:
            mutated_genome = genome
            is_mutated = rng.random() < mutation_probability
            if (is_mutated):# and mutations < MUTATIONS_PER_SPECIMEN):
               # mutations += 1
               mutation_operator = rng.choice(mutation_operators)
               mutated_genome = mutation_operator(mutated_genome)
            mutated_gene.append(mutated_genome)
      else:
         mutated_gene = specimen.gene
      
      mutant = Individual(gene=mutated_gene, cost=np.inf)
      mutated_population.append(mutant)
   
   return mutated_population

# def binary_mutate(population, bounds):
#    raise DeprecationWarning
#    for mutant in population:
#       gene_length = len(mutant.gene)

#       for genome_id in range(gene_length):
#          is_mutated = rng.random() < MUTATION_PROBABILITY
#          if (is_mutated):
#             genome = mutant.gene[genome_id]
#             binary_genome = list(value_to_binary(genome, bounds))

#             bit_to_mutate = int(rng.random() * BINARY_RESOLUTION)
#             old_bit = binary_genome[bit_to_mutate]
#             new_bit = FLIP_BIT[old_bit]
#             binary_genome[bit_to_mutate] = new_bit
#             new_genome = binary_to_value(''.join(binary_genome), bounds)

#             mutant.gene[genome_id] = new_genome

def reconstruct_specimen(data, load_cost=True):
   gene = data[0]
   if load_cost: 
      cost = data[1]
   else:
      cost = 0
   specimen = Individual(gene=gene, cost=cost)
   return specimen

def load_population(load_directory):
   if not os.path.isdir(load_directory):
      raise ValueError('Is not a directory: ' + load_directory)
   
   json_file_paths = glob.glob(load_directory + '/*.json')
   
   population = []
   for file_path in json_file_paths:
      with open(file_path, 'r') as file:
         try:
            data = json.load(file)
         except json.JSONDecodeError:
            continue

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

# def log_results(population, generation):
#    try:
#       with open("fitness_data.csv", "a+") as file:
#          for i, p in enumerate(population):
#             file.write('{},{},{}\n'.format(generation, i, p.cost))
#    except IOError:
#       print("Unable to log data to file")

def evolution_optimise(
      target,
      dimensions,
      crossover_operators,
      mutation_operators,
      bounds=Bounds(min=-1, max=1),
      population_size=10,
      generations=10,
      workers=1,
      display=True,
      should_load_population=False,
      should_save_population=False,
      save_directory=None,
      load_directory=None,
      allowed_seconds=None,
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
      # population = [generate_individual(dimensions, Bounds(min=0, max=0)) for _ in range(population_size)]
      population = [generate_individual(dimensions, bounds) for _ in range(population_size)]

   best_individual = Individual(gene=[], cost=0)
   generation_best_individual = Individual(gene=[], cost=0)
   parents = []
   # progres_stagnation = 0 #AF: wtf is this

   # main generation loop
   for gen in range(generations):
      try:
         # evaluate fitness
         population = evaluate_fitness(target, population, workers)

         # find the best one
         generation_avg_result = 0
         for p in population:
            generation_avg_result += p.cost
            if p.cost < best_individual.cost:
               best_individual = Individual(gene=p.gene.copy(), cost=p.cost)
         generation_avg_result = generation_avg_result / population_size

         # compare this generation to previous
         new_gen_best = min(population, key=lambda p: p.cost)
         was_there_any_progress = False
         if new_gen_best.cost < generation_best_individual.cost:
            was_there_any_progress = True
         generation_best_individual = new_gen_best

         # display the results
         if display:
            print("Generation {}/{}:  avg cost: {:.2e} gen best: {:.2e} global best cost: {:.2e}".format(
               gen, generations, generation_avg_result, generation_best_individual.cost, best_individual.cost))

         # log the results
         # log_results(population, gen)

         # check timer conditions
         clock = time.time()
         elapsed_seconds = clock - clock_start
         if (allowed_seconds is not None) and elapsed_seconds > allowed_seconds:
            if display:
               print("Evolution loop ran out of time. Finishing optimisation. Total runtime: {}".format(elapsed_seconds))
            break

         # construct new population
         parents = select_mating_pool(population, parent_pool_size - 1)
         rng.shuffle(parents)

         children = crossover(parents, population_size, crossover_operators)
         children = single_mutate(children, bounds, MUTATION_PROBABILITY, mutation_operators)
         # children = mutate(children, bounds, MUTATION_PROBABILITY, mutation_operators)
         children = apply_constraints(children, bounds)
         
         population = children + parents


         # save the population
         if should_save_population:
            save_population(children, save_directory)


      except KeyboardInterrupt:
         return best_individual

   return best_individual

