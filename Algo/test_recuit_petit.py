import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from import_data import *
from utils import *
from recuit_simule import *

L=[[0,1,2,3,4,5,0],[0,6,7,8,9,10,0],[0,11,12,13,14,15,0]]
positions = [[0, 43.37391833, 17.60171712], 
             [1, 43.41305, 17.87588],
             [2, 43.135963, 17.776839],
             [3, 43.46907801, 17.33702249],
             [4, 43.70716, 17.2229],
             [5, 43.08222786, 17.96003741],
             [6, 43.46470189, 17.31043644],
             [7, 43.35266, 17.80444],
             [8, 43.48189308, 17.30045863],
             [9, 43.35459, 17.79902],
             [10, 43.396088, 17.871369],
             [11, 43.71657, 17.23185],
             [12, 43.11036, 17.70165],
             [13, 43.71619, 17.2317],
             [14, 43.54998018, 17.42732548], 
             [15, 43.475001, 17.325417]]

dict_positions = coord_to_dict(positions)
#print(dict_positions)

solution  = recuit_simule(L,dict_positions)
#print(solution)
lat=[]
long=[]
for i in range(len(solution[1])): 
    for j in range(len(solution[1][i])):
        latitude,longitude = find_coords_from_code(solution[1][i][j], dict_positions)
        lat+= [latitude]
        long+= [longitude]

#visualize_coordinates(lat,long)
#plt.show()
print("Le coût de cette solution est : ", solution[0])
visualize_cycles(solution[1], lat, long)

