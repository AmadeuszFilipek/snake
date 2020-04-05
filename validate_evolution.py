import evolution as evo
import math

def rastrigin_function(arguments):
   result = 0
   for x in arguments:
      result += x ** 2 - math.cos(18 * x)
   
   return result

if __name__ == "__main__":

   shuffle_crossover_operator = evo.shuffle_crossover(0.5)
   gamma_crossover_operator = evo.gamma_weighted_crossover(tau=10)

   gamma = evo.evolution_optimise(
       target=rastrigin_function,
       crossover_operator=shuffle_crossover_operator,
       dimensions=100,
       population_size=100,
       generations=100,
       workers=1
   )

   shuffle = evo.evolution_optimise(
       target=rastrigin_function,
       crossover_operator=shuffle_crossover_operator,
       dimensions=100,
       population_size=100,
       generations=100,
       workers=1
   )

   print('gamma: ', gamma.cost)
   print('shuffle: ', shuffle.cost)

   # first observations: parent rate plays huge difference
   # those two operators does not make much of a difference... just becouse this target function
   # is retarded, it does not care for relations between the data