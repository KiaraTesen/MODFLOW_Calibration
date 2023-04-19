# -*- coding: utf-8 -*-

#---    Packages
from Functions_DPSO import *
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from functools import reduce
import time
import warnings
import sys
from request_server.request_server import send_request_py
warnings.filterwarnings('ignore')

#---    Paths
path_WEAP = r'C:\Users\Francisco Suárez P\Documents\WEAP Areas\SyntheticProblem_WEAPMODFLOW'
path_model = os.path.join(path_WEAP, 'MODFLOW_model')
path_nwt_exe = r'..\MODFLOW-NWT_1.2.0\bin\MODFLOW-NWT_64.exe'
path_GIS = r'..\GIS'
path_output = r'C:\Users\Francisco Suárez P\Desktop\GitHub - KT\MODFLOW_Calibration\data\output'      
path_obs_data = r'..\ObservedData'

#---    Initial matriz
HP = ['kx', 'sy'] 
initial_shape_HP = gpd.read_file(path_GIS + '/Elements_initial.shp')                   # El shape que se use depende del mejor resultado (?)
active_matriz = initial_shape_HP['Active'].to_numpy().reshape((84,185))             # Matriz de ceros y unos que permite uniformizar mantener área activa

for k in HP:
    locals()["init_matriz_" + str(k)] = initial_shape_HP[k].to_numpy().reshape((84,185))
    get_image_matriz(locals()["init_matriz_" + str(k)], str(k), os.path.join(path_GIS, str(k) +'.png'))
    plt.clf()

#---    Initial Sampling (Latyn Hypercube)
class Particle:
    def __init__(self,x,v,y):
        self.x = x                      # X contiene a los dos kernel
        self.v = v                      # velocidad del muestreo inicial = 0
        self.x_best = x                 # Para muestreo inicial sería X
        self.y = y
        self.y_best = y

n = 1                                                           # Population size

kernel_shape_1_kx = (5,5)
kernel_shape_1_sy = (5,5)
kernel_shape_2_kx = (3,3)
kernel_shape_2_sy = (10,10)

n_var_1_kx = reduce(lambda x,y: x*y, kernel_shape_1_kx)     
n_var_1_sy = reduce(lambda x,y: x*y, kernel_shape_1_sy)              
n_var_2_kx = reduce(lambda x,y: x*y, kernel_shape_2_kx)
n_var_2_sy = reduce(lambda x,y: x*y, kernel_shape_2_sy)
n_var = n_var_1_kx + n_var_1_sy + n_var_2_kx + n_var_2_sy       # Number of variables

l_bounds = np.concatenate((np.repeat(0, n_var_1_kx), np.repeat(0, n_var_1_sy),                      # First and third block: Hydraulic conductivity (K), 0.85 - 
                           np.repeat(0, n_var_2_kx), np.repeat(0, n_var_2_sy)), axis = 0)           # Second and fourth block: Specific yield (Sy), 0.05   
u_bounds = np.concatenate((np.repeat(0.2, n_var_1_kx), np.repeat(0.2, n_var_1_sy),                  # First and third block: Hydraulic conductivity (K), 1.01 - 
                           np.repeat(0.12, n_var_2_kx), np.repeat(0.1, n_var_2_sy)), axis = 0)       # Second and fourth block: Specific yield (Sy), 0.99
sample_scaled = get_sampling_LH(n_var, n, l_bounds, u_bounds)

pob = Particle(sample_scaled[0],np.array([0]*(n_var)),10000000000)

y_best = Run_WEAP_MODFLOW(path_output, str(0), initial_shape_HP, HP, pob.x, n_var_1_kx, n_var_1_sy, n_var_2_kx, n_var_2_sy, n_var, kernel_shape_1_kx, kernel_shape_1_sy, 
                          kernel_shape_2_kx, kernel_shape_2_sy, active_matriz, path_model, path_nwt_exe, path_obs_data)
