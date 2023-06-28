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
import sys
from request_server.request_server import send_request_py
import warnings
warnings.filterwarnings('ignore')

IP_SERVER_ADD = sys.argv[1]

#---    Paths
path_WEAP = r'C:\Users\vagrant\Documents\WEAP Areas\SyntheticProblem_WEAPMODFLOW'
path_model = os.path.join(path_WEAP, 'MODFLOW_model')
path_init_model = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\MODFLOW_model\MODFLOW_model_vinit'
path_nwt_exe = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\MODFLOW-NWT_1.2.0\bin\MODFLOW-NWT_64.exe'
path_GIS = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\GIS'    
path_output = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\MODFLOW_NewModel_DPSO\output'         # Need full path for WEAP Export
path_obs_data = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\ObservedData'

#---    Iteration register
all_lines = []
with open('log_iteration.txt') as f:
    for line in f:
      all_lines.append(line.replace("\n",""))

#---    Initial matriz
HP = ['kx', 'sy'] 
initial_shape_HP = gpd.read_file(path_GIS + '/Elements_initial.shp')
active_matriz = initial_shape_HP['Active'].to_numpy().reshape((84,185))             # Matrix of zeros and ones that allows maintaining active area

n = 1                                                           # Population size

kernel_shape_1_kx = (5,5)
kernel_shape_1_sy = (5,5)
kernel_shape_2_kx = (3,3)
kernel_shape_2_sy = (3,3)

n_var_1_kx = reduce(lambda x,y: x*y, kernel_shape_1_kx)     
n_var_1_sy = reduce(lambda x,y: x*y, kernel_shape_1_sy)              
n_var_2_kx = reduce(lambda x,y: x*y, kernel_shape_2_kx)
n_var_2_sy = reduce(lambda x,y: x*y, kernel_shape_2_sy)
n_var = n_var_1_kx + n_var_1_sy + n_var_2_kx + n_var_2_sy       # Number of variables

lb_1_kx, ub_1_kx = 0, 0.2               # [0.85 - 1.01]
lb_1_sy, ub_1_sy = 0, 0.2               # [0.05 - 0.99]
lb_2_kx, ub_2_kx = 0, 0.12
lb_2_sy, ub_2_sy = 0, 0.1

l_bounds = np.concatenate((np.around(np.repeat(lb_1_kx, n_var_1_kx),4), np.around(np.repeat(lb_1_sy, n_var_1_sy),4),                      # First and third block: Kx
                           np.around(np.repeat(lb_2_kx, n_var_2_kx),4), np.around(np.repeat(lb_2_sy, n_var_2_sy),4)), axis = 0)           # Second and fourth block: Sy
u_bounds = np.concatenate((np.around(np.repeat(ub_1_kx, n_var_1_kx),4), np.around(np.repeat(ub_1_sy, n_var_1_sy),4),                 
                           np.around(np.repeat(ub_2_kx, n_var_2_kx),4), np.around(np.repeat(ub_2_sy, n_var_2_sy),4)), axis = 0) 

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

y_init = Run_WEAP_MODFLOW(path_output, str(0), initial_shape_HP, HP, pob.x, n_var_1_kx, n_var_1_sy, n_var_2_kx, n_var_2_sy, n_var, kernel_shape_1_kx, kernel_shape_1_sy, 
                          kernel_shape_2_kx, kernel_shape_2_sy, active_matriz, path_init_model, path_model, path_nwt_exe, path_obs_data)
pob.y = y_init
pob.y_best = y_init

gbest = send_request_py(IP_SERVER_ADD, y_init, pob.x)           # Update global particle

#---    Save objective function value
file_object = open("log_iteration.txt", 'a')
file_object.write(f"{'Iteracion inicial: 0'}\n")
file_object.write(f"{'Pob.x: ', pob.x}\n")
file_object.write(f"{'Pob.y: ', pob.y}\n")
file_object.write(f"{'Pob.v: ', pob.v}\n")
file_object.write(f"{'Pob.x_best: ', pob.x_best}\n")
file_object.write(f"{'Pob.y_best: ', pob.y_best}\n")
file_object.write(f"{'Gbest: ', gbest}\n")
file_object.close()

#---    PSO
maxiter = 40

α = 0.8                                                    # Cognitive scaling parameter  # 0.8 # 1.49
β = 0.8                                                    # Social scaling parameter     # 0.8 # 1.49
w = 0.5                                                     # inertia velocity
w_min = 0.4                                                 # minimum value for the inertia velocity
w_max = 0.9                                                 # maximum value for the inertia velocity
vMax = np.around(np.multiply(u_bounds-l_bounds,0.4),4)      # Max velocity # De 0.8 a 0.4
vMin = -vMax                                                # Min velocity

for m in range(maxiter):
    time.sleep(1)

    #---    Update particle velocity
    ϵ1,ϵ2 = np.around(np.random.uniform(),4), np.around(np.random.uniform(),4)            # [0, 1]

    pob.v = np.around(np.around(w*pob.v,4) + np.around(α*ϵ1*(pob.x_best - pob.x),4) + np.around(β*ϵ2*(gbest - pob.x),4),4)

    #---    Adjust particle velocity
    index_vMax = np.where(pob.v > vMax)
    index_vMin = np.where(pob.v < vMin)

    if np.array(index_vMax).size > 0:
        pob.v[index_vMax] = vMax[index_vMax]
    if np.array(index_vMin).size > 0:
        pob.v[index_vMin] = vMin[index_vMin]

    #---    Update particle position
    pob.x += pob.v

    #---    Adjust particle position
    index_pMax = np.where(pob.x > u_bounds)
    index_pMin = np.where(pob.x < l_bounds)

    if np.array(index_pMax).size > 0:
        pob.x[index_pMax] = u_bounds[index_pMax]
    if np.array(index_pMin).size > 0:
        pob.x[index_pMin] = l_bounds[index_pMin]

    #---    Evaluate the fitnness function
    y = Run_WEAP_MODFLOW(path_output, str(m+1), initial_shape_HP, HP, pob.x, n_var_1_kx, n_var_1_sy, n_var_2_kx, n_var_2_sy, n_var, kernel_shape_1_kx, kernel_shape_1_sy, 
                         kernel_shape_2_kx, kernel_shape_2_sy, active_matriz, path_init_model, path_model, path_nwt_exe, path_obs_data)
    gbest = send_request_py(IP_SERVER_ADD, y, pob.x)
    
    if y < pob.y_best:
        pob.x_best = np.copy(pob.x)
        pob.y_best = y
        pob.y = y
    else:
        pob.y = y

    #---    Save objective function value
    file_object = open("log_iteration.txt", 'a')
    file_object.write(f"{'Iteracion: ', str(m+1)}\n")
    file_object.write(f"{'Pob.x: ', pob.x}\n")
    file_object.write(f"{'Pob.y: ', pob.y}\n")
    file_object.write(f"{'Pob.v: ', pob.v}\n")
    file_object.write(f"{'Pob.x_best: ', pob.x_best}\n")
    file_object.write(f"{'Pob.y_best: ', pob.y_best}\n")
    file_object.write(f"{'Gbest: ', gbest}\n")
    file_object.close()

    #---    Update the inertia velocity
    w = w_max - (m+1) * ((w_max-w_min)/maxiter)