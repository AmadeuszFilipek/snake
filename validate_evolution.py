import evolution as evo
import crossover_operators as xso
import mutation_operators as mo
import math

def rastrigin_function(arguments):
   result = 0
   for x in arguments:
      result += x ** 2 - math.cos(18 * x)
   
   return result

if __name__ == "__main__":

   crossover_operators = [
      xso.shuffle_crossover(mixing_rate=0.1),
      xso.average_crossover(ratio=0.2)
   ]

   mutation_operators = [
      mo.gauss_mutate(mu=0, sigma=0.05),\
      mo.spike_mutate(),
      mo.negate_mutate(),
      mo.univariate_mutate(mu=0, sigma=0.05),
      mo.null_mutate()
   ]
 
   results = evo.evolution_optimise(
       target=rastrigin_function,
       crossover_operators=crossover_operators,
       mutation_operators=mutation_operators,
       dimensions=100,
       population_size=100,
       generations=100,
       workers=1
   )

   print('results: ', results.cost)

   # first observations: parent rate plays huge difference
   # those two operators does not make much of a difference... just becouse this target function
   # is retarded, it does not care for relations between the data