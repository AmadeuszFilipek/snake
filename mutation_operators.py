from collections import namedtuple
import numpy as np
import random as rng

Individual = namedtuple('Individual', ['gene', 'cost'])
Bounds = namedtuple('Bounds', ['min', 'max'])

# shall be low so that there is movement but not much disturbance
MUTATION_PROBABILITY = 0.05

def gauss_mutate(mu=0, sigma=1):
   def lambda_gauss_mutate(specimen):
      mutated_gene = []

      for genome in specimen.gene:
         mutated_genome = genome
         is_mutated = rng.random() < MUTATION_PROBABILITY
         if (is_mutated):
            mutagen = rng.normalvariate(mu=mu, sigma=sigma)
            mutated_genome += mutagen
         mutated_gene.append(mutated_genome)

      return Individual(gene=mutated_gene, cost=np.inf)
   return lambda_gauss_mutate

def negate_mutate():
   def lambda_negate_mutate(specimen):
      mutated_gene = []

      for genome in specimen.gene:
         mutated_genome = genome
         is_mutated = rng.random() < MUTATION_PROBABILITY
         if (is_mutated):
            mutated_genome *= -1
         mutated_gene.append(mutated_genome)

      return Individual(gene=mutated_gene, cost=np.inf)
   return lambda_negate_mutate

def univariate_mutate(mu=0, sigma=1):
   def lambda_univariate_mutate(specimen):
      mutated_gene = []

      for genome in specimen.gene:
         mutated_genome = genome
         is_mutated = rng.random() < MUTATION_PROBABILITY
         if (is_mutated):
            mutagen = sigma * (2 * rng.random() - 1) + mu
            mutated_genome += mutagen
         mutated_gene.append(mutated_genome)

      return Individual(gene=mutated_gene, cost=np.inf)
   return lambda_univariate_mutate

def spike_mutate(bounds=Bounds(min=-1,max=1)):
   def lambda_spike_mutate(specimen):
      mutated_gene = []

      for genome in specimen.gene:
         mutated_genome = genome
         is_mutated = rng.random() < MUTATION_PROBABILITY
         if (is_mutated):
            mutagen = bounds.min if rng.random() < 0.5 else bounds.max
            mutated_genome = mutagen
         mutated_gene.append(mutated_genome)

      return Individual(gene=mutated_gene, cost=np.inf)
   return lambda_spike_mutate

def null_mutate(bounds=Bounds(min=-1,max=1)):
   def lambda_null_mutate(specimen):
      mutated_gene = []

      for genome in specimen.gene:
         mutated_genome = genome
         is_mutated = rng.random() < MUTATION_PROBABILITY
         if (is_mutated):
            mutagen = (bounds.min + bounds.max) / 2
            mutated_genome = mutagen
         mutated_gene.append(mutated_genome)

      return Individual(gene=mutated_gene, cost=np.inf)
   return lambda_null_mutate