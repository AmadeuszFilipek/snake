from collections import namedtuple
import numpy as np
import random as rng

Individual = namedtuple('Individual', ['gene', 'cost'])
Bounds = namedtuple('Bounds', ['min', 'max'])

def gamma_weighted_crossover(tau=10):
   ''' gamma parameter is randomly generated (0, 1) for each genome '''

   raise DeprecationWarning("This operator is badly designed")

   def lambda_gamma_weighted_crossover(father, mother):
      boy_gene = []
      girl_gene = []

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

   return lambda_gamma_weighted_crossover

def shuffle_crossover(mixing_rate=0.5):
   ''' each child gets some father and some mother genes '''
   if mixing_rate < 0 or mixing_rate > 1:
      raise ValueError()
   
   def lambda_shuffle_crossover(father, mother):

      boy_gene = []
      girl_gene = []

      for f_genome, m_genome in zip(father.gene, mother.gene):

         gamma = rng.random()
         if gamma > mixing_rate:
            boy_genome  = f_genome
            girl_genome = m_genome
         else:
            boy_genome  = m_genome
            girl_genome = f_genome

         boy_gene.append(boy_genome)
         girl_gene.append(girl_genome)
      
      boy = Individual(gene=boy_gene, cost=np.inf)
      girl = Individual(gene=girl_gene, cost=np.inf)

      return boy, girl
   
   return lambda_shuffle_crossover

def average_crossover(ratio=0.5):
   ''' averages the genes from both parens using ratio '''

   if ratio < 0 or ratio > 1:
      raise ValueError("Ratio shall be value in range [0, 1]")

   def lambda_average_crossover(father, mother):
      boy_gene = []
      girl_gene = []

      for f_genome, m_genome in zip(father.gene, mother.gene):

         boy_genome  = ratio * f_genome + (1 - ratio) * m_genome
         girl_genome = ratio * m_genome + (1 - ratio) * f_genome

         boy_gene.append(boy_genome)
         girl_gene.append(girl_genome)
      
      boy = Individual(gene=boy_gene, cost=np.inf)
      girl = Individual(gene=girl_gene, cost=np.inf)

      return boy, girl

   return lambda_average_crossover
