from utils import * 
from import_data import * 


class GA():

    def __init__(self, lat: list[float], lon: list[float]) -> None:
        self.lat = lat
        self.lon = lon


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

if __name__ == "__main__":
    lat, lon = coordinates("2_detail_table_customers.xls", "4_detail_table_depots.xls")
    n = len(lat) - 1
    cycles = random_cycles(n, 8)
    ga = GA(lat, lon)
    print(ga.fitness(cycles))
