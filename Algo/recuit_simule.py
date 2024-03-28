import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from mesa import Agent

from utils import *

"""Algo recuit simulé"""

def recuit_simule(solution_initiale, coord_dict, t0 = 10,nbiter_cycle = 1e2,a = 0.99):
  # Solution (initiale) qui fonctionne
  # coord_dict = dictionnaire contenant l'id la latitude et la longitude du dépôt et de tous les clients
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
    
    #Tant que le cycle en cours n'a pas atteint une solution satisfaisante
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

    #Le système refroidit 
    t *= a

  return [best_cost, best_solution]


#Création de l'Agent Recuit 
class AgentRecuit(Agent):
  
  #Initialisation de l'agent
  def __init__(self, unique_id, model, solution_initiale, coord_dict, t0 = 10,nbiter_cycle = 1e2,a = 0.99):
    super.__init__(unique_id, model)

    self.cost = solution_initiale[0]
    self.solution = solution_initiale[1]
    self.dict = coord_dict
    self.t_init = t0
    self.nbiter_cycle = nbiter_cycle
    self.a = a

  #Définition de la fonction de contact permetant à 2 algos d'échanger leurs solutions
  def contact(self):
    # On regarde tous les voisins $
    for agent in self.model.schedule.agents:
      #Si l'un d'entre eux à un meilleur coût que nous, on le garde et on prend sa solution
      if agent.cost<self.cost:
          self.cost=agent.cost
          self.solution=agent.solution

  #Définition de la fonction step
  def step(self):
    #On calcule la solution grâce à l'algo de recuit 
    variable=recuit_simule([self.cost,self.solution],self.dict,self.t_init,self.nbiter_cycle,self.a) #Variable = [cout, [routes]]
    self.cost=variable[0]
    self.solution=variable[1]
    #On compare les réultats des différents algos
    self.contact()





  
