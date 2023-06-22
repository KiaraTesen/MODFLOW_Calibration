# -*- coding: utf-8 -*-

#---    Packages
from Functions_DPSO_nkernel import *
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from functools import reduce
import time
import sys
from request_server.request_server import send_request_py
import warnings
warnings.filterwarnings('ignore')

#IP_SERVER_ADD = sys.argv[1]

#---    Paths
path_WEAP = r'C:\Users\vagrant\Documents\WEAP Areas\SyntheticProblem_WEAPMODFLOW'
path_model = os.path.join(path_WEAP, 'MODFLOW_model')
path_init_model = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\MODFLOW_model\MODFLOW_model_vinit'
path_nwt_exe = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\MODFLOW-NWT_1.2.0\bin\MODFLOW-NWT_64.exe'
path_GIS = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\GIS'    
path_output = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\MODFLOW_NewModel_DPSO\output'         # Need full path for WEAP Export
path_obs_data = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\ObservedData'

#---    Initial matriz
HP = ['kx', 'sy'] 
initial_shape_HP = gpd.read_file(path_GIS + '/Elements_initial_unique_value.shp')
active_matriz = initial_shape_HP['Active'].to_numpy().reshape((84,185))             # Matrix of zeros and ones that allows maintaining active area

n = 1                                                           # Population size

k_shape_1 = (20,20)
k_shape_2 = (5,5)
k_shape_3 = (10,10)
k_shape_4 = (5,5)
k_shape_5 = (10,10)

n_var_1 = reduce(lambda x,y: x*y, k_shape_1)
n_var_2 = reduce(lambda x,y: x*y, k_shape_2)
n_var_3 = reduce(lambda x,y: x*y, k_shape_3)
n_var_4 = reduce(lambda x,y: x*y, k_shape_4)
n_var_5 = reduce(lambda x,y: x*y, k_shape_5)
n_var = 2 * (n_var_1 + n_var_2 + n_var_3 + n_var_4 + n_var_5)    # Number of variables
print (n_var)

lb_kx, lb_sy = 0, 0
ub_1_kx, ub_2_kx, ub_3_kx, ub_4_kx, ub_5_kx = 0.050, 0.025, 0.040, 0.040, 0.040
ub_1_sy, ub_2_sy, ub_3_sy, ub_4_sy, ub_5_sy = 0.025, 0.015, 0.050, 0.040, 0.040

l_bounds = np.concatenate((np.around(np.repeat(lb_kx, n_var_1),4), np.around(np.repeat(lb_sy, n_var_1),4), np.around(np.repeat(lb_kx, n_var_2),4), 
                           np.around(np.repeat(lb_sy, n_var_2),4), np.around(np.repeat(lb_kx, n_var_3),4), np.around(np.repeat(lb_sy, n_var_3),4), 
                           np.around(np.repeat(lb_kx, n_var_4),4), np.around(np.repeat(lb_sy, n_var_4),4), np.around(np.repeat(lb_kx, n_var_5),4), 
                           np.around(np.repeat(lb_sy, n_var_5),4)), axis = 0)
u_bounds = np.concatenate((np.around(np.repeat(ub_1_kx, n_var_1),4), np.around(np.repeat(ub_1_sy, n_var_1),4), np.around(np.repeat(ub_2_kx, n_var_2),4), 
                           np.around(np.repeat(ub_2_sy, n_var_2),4), np.around(np.repeat(ub_3_kx, n_var_3),4), np.around(np.repeat(ub_3_sy, n_var_3),4),                 
                           np.around(np.repeat(ub_4_kx, n_var_4),4), np.around(np.repeat(ub_4_sy, n_var_4),4), np.around(np.repeat(ub_5_kx, n_var_5),4), 
                           np.around(np.repeat(ub_5_sy, n_var_5),4)), axis = 0) 

#---    Initial Sampling (Latyn Hypercube)
class Particle:
    def __init__(self,x,v,y):
        self.x = x                      # X represents the kernels
        self.v = v                      # initial velocity = zeros
        self.y = y
        self.x_best = np.copy(x)                 
        self.y_best = y

sample_scaled = get_sampling_LH(n_var, n, l_bounds, u_bounds)
pob = Particle(sample_scaled[0],np.around(np.array([0]*(n_var)),4),10000000000)

y_init = Run_WEAP_MODFLOW(path_output, str(0), initial_shape_HP, HP, pob.x, n_var_1, n_var_2, n_var_3, n_var_4, n_var_5, n_var, 
                          k_shape_1, k_shape_2, k_shape_3, k_shape_4, k_shape_5, active_matriz, path_init_model, path_model, path_nwt_exe, 
                          path_obs_data)


#gbest = send_request_py(IP_SERVER_ADD, y_init, pob.x)           # Update global particle

