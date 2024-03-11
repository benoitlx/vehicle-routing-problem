from utils import * 
from import_data import * 
import numpy as np
from random import uniform

class GA():

    def __init__(self, lat: list[float], lon: list[float], size: int, vehicle_num: int, iteration: int) -> None:
        self.lat = lat
        self.lon = lon
        self.N = len(lat) - 1
        self.m = vehicle_num
        self.iteration = iteration

        self.pop_size = size
        self.init_pop = self.gen_initial_pop()

    def gen_initial_pop(self) -> np.ndarray[list[list[int]]]:
        return np.array([random_cycles(self.N, self.m) for _ in range(self.pop_size)])

    def fitness(self, cycles: list[list[int]]) -> float:
        n_la = []
        n_lo = []
        for cycle in cycles:
            for c in cycle:
                n_la.append(self.lat[c])
                n_lo.append(self.lon[c])
        coordinates = list(zip(n_la, n_lo))
        distances = []
        n = len(coordinates)

        for i, coord in enumerate(coordinates):
            distances.append(distance_squared(coord, coordinates[(i+1)%n]))

        return sum(distances)

    def crossover(self, p1: list[list[int]], p2: list[list[int]]) -> list[list[int]]:
        proba_p1 = [[] for _ in range(self.m)]
        proba_p2 = [[] for _ in range(self.m)]

        child = [[] for _ in range(self.m)]

        for i, cycle in enumerate(p1):
            for _ in cycle:
                proba_p1[i].append(uniform(0, 1))
                proba_p2[i].append(uniform(0, 1))
            proba_p1[i].sort()
            proba_p2[i].sort()

        for i, cycle in enumerate(child):
            for j, _ in enumerate(cycle):
                if proba_p1[i][j] >= proba_p2[i][j]:
                    child[i].append(p1[i][j])
                else:
                    child[i].append(p2[i][j])

        return child

    def next_gen(self, pop: np.ndarray[list[list[int]]]):
        pass

    def evolve(self) -> np.ndarray[list[list[int]]]:
        pop = self.init_pop
        for i in range(self.iteration):
            pop = self.next_gen(pop)

        return pop

    def final_cycles(self) -> list[list[int]]:
        pass


if __name__ == "__main__":
    lat, lon = coordinates("2_detail_table_customers.xls", "4_detail_table_depots.xls")
    n = len(lat) - 1
    cycles = random_cycles(n, 8)
    ga = GA(lat, lon)
    print(ga.fitness(cycles))