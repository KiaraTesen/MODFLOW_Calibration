# -*- coding: utf-8 -*-

#---    Packages
from Functions import *
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from functools import reduce
import time
import sys
import warnings
warnings.filterwarnings('ignore')

#---    Paths
path_WEAP = r'C:\Users\vagrant\Documents\WEAP Areas\SyntheticProblem_WEAPMODFLOW'
path_model = os.path.join(path_WEAP, 'MODFLOW_model')
path_nwt_exe = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\MODFLOW-NWT_1.2.0\bin\MODFLOW-NWT_64.exe'
path_GIS = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\GIS'    
path_output = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\output'             # Need full path for WEAP Export
path_obs_data = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\ObservedData'

#---    Iteration register
all_lines = []
with open('log_iteration.txt') as f:
    for line in f:
      all_lines.append(line.replace("\n",""))

#---    Initial matriz
HP = ['kx', 'sy'] 
initial_shape_HP = gpd.read_file(path_GIS + '/Elements_initial.shp')            
active_matriz = initial_shape_HP['Active'].to_numpy().reshape((84,185))                 # Matrix of zeros and ones that allows maintaining active area

for k in HP:
    locals()["init_matriz_" + str(k)] = initial_shape_HP[k].to_numpy().reshape((84,185))
    get_image_matriz(locals()["init_matriz_" + str(k)], str(k), os.path.join(path_GIS, str(k) +'.png'))
    plt.clf()

n = 1                                                           # Population size

kernel_shape_1_kx = (5,5)
kernel_shape_1_sy = (5,5)
kernel_shape_2_kx = (3,3)
kernel_shape_2_sy = (3,3)

n_var_1_kx = reduce(lambda x,y: x*y, kernel_shape_1_kx)     
n_var_1_sy = reduce(lambda x,y: x*y, kernel_shape_1_sy)              
n_var_2_kx = reduce(lambda x,y: x*y, kernel_shape_2_kx)
n_var_2_sy = reduce(lambda x,y: x*y, kernel_shape_2_sy)
n_var = n_var_1_kx + n_var_1_sy + n_var_2_kx + n_var_2_sy       # Problem dimension

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
    def __init__(self,x):
        self.x = x 
        self.y = 1000000000

sample_scaled = get_sampling_LH(n_var, n, l_bounds, u_bounds)
pob = Particle(sample_scaled[0])

of_init = Run_WEAP_MODFLOW(path_output, str(0), initial_shape_HP, HP, pob.x, n_var_1_kx, n_var_1_sy, n_var_2_kx, n_var_2_sy, n_var, kernel_shape_1_kx, kernel_shape_1_sy, 
                           kernel_shape_2_kx, kernel_shape_2_sy, active_matriz, path_model, path_nwt_exe, path_obs_data)
pob.y = of_init

#---    Zero solution
print(pob.x, pob.y)

#---    Save objective function zero value
file_object = open("log_iteration.txt", 'a')
file_object.write(f"{'Iteracion inicial: 0'}\n")
file_object.write(f"{'Pob.x: ', pob.x}\n")
file_object.write(f"{'Pob.y: ', pob.y}\n")
file_object.close()

#---    Differential Evolution
maxiter = 10
vms = 20        # Number of VMs we use for the experiment

α = 0.8         # Step size [0, 0.9] - [0.45, 0.95]
pc = 0.9        # Crossover probability - [0.1, 0.8]

id_vm = ######## FUNCION PARA OBTENER EL ID #############
for m in range(maxiter):
    print("Iter #:" , m+1)
    time.sleep(1)

    xi = pob.x                                                # Pick candidate solution

    ids_vms = np.linspace(0, vms - 1, vms, dtype = int)       # ids_vms vector containing the indexes of the all other candidate solution but xi
    ids_vms = np.where(ids_vms != id_vm)
    ids_vms = np.asarray(ids_vms)[0]

    # Randomly pick 3 candidate solution using indexes ids_vms
    xa , xb , xc = np.random.choice(ids_vms, 3, replace = False)    #### TIENE QUE REGRESAR pob.x
    V1 = xa
    V2 = xb
    Vb = xc
    
    Vd = V1 - V2                                # The difference vector        
    Vm = Vb + α*Vd                              # The mutant vector         
    Vm = np.clip(Vm,l_bounds,u_bounds)          # make sure the mutant vector is in [lb,ub]
    
    # Create a trial vector by recombination
    Vt = np.zeros(n_var)
    rj = np.random.rand()                       # index of the dimension that will under crossover regardless of pc
    for id_dim in range(n_var):
        rc = np.random.rand()
        if rc < pc or id_dim == rj:
            Vt[id_dim] = Vm[id_dim]             # Perform recombination
        else:
            Vt[id_dim] = xi[id_dim]             # copy from Vb
    
    # Obtain the OF of the trial vector
    vt_of = Run_WEAP_MODFLOW(path_output, str(m+1), initial_shape_HP, HP, Vt, n_var_1_kx, n_var_1_sy, n_var_2_kx, n_var_2_sy, n_var, kernel_shape_1_kx, kernel_shape_1_sy, 
                             kernel_shape_2_kx, kernel_shape_2_sy, active_matriz, path_model, path_nwt_exe, path_obs_data)

    # Select the id_pop individual for the next generation
    if vt_of < pob.y:
        pob.x = Vt
        pob.y = vt_of

    file_object = open("log_iteration.txt", 'a')
    file_object.write(f"{'Iteracion: ', str(m+1)}\n")
    file_object.write(f"{'Pob.x: ', pob.x}\n")
    file_object.write(f"{'Pob.y: ', pob.y}\n")
    file_object.close()