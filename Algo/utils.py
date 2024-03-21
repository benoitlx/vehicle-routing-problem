from random import shuffle, randint, uniform
from import_data import *
import matplotlib.pyplot as plt
from math import floor

type cycles = np.ndarray[float]

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

def random_float_cycles(n: int, m: int) -> cycles:
    """
    O(n)
    """
    return np.array([randint(0, m-1) + uniform(0, 1) for _ in range(n)])

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


def distance_squared(a: tuple[float], b: tuple[float]) -> float:
    """
    O(1)
    """
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

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