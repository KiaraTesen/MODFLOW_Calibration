# -*- coding: utf-8 -*-

#---    Packages
from Functions_DPSO_SCL_CCL import *
import numpy as np
import h5py
import os
from functools import reduce
import warnings
warnings.filterwarnings('ignore')

#---    Initial matriz
n = 35                                                 # Population size: 20, 35, 50

active_cells = 7536
n_var = active_cells * 2
print (n_var)

#---    Create iteration register file
with h5py.File('Pre_DPSO_historial.h5', 'w') as f:
    pob_x_h5py = f.create_dataset("pob_x", (n, n_var))

#---    Bounds
lb_kx, ub_kx = 0.01, 4
lb_sy, ub_sy = 0.30, 5

l_bounds = np.concatenate((np.around(np.repeat(lb_kx, active_cells),4), np.around(np.repeat(lb_sy, active_cells),4)), axis = 0)
u_bounds = np.concatenate((np.around(np.repeat(ub_kx, active_cells),4), np.around(np.repeat(ub_sy, active_cells),4)), axis = 0) 

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

#---    Read file to verify
with h5py.File('Pre_DPSO_historial.h5', 'r') as f:
    x = f["pob_x"][:]
print(x[0])
print(len(x))