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

from neural_net import alternate

Bounds = namedtuple('Bounds', ['min', 'max'])
Bin = namedtuple('Bin', ['min', 'max'])
Individual = namedtuple('Individual', ['gene', 'fitness', 'score'])

PARENT_RATE = 0.33
MUTATION_PROBABILITY = 0.05

def generate_individual(shapes, bounds):
   if bounds.max < bounds.min:
      raise ValueError("Invalid bounds: {}".format(bounds))
   
   gene = []
   for shape in shapes:
      span = bounds.max - bounds.min
      random_table = span * np.random.random(shape) + bounds.min
      gene.append(random_table)

   return Individual(gene=gene, fitness=0, score=0)

def gene_iterator(population):
   for p in population:
      yield p.gene

def fitness_iterator(population):
   for p in population:
      yield p.fitness

def roulette_choose(population):
   wheel = sum(fitness_iterator(population))
   shot = rng.uniform(0, wheel)
   aggregate = 0
   for specimen in population:
      aggregate += specimen.fitness
      if aggregate > shot:
         return specimen

def select_mating_pool(population, parents_pool_size):
   parents = []
   candidates = population.copy()
   candidates.sort(key=lambda x: x.fitness, reverse=True)
   parents = candidates[:parents_pool_size]

   return parents

def crossover(parents, offspring_size, crossover_operators):
   if offspring_size % 2 == 1:
      raise ValueError("Requested offspring size not even.")

   children = []
   for _ in range(offspring_size // 2):

      father = roulette_choose(parents)
      mother = roulette_choose(parents)

      boy_gene = []
      girl_gene = []

      for (f_weight, f_bias), (m_weight, m_bias) in zip(alternate(father.gene), alternate(mother.gene)):
         crossover_operator = rng.choice(crossover_operators)

         boy_weight, girl_weight = crossover_operator(f_weight, m_weight)
         boy_bias, girl_bias = crossover_operator(f_bias, m_bias)

         boy_gene.append(boy_weight)
         boy_gene.append(boy_bias)
         girl_gene.append(girl_weight)
         girl_gene.append(girl_bias)
      
      boy = Individual(gene=boy_gene, fitness=0, score=0)
      girl = Individual(gene=girl_gene, fitness=0, score=0)

      children.append(boy)
      children.append(girl)

   return children

def evaluate_fitness(target, population, workers):
   evaluated_population = []
   genes = gene_iterator(population)

   if workers > 1:
      with Pool(processes=workers,  maxtasksperchild=50) as pool:
         results = pool.map(target, genes)
   else:
      results = [target(g) for g in genes]

   # build new specimens with their fitness
   for (fitness, points), specimen in zip(results, population):
      new_specimen = Individual(gene=specimen.gene, fitness=fitness, score=points)
      evaluated_population.append(new_specimen)

   return evaluated_population

def apply_constraints(population, bounds):
   clipped_population = []

   for gene in gene_iterator(population):
      clipped_gene = [np.clip(g, bounds.min, bounds.max) for g in gene]
      clipped_specimen = Individual(gene=clipped_gene, fitness=0, score=0)
      clipped_population.append(clipped_specimen)
   
   return clipped_population

def mutate(population, mutation_probability, mutation_operators):
   mutated_population = []

   for specimen in population:

      mutated_gene = []

      for weight, bias in alternate(specimen.gene):
         mutated_weight, mutated_bias = weight.copy(), bias.copy()
         weight_mutation_table = np.random.random(weight.shape) < mutation_probability
         bias_mutation_table = np.random.random(bias.shape) < mutation_probability

         mutation_operator = rng.choice(mutation_operators)
         mutated_weight[weight_mutation_table] = mutation_operator(weight[weight_mutation_table])
         mutated_bias[bias_mutation_table] = mutation_operator(bias[bias_mutation_table])

         mutated_gene.append(mutated_weight)
         mutated_gene.append(mutated_bias)

      mutant = Individual(gene=mutated_gene, fitness=0, score=0)
      mutated_population.append(mutant)
   
   return mutated_population

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
         gene = []
         for weight, bias in alternate(data):
            gene.append(np.array(weight))
            gene.append(np.array(bias))
      specimen = Individual(gene=data, fitness=0, score=0)
      population.append(specimen)
   
   return population

def save_population(population, directory):
   if not os.path.isdir(directory):
      os.makedirs(directory)

   for i, specimen in enumerate(population):
      name = 'snake_{}.json'.format(i)
      data = []
      for weight, bias in alternate(specimen.gene):
         data.append(weight.tolist())
         data.append(bias.tolist())

      with open(directory + '/' + name, 'w') as file:
         json.dump(data, file)

def log_results(message):
   try:
      with open("fitness_data.csv", "a+") as file:
         file.write('{}\n'.format(message))
   except IOError:
      print("Unable to log data to file")

def evolution_optimise(
      target,
      shapes,
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
      population = [generate_individual(shapes, bounds) for _ in range(population_size)]

   best_individual = Individual(gene=np.array([]), fitness=0, score=0)
   generation_best_individual = Individual(gene=np.array([]), fitness=0, score=0)

   # main generation loop
   for gen in range(generations):
      try:
         # evaluate fitness
         population = evaluate_fitness(target, population, workers)

         # find the best one
         generation_avg_result = 0
         for p in population:
            generation_avg_result += p.fitness
            if p.fitness > best_individual.fitness:
               best_individual = Individual(gene=p.gene.copy(), fitness=p.fitness, score=p.score)
         generation_avg_result = generation_avg_result / population_size

         # compare this generation to previous
         new_gen_best = max(population, key=lambda p: p.fitness)
         generation_best_individual = new_gen_best

         # display the results
         if display:
            print("Generation {}/{}: best score: {:d} avg fitness: {:.2f} gen best: {:.2f} global best fitness: {:.2f}".format(
               gen,
               generations,
               generation_best_individual.score,
               generation_avg_result,
               generation_best_individual.fitness, 
               best_individual.fitness
            ))

         # log the results
         # log_results("{}, {}, {}, {}".format(gen, generation_best_individual.score, generation_avg_result, generation_best_individual.fitness))

         # check timer conditions
         clock = time.time()
         elapsed_seconds = clock - clock_start
         if (allowed_seconds is not None) and elapsed_seconds > allowed_seconds:
            if display:
               print("Evolution loop ran out of time. Finishing optimisation. Total runtime: {}".format(elapsed_seconds))
            break

         # construct new population
         parents = select_mating_pool(population, parent_pool_size)
         children = crossover(parents, offspring_size, crossover_operators)
         children = mutate(children, MUTATION_PROBABILITY, mutation_operators)
         children = apply_constraints(children, bounds)
         population = children + parents
         rng.shuffle(population)

         # save the population
         if should_save_population:
            save_population(children, save_directory)


      except KeyboardInterrupt:
         return best_individual

   return best_individual

