from random import shuffle, randint, uniform
from import_data import *
import matplotlib.pyplot as plt
from math import floor
import numpy as np
import random


type cycles = np.ndarray[float]

# Fonction permettant de créer une solution initiale 
def random_cycles(n: int, m: int) -> list[list[int]]:
    """
    @parameters
    n: the number of customers
    m: the number of vehicle

    @return-value
    a list of list of index representing the cycles of each vehicles
    O(n)
    """
    
    cycles = [[] for _ in range(m)]
    custs = list(range(1, n+1))
    shuffle(custs)

    sep = list(range(n-1))
    shuffle(sep)
    sep = list(sep)[:(m-1)]

    j = 0
    for i in range(n):
        cycles[j].append(custs[i])
        if i in sep:
            j += 1

    return cycles

#
def random_float_cycles(n: int, m: int) -> cycles:
    """
    O(n)
    """
    return np.array([randint(0, m-1) + uniform(0, 1) for _ in range(n)])

#
def float_cycles_to_indices(c: cycles, m: int) -> list[list[int]]:
    """
    O(n log n)
    """
    cyc = [[0] for _ in range(m)]
    indices = np.argsort(c) # O(n log n)
    for i in indices:
        vehicle_id = floor(c[i])
        cyc[vehicle_id].append(i+1)

    for i in range(len(cyc)):
        cyc[i].append(0)

    return cyc

# Fonction pour calculer la distance entre 2 points 
def distance_squared(a: tuple[float], b: tuple[float]) -> float:
    """
    O(1)
    """
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# Fonction permettant d'afficher la solution proposée avec les différentes routes
def visualize_cycles(cycles: list[list[int]], lat: list[float], lon: list[float]) -> None:
    """
    O(n)
    """
    visualize_coordinates(lat, lon)
    X = [] 
    Y = []

    for i, cycle in enumerate(cycles):
        for c in cycle:
            X.append(lat[c])
            Y.append(lon[c])

        plt.plot(X, Y)
        X = []
        Y = []

    plt.show()

# Fonction pour obtenir le nombre de véhicules utilisés dans la solution
def K(x) : 
  Nb_vehicules = 0
  for i in range(len(x)-1) : # -1 pour ne pas prendre le dernier 0
    if x[i]==0 :
      Nb_vehicule+=1
  return Nb_vehicules

# Fonction permettant d'obtenir le coût d'une solution
def cout(solution, clients, omega = 100): 
  somme_distances=0
  nbr_vehicules = K(solution)
  
  for i in range (len(solution)-1): 
    somme_distances += distance_squared(clients[solution[i]], clients[solution[i + 1]])
  return omega*nbr_vehicules+somme_distances

# Fonction pour créer une solution voisine en échnageant la position de deux points aléatoirement
def random_swap(solution):
  swap_indexes = random.choice(solution.shape[0], 2, replace = False)
  valeur_transition = solution[swap_indexes[0]]
  solution[swap_indexes[0]] = solution[swap_indexes[1]] 
  solution[swap_indexes[1]] = valeur_transition
  return solution

if __name__ == "__main__":
    lat, lon = coordinates("2_detail_table_customers.xls", "4_detail_table_depots.xls")
    """
    n = len(lat) - 1
    cycles = random_cycles(n, 8)
    visualize_cycles(cycles, lat, lon)
    """
    c = random_float_cycles(10, 3)
    print(c)
    print(float_cycles_to_indices(c, 3))