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

IP_SERVER_ADD = sys.argv[1]
ITERATION = int(sys.argv[2])
TOTAL_ITERATION = int(sys.argv[3])
FINAL_ITERATION = int(sys.argv[4])

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

n = 1                                                           # Population size

active_cells = 7536

k_shape_1 = (5,5)
k_shape_2 = (3,3)

n_var = active_cells
for k in range(1,3):
    globals()['n_var_' + str(k)] = reduce(lambda x,y: x*y, globals()['k_shape_' + str(k)])
    n_var += globals()['n_var_' + str(k)]
n_var = 2 * n_var    # Number of variables
print (n_var)

#---    Bounds
lb_kx, ub_kx = 0.001, 3.9
lb_sy, ub_sy = 0.35, 3.561

lb_1_kx, lb_1_sy = 0.001, 0.05   #0.02, 0.03
lb_2_kx, lb_2_sy = 0.002, 0.09   #0.004
ub_1_kx, ub_1_sy = 0.1, 0.09
ub_2_kx, ub_2_sy = 0.3, 0.22

l_bounds = np.concatenate((np.around(np.repeat(lb_kx, active_cells),4), np.around(np.repeat(lb_sy, active_cells),4), 
                           np.around(np.repeat(lb_1_kx, n_var_1),4), np.around(np.repeat(lb_1_sy, n_var_1),4), 
                           np.around(np.repeat(lb_2_kx, n_var_2),4), np.around(np.repeat(lb_2_sy, n_var_2),4)), axis = 0)
u_bounds = np.concatenate((np.around(np.repeat(ub_kx, active_cells),4), np.around(np.repeat(ub_sy, active_cells),4), 
                           np.around(np.repeat(ub_1_kx, n_var_1),4), np.around(np.repeat(ub_1_sy, n_var_1),4), 
                           np.around(np.repeat(ub_2_kx, n_var_2),4), np.around(np.repeat(ub_2_sy, n_var_2),4)), axis = 0) 

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
######################
if ITERATION == 0:
    #---    Initial Sampling - Pob(0)
    y_init = Run_WEAP_MODFLOW(path_output, str(ITERATION), initial_shape_HP, HP, active_cells, pob.x, n_var_1, n_var_2, n_var, 
                              k_shape_1, k_shape_2, active_matriz, path_init_model, path_model, path_nwt_exe, 
                              path_obs_data)
