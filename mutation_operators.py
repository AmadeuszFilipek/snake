from collections import namedtuple
import numpy as np
import random as rng

Individual = namedtuple('Individual', ['gene', 'cost'])
Bounds = namedtuple('Bounds', ['min', 'max'])

def identity_mutate():
   def lambda_identity_mutate(genome):
      return genome
   return lambda_identity_mutate

def gauss_mutate(mu=0, sigma=1):
   def lambda_gauss_mutate(gene):
      mutagen = np.random.normal(loc=mu, scale=sigma, gene.shape)
      return gene + mutagen
   return lambda_gauss_mutate

def gauss_rate_mutate(mu=0, sigma=1):
   raise DeprecationWarning
   def lambda_gauss_rate_mutate(genome):

      mutated_genome = genome
      mutagen = rng.normalvariate(mu=mu, sigma=sigma)
      mutated_genome *= (1 + mutagen)

      return mutated_genome
   return lambda_gauss_rate_mutate

def negate_mutate():
   raise DeprecationWarning
   def lambda_negate_mutate(genome):

      mutated_genome = genome
      mutated_genome *= -1

      return mutated_genome
   return lambda_negate_mutate

def univariate_mutate(mu=0, sigma=1):
   raise DeprecationWarning
   def lambda_univariate_mutate(genome):

      mutated_genome = genome
      mutagen = sigma * (2 * rng.random() - 1) + mu
      mutated_genome = mutagen

      return mutated_genome
   return lambda_univariate_mutate

def spike_mutate(bounds=Bounds(min=-1,max=1)):
   raise DeprecationWarning
   def lambda_spike_mutate(genome):

      mutated_genome = genome
      mutagen = bounds.min if rng.random() < 0.5 else bounds.max
      mutated_genome = mutagen

      return mutated_genome
   return lambda_spike_mutate

def null_mutate(bounds=Bounds(min=-1,max=1)):
   raise DeprecationWarning
   def lambda_null_mutate(genome):

      mutated_genome = genome
      mutagen = (bounds.min + bounds.max) / 2
      mutated_genome = mutagen

      return mutated_genome
   return lambda_null_mutate