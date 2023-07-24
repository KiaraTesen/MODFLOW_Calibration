# -*- coding: utf-8 -*-

#---    Packages
from Functions_DPSO_SCL_CCL import *
import geopandas as gpd
import pandas as pd
import numpy as np
import h5py
import matplotlib.pyplot as plt
import os
from functools import reduce
import time
import sys
from request_server.request_server import send_request_py
import warnings
warnings.filterwarnings('ignore')
"""
IP_SERVER_ADD = sys.argv[1]
ITERATION = int(sys.argv[2])
TOTAL_ITERATION = int(sys.argv[3])
FINAL_ITERATION = int(sys.argv[4])

VMS = int(sys.argv[5])
VM = int(sys.argv[6])
"""
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
initial_shape_HP = gpd.read_file(path_GIS + '/Elements_initial_unique_value_v2.shp')   # /Elements_initial_unique_value.shp, /Elements_initial_zones_reduced.shp
active_matriz = initial_shape_HP['Active'].to_numpy().reshape((84,185))             # Matrix of zeros and ones that allows maintaining active area

n = 20                                                           # Population size

active_cells = 7536

k_shape_1 = (5,5)   #HK_1
k_shape_2 = (3,3)   #SY_1
k_shape_3 = (3,3)   #HK_2
k_shape_4 = (2,2)   #SY_2

n_var = active_cells * 2
for k in range(1,5):
    globals()['n_var_' + str(k)] = reduce(lambda x,y: x*y, globals()['k_shape_' + str(k)])
    n_var += globals()['n_var_' + str(k)]
n_var = n_var    # Number of variables
print (n_var)

#---    Create iteration register file
with h5py.File('PRE_DPSO_historial.h5', 'w') as f:
    pob_x_h5py = f.create_dataset("pob_x", (n, n_var))

#---    Bounds
lb_kx, ub_kx = 0.015, 3.8
lb_sy, ub_sy = 0.278, 3.57

lb_1_kx, ub_1_kx = 0.001, 0.1
lb_1_sy, ub_1_sy = 0.365, 0.45
lb_2_kx, ub_2_kx = 0.002, 0.3
lb_2_sy, ub_2_sy = 0.125, 0.15

l_bounds = np.concatenate((np.around(np.repeat(lb_kx, active_cells),4), np.around(np.repeat(lb_sy, active_cells),4), 
                           np.around(np.repeat(lb_1_kx, n_var_1),4), np.around(np.repeat(lb_1_sy, n_var_2),4), 
                           np.around(np.repeat(lb_2_kx, n_var_3),4), np.around(np.repeat(lb_2_sy, n_var_4),4)), axis = 0)
u_bounds = np.concatenate((np.around(np.repeat(ub_kx, active_cells),4), np.around(np.repeat(ub_sy, active_cells),4), 
                           np.around(np.repeat(ub_1_kx, n_var_1),4), np.around(np.repeat(ub_1_sy, n_var_2),4), 
                           np.around(np.repeat(ub_2_kx, n_var_3),4), np.around(np.repeat(ub_2_sy, n_var_4),4)), axis = 0) 

#---    Initial Sampling (Latyn Hypercube)
class Particle:
    def __init__(self,x,v,y):
        self.x = x                      # X represents the kernels
        self.v = v                      # initial velocity = zeros
        self.y = y
        self.x_best = np.copy(x)                 
        self.y_best = y

sample_scaled = get_sampling_LH(n_var, n, l_bounds, u_bounds)
print(sample_scaled)

#---    Iteration register
for i in range(n):
    with h5py.File('Pre_DPSO_historial.h5', 'a') as f:
        f["pob_x"][i] = np.copy(sample_scaled[i])
    f.close()