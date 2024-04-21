import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

from utils import *
from recuit_simule import *

class ModelVRPTW(Model):
    
    def __init__(self, population, coord_dict, t0 = 10,nbiter_cycle = 1e2,a = 0.99, N_RS = 1, N_TB=1, N_AG=1):
        super.__init__()
        
        self.dict = coord_dict
        self.t_init = t0
        self.nbiter_cycle = nbiter_cycle
        self.a = a
        self.population=population
        self.NRS = N_RS
        self.NTB = N_TB
        self.NAG = N_AG

        self.best_cost=random.choice(self.population)[0]

        #Schedule
        self.schedule = SimultaneousActivation(self)

        #Créer agents Recuit
        for i in range(int(self.NRS)):
            solution_test = random.choice(self.population)
            agent = AgentRecuit(i, self, solution_test, self.dict, self.t_init, self.nbiter_cycle, self.a)
            self.schedule.add(agent)
        
        #Créer agents Tabou


        #Créer agents Génétique 
            
        
        #Datacollector
        self.datacollector = DataCollector(model_reporter = {"Meilleur coût" : lambda m : m.best_cost})
        
    def step(self): 
        self.schedule.step()
        self.best_cost=random.choice(self.schedule.agents).cost
        self.datacollector.collect(self)