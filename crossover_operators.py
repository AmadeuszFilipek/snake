from collections import namedtuple
import numpy as np
import random as rng
from neural_net import shape_parameters, flatten_shaped_parameters, alternate
import code

Individual = namedtuple('Individual', ['gene', 'cost'])
Bounds = namedtuple('Bounds', ['min', 'max'])

def gamma_weighted_crossover(tau=10):
   ''' gamma parameter is randomly generated (0, 1) for each genome '''

   def lambda_gamma_weighted_crossover(father, mother):
      boy_gene = []
      girl_gene = []

      for f_genome, m_genome in zip(father.gene, mother.gene):

         gamma = rng.random()
         if gamma < 0.5:
            gamma = (2 * gamma) ** (1 / (tau + 1))
         else:
            gamma = (1 / (2 * (1 - gamma))) ** (1 / (tau + 1))

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

def single_point_crossover():
   ''' classical single point crossover, take two genes,
       cut them at random point and glue the parts together
   '''

   def lambda_single_point_crossover(father, mother):
      crosspoint = rng.choice(range(len(father.gene)))
      
      boy_gene = father.gene[:crosspoint] + mother.gene[crosspoint:]
      girl_gene = mother.gene[:crosspoint] + father.gene[crosspoint:]

      boy = Individual(gene=boy_gene, cost=np.inf)
      girl = Individual(gene=girl_gene, cost=np.inf)

      return boy, girl

   return lambda_single_point_crossover

def identity_crossover():
   ''' resultant genes are exact copy of input genes
   '''

   def lambda_identity_crossover(father, mother):

      boy = Individual(gene=father.gene, cost=np.inf)
      girl = Individual(gene=mother.gene, cost=np.inf)

      return boy, girl

   return lambda_identity_crossover

def neural_crossover(shapes):
   ''' cut each layer+bias neuron-wise and glue parts from parents
       shapes - shape of neural net structure
   '''

   def lambda_neural_crossover(father, mother):

      father_layers = shape_parameters(shapes, father.gene)
      mother_layers = shape_parameters(shapes, mother.gene)

      crosspoint = rng.choice(range(len(father_layers)))

      # for each weight_matrix + bias matrix
      # generate cut point for vertical cut-off
      # meaning that each weight layer + bias will be cut neuron-wise
      # so that each neuron holds its bias and input weights ...
      
      boy_layers = []
      girl_layers = []

      for (weight_i, bias_i) in alternate(range(len(father_layers))):
         father_layer = father_layers[weight_i]
         father_bias = father_layers[bias_i]

         mother_layer = mother_layers[weight_i]
         mother_bias = mother_layers[bias_i]

         crosspoint = rng.choice(range(len(father_bias)))
         # crosspoint = len(father_bias) // 2

         boy_layer = father_layer.copy()
         boy_layer[:, crosspoint:] = mother_layer[:, crosspoint:]

         boy_bias = father_bias.copy()
         boy_bias[crosspoint:] = mother_bias[crosspoint:]

         girl_layer = mother_layer.copy()
         girl_bias = mother_bias.copy()
         
         girl_layer[:, crosspoint:] = father_layer[:, crosspoint:]
         girl_bias[crosspoint:] = father_bias[crosspoint:]

         boy_layers.append(boy_layer)
         boy_layers.append(boy_bias)
         girl_layers.append(girl_layer)
         girl_layers.append(girl_bias)

      boy_gene = flatten_shaped_parameters(boy_layers)
      girl_gene = flatten_shaped_parameters(girl_layers)

      boy = Individual(gene=boy_gene, cost=np.inf)
      girl = Individual(gene=girl_gene, cost=np.inf)

      return boy, girl

   return lambda_neural_crossover

def neural_layer_crossover(shapes):
   ''' cut networks by their layers and glue the layers back toghether
   '''

   def lambda_neural_layer_crossover(father, mother):
      father_layers = shape_parameters(shapes, father.gene)
      mother_layers = shape_parameters(shapes, mother.gene)

      # choose point in bias layer
      crosspoint = rng.choice(range(1, len(father_layers), 2))

      boy_layers = father_layers[:crosspoint] + mother_layers[crosspoint:]
      girl_layers = mother_layers[:crosspoint] + father_layers[crosspoint:]

      boy_gene = flatten_shaped_parameters(boy_layers)
      girl_gene = flatten_shaped_parameters(girl_layers)

      boy = Individual(gene=boy_gene, cost=np.inf)
      girl = Individual(gene=girl_gene, cost=np.inf)

      return boy, girl

   return lambda_neural_layer_crossover