import unittest
import evolution as evo

class TestEvolution(unittest.TestCase):

   def test_generate_individual(self):
      specimen = evo.generate_individual(10, evo.Bounds(min=5, max=7))

      self.assertEqual(specimen.cost, 0)
      self.assertEqual(len(specimen.gene), 10)
      for genome in specimen.gene:
         self.assertGreater(genome, 5)
         self.assertGreater(7, genome)
   
   def test_construct_bins_initial(self):
      
      population = []
      population.append(evo.Individual(gene=[0], cost=0))
      population.append(evo.Individual(gene=[0], cost=0))

      result = evo.construct_bins(population)
      expected = [evo.Bin(min=0, max=0.5), evo.Bin(min=0.5, max=1)]
      
      self.assertEqual(result, expected)

   def test_construct_bins_binary(self):
      
      population = []
      population.append(evo.Individual(gene=[0], cost=0))
      population.append(evo.Individual(gene=[0], cost=-1))

      result = evo.construct_bins(population)
      expected = [evo.Bin(min=0, max=0), evo.Bin(min=0, max=1)]
      
      self.assertEqual(result, expected)

   def test_construct_bins_weighted_1(self):
      
      population = []
      population.append(evo.Individual(gene=[0], cost=-5))
      population.append(evo.Individual(gene=[0], cost=-10))

      result = evo.construct_bins(population)
      expected = [
         evo.Bin(min=0, max=0.3333333333333333),
         evo.Bin(min=0.3333333333333333, max=1)
      ]
      
      self.assertEqual(result, expected)

   def test_construct_bins_weighted_2(self):
      
      population = []
      population.append(evo.Individual(gene=[0], cost=-5))
      population.append(evo.Individual(gene=[0], cost=-10))
      population.append(evo.Individual(gene=[0], cost=-15))

      result = evo.construct_bins(population)
      expected = [
         evo.Bin(min=0, max=0.16666666666666666),
         evo.Bin(min=0.16666666666666666, max=0.5),
         evo.Bin(min=0.5,  max=1)
      ]
      
      self.assertEqual(result, expected)

   def test_construct_bins_long_input(self):
      
      population = []
      population.append(evo.Individual(gene=[0], cost=-1))
      population.append(evo.Individual(gene=[0], cost=-2))
      population.append(evo.Individual(gene=[0], cost=-3))
      population.append(evo.Individual(gene=[0], cost=-4))
      population.append(evo.Individual(gene=[0], cost=-5))
      population.append(evo.Individual(gene=[0], cost=-6))

      result = evo.construct_bins(population)
      expected = [
         evo.Bin(min=0, max=0.047619047619047616),
         evo.Bin(min=0.047619047619047616, max=0.14285714285714285),
         evo.Bin(min=0.14285714285714285, max=0.2857142857142857),
         evo.Bin(min=0.2857142857142857, max=0.47619047619047616),
         evo.Bin(min=0.47619047619047616, max=0.7142857142857142),
         evo.Bin(0.7142857142857142, max=0.9999999999999999)
      ]
      
      self.assertEqual(result, expected)

   def test_select_mating_pool_two_times_best(self):

      population = []
      population.append(evo.Individual(gene=[0], cost=0))
      population.append(evo.Individual(gene=[1], cost=-2))

      pool_size = 2
      result = evo.select_mating_pool(population, pool_size)
      expected = [
         evo.Individual(gene=[1], cost=-2),
         evo.Individual(gene=[1], cost=-2)
      ]

      self.assertEqual(result, expected)

   def test_select_mating_pool_one_best(self):

      population = []
      population.append(evo.Individual(gene=[0], cost=0))
      population.append(evo.Individual(gene=[0], cost=0))
      population.append(evo.Individual(gene=[0], cost=0))
      population.append(evo.Individual(gene=[0], cost=0))
      population.append(evo.Individual(gene=[1], cost=-2))

      pool_size = 1
      result = evo.select_mating_pool(population, pool_size)
      expected = [
         evo.Individual(gene=[1], cost=-2)
      ]

      self.assertEqual(result, expected)

   def test_select_mating_pool_roulette(self):

      population = []
      population.append(evo.Individual(gene=[0], cost=-5))
      population.append(evo.Individual(gene=[0], cost=-10))
      population.append(evo.Individual(gene=[1], cost=-15))

      times_best_picked = 0
      check = 1000
      pool_size = 1
      for i in range(check):
         parents = evo.select_mating_pool(population, pool_size)

         expected = [
            evo.Individual(gene=[1], cost=-15)
         ]
         if parents == expected:
            times_best_picked += 1

      ratio = times_best_picked / check
      self.assertAlmostEqual(ratio, 1/2, places=1)

   def test_crossover_twice_the_same(self):

      father = evo.Individual(gene=[5, 5], cost=0)
      mother = evo.Individual(gene=[5, 5], cost=0)
      boy, girl = evo.gamma_weighted_crossover(father, mother)

      self.assertAlmostEqual(boy, girl)

   def test_crossover_twice_the_same(self):

      father = evo.Individual(gene=[5, 5], cost=0)
      mother = evo.Individual(gene=[5, 5], cost=0)
      
      for i in range(100):
         boy, girl = evo.gamma_weighted_crossover(father, mother)
         self.assertAlmostEqual(boy, girl)

   def test_crossover_different(self):

      father = evo.Individual(gene=[-10, -10], cost=0)
      mother = evo.Individual(gene=[10, 10], cost=0)

      for i in range(100):
         boy, girl = evo.gamma_weighted_crossover(father, mother)
         genes = boy.gene + girl.gene
         for genome in genes:
            self.assertGreater(genome, -10)
            self.assertLess(genome, 10)

 

if __name__ == "__main__":
    unittest.main()