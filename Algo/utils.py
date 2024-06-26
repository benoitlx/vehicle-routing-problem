from random import shuffle, randint, uniform
import matplotlib.pyplot as plt
from math import floor
from numpy import sqrt

from import_data import *


def random_cycles(n: int, m: int) -> list[list[int]]:
    """
    @parameters
    n: the number of customers
    m: the number of vehicle

    @return-value
    a list of list of index representing the cycles of each vehicles
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


def random_float_cycles(n: int, m: int):
    return np.array([randint(0, m-1) + uniform(0, 1) for _ in range(n)])


def float_cycles_to_indices(c, m: int) -> list[list[int]]:
    cyc = [[0] for _ in range(m)]
    indices = np.argsort(c) # O(n log n)
    print(f'indices = {indices}')
    for i in indices:
        vehicle_id = floor(c[i])
        cyc[vehicle_id].append(i+1)

    for i in range(len(cyc)):
        cyc[i].append(0)

    return cyc


def indice_cycles_to_codes(cycle_indices, coordinates):
    cycle_codes = cycle_indices.copy()
    for i in range(len(cycle_indices)):
        for j in range(len(cycle_indices[i])):
            cycle_codes[i][j] = coordinates[cycle_indices[i][j]][0]
    return cycle_codes


def gen_init_sol(cust_file, depots_file, vehicle_capacity):
    coordinates_list = coordinates(cust_file, depots_file)
    depots_data = coordinates_list.pop(0)

    n_clients = len(coordinates_list)
    if n_clients % vehicle_capacity == 0 : 
        n_vehicules = n_clients//vehicle_capacity 
    else : 
        n_vehicules = n_clients//vehicle_capacity + 1

    shuffle(coordinates_list)

    sol = []
    for i in range(n_vehicules):
        sol.append([0])
        while len(sol[i]) < vehicle_capacity + 1 and len(coordinates_list)>0:
            sol[i].append(coordinates_list.pop(0)[0])
        
        sol[i].append(0)

    return sol


def coord_to_dict(coordinates):
    keys = ['Code', 'lat', 'long']
    coord_dict = {key: [] for key in keys}

    for client in coordinates:
        coord_dict['Code'].append(client[0])
        coord_dict['lat'].append(client[1])
        coord_dict['long'].append(client[2])

    return coord_dict


def find_coords_from_code(code: int, coord_dict):
    client_index = coord_dict['Code'].index(code)

    return coord_dict['lat'][client_index], coord_dict['long'][client_index]

def cost(solution, coord_dict, penality_coeff = 100):
    cost = 0
    n_vehicules = len(solution)
    cost += penality_coeff * n_vehicules

    for i in range(n_vehicules):
        for j in range(len(solution[i]) -  1):
            code1 = solution[i][j]
            code2 = solution[i][j + 1]
            
            lat1, long1 = find_coords_from_code(code1, coord_dict)
            lat2, long2 = find_coords_from_code(code2, coord_dict)

            cost += sqrt(distance_squared([lat1, long1], [lat2, long2]))
            
    return cost


def distance_squared(a: tuple[float], b: tuple[float]) -> float:
    return (a[0]-b[0])**2 + (a[1]-b[1])**2


def visualize_cycles(cycles: list[list[int]], lat: list[float], long: list[float]) -> None:
    visualize_coordinates(lat, long)
    X = [] 
    Y = []
    compteur = 0

    for cycle in cycles:
        #print(cycle)
        for c in range(len(cycle)):
            X.append(lat[compteur])
            Y.append(long[compteur])
            compteur +=1
            #print(c)
        
        plt.plot(X, Y)
        X = []
        Y = []

    plt.savefig("Figure")
    plt.show(block=False)


def swap_elements_cycle(cycles: list[list[int]]) -> list[list[int]]:
    n = len(cycles)
    swapped_cycles = cycles.copy()
    swap = False

    while (swap == False) :
        i1 = randint(0, n-1)
        i2 = randint(1, len(cycles[i1])-2)
        j1 = randint(0, n-1)
        j2 = randint(1, len(cycles[j1])-2)

        if (i1, i2) != (j1, j2):
            swapped_cycles[i1][i2], swapped_cycles[j1][j2] = swapped_cycles[j1][j2], swapped_cycles[i1][i2]
            swap = True

    return swapped_cycles


if __name__ == "__main__":
    coords = coordinates("2_detail_table_customers.xls", "4_detail_table_depots.xls")
    #print(coords)

    lat = [x[1] for x in coords]
    lon = [x[2] for x in coords]
    #lat, lon = coordinates("2_detail_table_customers.xls", "4_detail_table_depots.xls")
    """
    n = len(lat) - 1
    cycles = random_cycles(n, 8)
    visualize_cycles(cycles, lat, lon)
    """
    c = random_float_cycles(10, 3)
    print(c)
    print(float_cycles_to_indices(c, 3))