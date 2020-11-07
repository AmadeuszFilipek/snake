import evolution as evo
import crossover_operators as xso
import mutation_operators as mo
import math

def rastrigin_function(arguments):
   result = 0
   for x in arguments:
      result += x ** 2 - 10 * math.cos(18 * x)
   
   result += 10 * len(arguments)

   return result

if __name__ == "__main__":

   crossover_operators = [
      # xso.average_crossover(ratio=0.2),
      # xso.shuffle_crossover(mixing_rate=0.5),
      xso.gamma_weighted_crossover()
   ]

   mutation_operators = [
      # mo.univariate_mutate(mu=0, sigma=0.05),
      mo.gauss_rate_mutate(mu=0, sigma=1),
      # mo.gauss_mutate(mu=0, sigma=2),
      mo.null_mutate()
      # mo.spike_mutate(),
      # mo.negate_mutate(),
   ]
 
   results = evo.evolution_optimise(
      bounds=evo.Bounds(-5, 5),
       target=rastrigin_function,
       crossover_operators=crossover_operators,
       mutation_operators=mutation_operators,
       dimensions=100,
       population_size=100,
       generations=1000,
       workers=1
   )

   print('results: ', results.cost)

   # first observations: parent rate plays huge difference
   # those two operators does not make much of a difference... just becouse this target function
   # is retarded, it does not care for relations between the data