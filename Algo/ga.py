from import_data import * 


def distance_squared(a: tuple[float], b: tuple[float]) -> float:
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def fitness(cycle: list[int], lat: list[float], lon: list[float]) -> float:
    score = 0
    for i, j in zip(cycle[:-1], cycle[1:]):
        pass

if __name__ == "__main__":
    lat, lon = coordinates("2_detail_table_customers.xls", "4_detail_table_depots.xls")
    visualize_coordinates(lat, lon)