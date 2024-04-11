import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy

from import_data import *
from utils import *
from recuit_simule import *


cust_file = '2_detail_table_customers.xls'

depots_file = '4_detail_table_depots.xls'

data = coordinates(cust_file, depots_file)
coord_dict = coord_to_dict(data)

sol_init = gen_init_sol (cust_file, depots_file, 30)

solution  = recuit_simule(sol_init,coord_dict)
#print(solution)

lat=[]
long=[]
for i in range(len(solution[1])): 
    for j in range(len(solution[1][i])):
        latitude,longitude = find_coords_from_code(solution[1][i][j], coord_dict)
        lat+= [latitude]
        long+= [longitude]

# visualize_coordinates(lat,long)
# plt.show()

print("Le coût de cette solution est : ", solution[0])
visualize_cycles(solution[1], lat, long)