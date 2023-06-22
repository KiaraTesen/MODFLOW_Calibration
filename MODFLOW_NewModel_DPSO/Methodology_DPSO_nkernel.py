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

kernel_shape_1_kx = (10,10)
kernel_shape_1_sy = (10,10)
kernel_shape_2_kx = (5,5)
kernel_shape_2_sy = (5,5)
kernel_shape_3_kx = (10,10) #
kernel_shape_3_sy = (10,10) #
kernel_shape_4_kx = (5,5) #
kernel_shape_4_sy = (5,5) #
kernel_shape_5_kx = (10,10) #
kernel_shape_5_sy = (10,10) #

n_var_1_kx = reduce(lambda x,y: x*y, kernel_shape_1_kx)
n_var_1_sy = reduce(lambda x,y: x*y, kernel_shape_1_sy)
n_var_2_kx = reduce(lambda x,y: x*y, kernel_shape_2_kx)
n_var_2_sy = reduce(lambda x,y: x*y, kernel_shape_2_sy)
n_var_3_kx = reduce(lambda x,y: x*y, kernel_shape_3_kx) #
n_var_3_sy = reduce(lambda x,y: x*y, kernel_shape_3_sy) #
n_var_4_kx = reduce(lambda x,y: x*y, kernel_shape_4_kx) #
n_var_4_sy = reduce(lambda x,y: x*y, kernel_shape_4_sy) #
n_var_5_kx = reduce(lambda x,y: x*y, kernel_shape_5_kx) #
n_var_5_sy = reduce(lambda x,y: x*y, kernel_shape_5_sy) #
n_var = n_var_1_kx + n_var_1_sy + n_var_2_kx + n_var_2_sy + n_var_3_kx + n_var_3_sy + n_var_4_kx + n_var_4_sy + n_var_5_kx + n_var_5_sy     # Number of variables

lb_1_kx, ub_1_kx = 0, 0.050              # [0.015 - 3.482]
lb_1_sy, ub_1_sy = 0, 0.025               # [0.05 - 0.99]
lb_2_kx, ub_2_kx = 0, 0.025
lb_2_sy, ub_2_sy = 0, 0.015
lb_3_kx, ub_3_kx = 0, 0.040
lb_3_sy, ub_3_sy = 0, 0.050
lb_4_kx, ub_4_kx = 0, 0.040
lb_4_sy, ub_4_sy = 0, 0.040
lb_5_kx, ub_5_kx = 0, 0.040
lb_5_sy, ub_5_sy = 0, 0.040

l_bounds = np.concatenate((np.around(np.repeat(lb_1_kx, n_var_1_kx),4), np.around(np.repeat(lb_1_sy, n_var_1_sy),4),
                           np.around(np.repeat(lb_2_kx, n_var_2_kx),4), np.around(np.repeat(lb_2_sy, n_var_2_sy),4),
                           np.around(np.repeat(lb_3_kx, n_var_3_kx),4), np.around(np.repeat(lb_3_sy, n_var_3_sy),4),
                           np.around(np.repeat(lb_4_kx, n_var_4_kx),4), np.around(np.repeat(lb_4_sy, n_var_4_sy),4),
                           np.around(np.repeat(lb_5_kx, n_var_5_kx),4), np.around(np.repeat(lb_5_sy, n_var_5_sy),4)), axis = 0)
u_bounds = np.concatenate((np.around(np.repeat(ub_1_kx, n_var_1_kx),4), np.around(np.repeat(ub_1_sy, n_var_1_sy),4),                 
                           np.around(np.repeat(ub_2_kx, n_var_2_kx),4), np.around(np.repeat(ub_2_sy, n_var_2_sy),4),
                           np.around(np.repeat(ub_3_kx, n_var_3_kx),4), np.around(np.repeat(ub_3_sy, n_var_3_sy),4),                 
                           np.around(np.repeat(ub_4_kx, n_var_4_kx),4), np.around(np.repeat(ub_4_sy, n_var_4_sy),4),
                           np.around(np.repeat(ub_5_kx, n_var_5_kx),4), np.around(np.repeat(ub_5_sy, n_var_5_sy),4)), axis = 0) 

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

y_init = Run_WEAP_MODFLOW(path_output, str(0), initial_shape_HP, HP, pob.x, n_var_1_kx, n_var_1_sy, n_var_2_kx, n_var_2_sy, n_var_3_kx, 
                          n_var_3_sy, n_var_4_kx, n_var_4_sy, n_var_5_kx, n_var_5_sy, n_var, kernel_shape_1_kx, kernel_shape_1_sy, kernel_shape_2_kx, kernel_shape_2_sy, 
                          kernel_shape_3_kx, kernel_shape_3_sy, kernel_shape_4_kx, kernel_shape_4_sy, kernel_shape_5_kx, kernel_shape_5_sy, active_matriz, path_init_model, path_model, 
                          path_nwt_exe, path_obs_data)


#gbest = send_request_py(IP_SERVER_ADD, y_init, pob.x)           # Update global particle

