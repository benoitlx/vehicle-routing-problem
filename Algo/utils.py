from random import shuffle
from import_data import *
import matplotlib.pyplot as plt

def random_cycles(n: int, m: int) -> list[list[int]]:
    """
    @parameters
    n: the number of customers
    m: the number of vehicle

    @return-value
    a list of list of index representing the cycles of each vehicles
    """
    
    cycles = [[] for _ in range(m)]
    cycles[0].append(0)
    custs = list(range(1, n+1))
    shuffle(custs)

    sep = list(range(n-1))
    shuffle(sep)
    sep = list(sep)[:(m-1)]

    j = 0
    for i in range(n):
        cycles[j].append(custs[i])
        if i in sep:
            cycles[j].append(0)
            j += 1
            cycles[j].insert(0, 0)

    cycles[m-1].append(0)

    return cycles

def distance_squared(a: tuple[float], b: tuple[float]) -> float:
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def visualize_cycles(cycles: list[list[int]], lat: list[float], lon: list[float]) -> None:
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
    n = len(lat) - 1
    cycles = random_cycles(n, 8)
    visualize_cycles(cycles, lat, lon)