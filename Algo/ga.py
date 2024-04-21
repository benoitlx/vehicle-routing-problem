from utils import * 
from import_data import * 
import numpy as np
from random import uniform, sample, choice 

class GA():

    def __init__(self, lat: list[float], lon: list[float], size: int, vehicle_num: int, iteration: int, proba: float) -> None:
        self.lat = lat
        self.lon = lon
        self.n = len(lat) - 1
        self.m = vehicle_num
        self.iteration = iteration
        # self.select_ratio

        self.pop_size = size
        self.init_pop = self.gen_initial_pop()
        self.cross_proba = proba
        self.final_pop = None

        self.scores = []

    def gen_initial_pop(self) -> list[cycles]:
        """
        @retval a list of pop_size cycles representing the population
        O(np) where n is the number of customers and p the population size
        """
        return [random_float_cycles(self.n, self.m) for _ in range(self.pop_size)]

    def fitness(self, c: cycles) -> float:
        """
        TODO 
        - sort cycles and get sorted indices
        - indices -> score
        O(n log n)
        """

        cyc = float_cycles_to_indices(c, self.m)
        n_la = []
        n_lo = []
        for cycle in cyc:
            for c in cycle:
                n_la.append(self.lat[c])
                n_lo.append(self.lon[c])
        coordinates = list(zip(n_la, n_lo))
        distances = []
        n = len(coordinates)

        for i, coord in enumerate(coordinates):
            distances.append(distance_squared(coord, coordinates[(i+1)%n]))

        return sum(distances)

    def crossover(self, p1: cycles, p2: cycles) -> cycles:
        """
        @retval a cycles sharing similarity with p1 and p2
        O(n)
        """
        return [p1[i] if uniform(0, 1) >= self.cross_proba else p2[i] for i in range(self.n)] 

    def next_gen(self, pop: list[cycles]) -> list[cycles]:
        """
        - Select random individuals in pop
        - Class these individuals by fitness (priority queue insertion)
        - Reproduce best individuals while next_pop size <= pop_size
        O(np log n)
        """
        # selection = sample(pop, int(self.pop_size/self.select_ratio))

        next_gen = []
        while len(next_gen) < self.pop_size:
            sub_select = sorted(sample(pop, 10), key=lambda x:self.fitness(x))
            sub_select = sub_select[:5]
            p1 = choice(sub_select) 
            p2 = choice(sub_select)

            next_gen.append(self.crossover(p1, p2))

        self.scores.append(self.fitness(next_gen[0]))

        return next_gen

    def evolve(self) -> None:
        """
        O(npi log n)
        """
        pop = self.init_pop
        for _ in range(self.iteration):
            #print(pop)
            #visualize_cycles(float_cycles_to_indices(pop[0], self.m), self.lat, self.lon)
            pop = self.next_gen(pop)

        self.final_pop = pop

    def final_cycles(self) -> cycles:
        """
        IDEA: on pourrait choisir le meilleur
        O(1)
        """
        return self.final_pop[0] 


if __name__ == "__main__":
    coords = coordinates("2_detail_table_customers.xls", "4_detail_table_depots.xls")
    #print(coords)

    lat = [x[1] for x in coords]
    lon = [x[2] for x in coords]


    #_, lat, lon = coordinates("2_detail_table_customers.xls", "4_detail_table_depots.xls")

    lat = [0]
    lon = [0]
    for _ in range(30):
        lat.append(uniform(-5, 5))
        lon.append(uniform(-5, 5))

    n = len(lat) - 1
    m = 4 

    # + pop_size => + diversity
    # + iteration => less chance of missing good solution

    # Remarque: je pense que la diversité disparait trop vite

    g = GA(lat, lon, 150, m, 80, 0.25)
    g.evolve()
    c = g.final_cycles()
    Y = g.scores
    plt.plot(list(range(len(Y))), Y)
    plt.show()
    visualize_cycles(float_cycles_to_indices(g.init_pop[0], m), lat, lon)
    visualize_cycles(float_cycles_to_indices(c, m), lat, lon)
