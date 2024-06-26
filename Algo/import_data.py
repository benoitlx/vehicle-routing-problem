import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def extract_file_info(cust_file, depot_file):
    """
    Return a tuple (code, lat, lon)
    where lat[0], lon[0] is the coordinate of the depot and lat[1:], lon[1:] are
    the coordinates of the customers
    O(n)
    """
    prefix = '../Data/'
    df_cust = pd.read_excel(prefix + cust_file).drop_duplicates(subset = ['CUSTOMER_CODE'])
    df_petit = df_cust.iloc[0:100]
    df_depot = pd.read_excel(prefix + depot_file)

    code = list(df_petit["CUSTOMER_CODE"].to_numpy())
    lat = list(df_petit["CUSTOMER_LATITUDE"].to_numpy())
    lon = list(df_petit["CUSTOMER_LONGITUDE"].to_numpy())

    lat_depot = df_depot["DEPOT_LATITUDE"].to_numpy()[0]
    lon_depot = df_depot["DEPOT_LONGITUDE"].to_numpy()[0]

    code.insert(0, 0)
    lat.insert(0, lat_depot)
    lon.insert(0, lon_depot)

    return code, lat, lon

def coordinates(cust_file: str, depot_file: str) -> tuple[list[float]]:
    code, lat, lon = extract_file_info(cust_file, depot_file)
    return list(zip(code, lat, lon))

def visualize_coordinates(lat: list[float], lon: list[float]) -> None:
    """
    Display in red the depot and in blue customers
    TODO add google maps visualization
    O(n)
    """
    cat = np.array([0] + ([1] * (len(lat)-1)))
    colormap = np.array(['r', 'b'])
    sizemap = np.array([100, 10])
    plt.scatter(lat, lon, s=sizemap[cat], c=colormap[cat])


if __name__ == "__main__":
    lat, lon = coordinates("2_detail_table_customers.xls", "4_detail_table_depots.xls")
    visualize_coordinates(lat, lon)