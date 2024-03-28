import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

from utils import *

"""Algo recuit simulé"""

def recuit(solution_initiale, coord_dict, t0 = 10,nbiter_cycle = 1e2,a = 0.99):
  # X = une solution (initiale) qui fonctionne
  # t0 = température initiale
  # nbiter_cycle = nbr de paliers
  # a = coefficient de refroidissement
  
  #Initialisation
  best_solution = np.copy(solution_initiale)
  best_cost = cost(best_solution, coord_dict)
  nbiter = 0
  nouveaucycle = True
  t = t0

  #Itération tant qu'on a pas atteint l'équilibre du système
  while nouveaucycle == True: 
    nbiter = 0
    nouveaucycle = False
    
    while nbiter < nbiter_cycle:
      nbiter += 1

      solution_voisine = np.copy(best_solution)
      solution_voisine = swap_elements_cycle(solution_voisine)

      #On compare le coût des deux solutions 
      neighbor_cost = cost(solution_voisine, coord_dict)
      difference = neighbor_cost - best_cost

      #Si la nouvelle solution est meilleure que la précédente on la garde
      if difference < 0:
        best_solution=solution_voisine
        best_cost = neighbor_cost
        nouveaucycle=True
      
      #Si elle est moins bonne, on peut la garder avec une certaine probabilité 
      else:
        probabilite = np.exp(-difference / t)
        q = random.random()

        if q < probabilite:
          best_solution = solution_voisine
          best_cost = neighbor_cost
          nouveaucycle=True

    t *= a

  return [best_cost, best_solution]