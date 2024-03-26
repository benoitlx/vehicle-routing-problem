import numpy as np
import random
import utils as ut

"""Algo recuit simulé"""

def recuit_simule(solution_initiale,t0 = 10,nbiter_cycle = 1e3,a = 0.99):
  # X = une solution (initiale) qui fonctionne
  # t0 = température initiale
  # nbiter_cycle = nbr de paliers
  # a = coefficient de refroidissement
  
  #Initialisation
  best_solution=np.copy(solution_initiale)
  nbiter=0
  nouveaucycle=True
  t=t0

  #Itération tant qu'on a pas atteint l'équilibre du système
  while nouveaucycle==True: 
    nbiter=0
    nouveaucycle=False
    while nbiter<nbiter_cycle:
      nbiter+=1

      solution_voisine=np.copy(best_solution)
      solution_voisine = ut.random_swap(solution_voisine)

      #On compare le coût des deux solutions 
      difference=ut.cout(solution_voisine)-ut.cout(best_solution) 

      #Si la nouvelle solution est meilleure que la précédente on la garde
      if difference<0:
        best_solution=solution_voisine
        nouveaucycle=True
      
      #Si elle est moins bonne, on peut la garder avec une certaine probabilité 
      else:
        probabilite=np.exp(-difference/t)
        q=random.random()
        if q<probabilite:
          best_solution=solution_voisine
          nouveaucycle=True
    t=a*t

  return
