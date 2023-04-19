# -*- coding: utf-8 -*-

#---    Packages
from Functions_PSO import *
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from functools import reduce
import time
import warnings
warnings.filterwarnings('ignore')

#---    Paths
path_WEAP = r'C:\Users\Francisco Suárez P\Documents\WEAP Areas\SyntheticProblem_WEAPMODFLOW'
#path_WEAP = r'C:\Users\vagrant\Documents\WEAP Areas\SyntheticProblem_WEAPMODFLOW'
path_model = os.path.join(path_WEAP, 'MODFLOW_model')
path_nwt_exe = r'..\MODFLOW-NWT_1.2.0\bin\MODFLOW-NWT_64.exe'
path_GIS = r'..\GIS'
path_output = r'C:\Users\Francisco Suárez P\Desktop\GitHub - KT\MODFLOW_Calibration\data\output'      
#path_output = r'C:\Users\vagrant\Documents\MODFLOW_Calibration\data\output'         # Necesita ruta completa por WEAP Export
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
    def __init__(self,x,v):
        self.x = x                      # X contiene a los dos kernel
        self.v = v                      # velocidad del muestreo inicial = 0
        self.x_best = x                 # Para muestreo inicial sería X
        self.y_best = 10000000000

n = 1                                                           # Population size
n_kernels = 2
kernel_shape_1 = (5,5)
kernel_shape_2 = (3,3)
n_hp = 2
n_var_1 = reduce(lambda x,y: x*y, kernel_shape_1)*n_hp                 
n_var_2 = reduce(lambda x,y: x*y, kernel_shape_2)*n_hp
n_var = n_var_1 + n_var_2                                       # Number of variables

l_bounds = np.concatenate((np.repeat(0, n_var_1/n_hp), np.repeat(0, n_var_1/n_hp),                      # First and third block: Hydraulic conductivity (K), 0.85 - 
                           np.repeat(0, n_var_2/n_hp), np.repeat(0, n_var_2/n_hp)), axis = 0)           # Second and fourth block: Specific yield (Sy), 0.05   
u_bounds = np.concatenate((np.repeat(0.2, n_var_1/n_hp), np.repeat(0.4, n_var_1/n_hp),                  # First and third block: Hydraulic conductivity (K), 1.01 - 
                           np.repeat(0.1, n_var_2/n_hp), np.repeat(0.2, n_var_2/n_hp)), axis = 0)       # Second and fourth block: Specific yield (Sy), 0.99

sample_scaled = get_sampling_LH(n_var, n, l_bounds, u_bounds)
pob = [Particle(x,np.array([0]*(n_var))) for x in sample_scaled]

x_best = pob[0].x_best
y_best = 100000000000

#---    PSO
maxiter = 3
α = 0.8         # Cognitive scaling parameter # si el error no baja tanto
β = 0.8         # Social scaling parameter
w = 0.5         # inertia velocity
w_min = 0.4     # minimum value for the inertia velocity
w_max = 0.9     # maximum value for the inertia velocity

vMax = np.multiply(u_bounds-l_bounds,0.2)       # Max velocity
vMin = -vMax                                    # Min velocity

start_time = time.time()
iter = 0
for m in range(maxiter):
    df_iter = pd.DataFrame(columns = ['x', 'v', 'x_best', 'y_best'])
    for P in pob:
        #---    Update particle velocity
        ϵ1,ϵ2 = np.random.uniform(), np.random.uniform()            # One value between 0 and 1
        P.v = w*P.v + α*ϵ1*(P.x_best - P.x) + β*ϵ2*(x_best - P.x)

        #---    Adjust particle velocity
        index_vMax = np.where(P.v > vMax)
        index_vMin = np.where(P.v < vMin)

        if np.array(index_vMax).size > 0:
            P.v[index_vMax] = vMax[index_vMax]
        if np.array(index_vMin).size > 0:
            P.v[index_vMin] = vMin[index_vMin]
        
        #---    Update particle position
        P.x += P.v

        #---    Adjust particle position
        index_pMax = np.where(P.x > u_bounds)
        index_pMin = np.where(P.x < l_bounds)

        if np.array(index_pMax).size > 0:
            P.x[index_pMax] = u_bounds[index_pMax]
        if np.array(index_pMin).size > 0:
            P.x[index_pMin] = l_bounds[index_pMin]

        #---    Evaluate the fitnness function
        y = Run_WEAP_MODFLOW(path_output, str(m), initial_shape_HP, HP, P.x, n_var_1, n_var_2, n_var, n_hp, kernel_shape_1, kernel_shape_2, active_matriz, 
                             path_model, path_nwt_exe, path_obs_data)

        if y < y_best:
            x_best = np.copy(P.x)
            P.x_best = np.copy(P.x)
            y_best = y
            P.y_best = y
        elif y < P.y_best:
            P.x_best = np.copy(P.x)
            P.y_best = y

        #---    Registro de resultados por máquina #############
        df_iter.loc[iter,'x'] = P.x
        df_iter.loc[iter,'v'] = P.v
        df_iter.loc[iter,'x_best'] = P.x_best
        df_iter.loc[iter,'y_best'] = P.y_best

        #---    Update the inertia velocity
        w = w_max - m * ((w_max-w_min)/maxiter)
    iter += 1

df_iter.to_csv(os.path.join(path_output, 'df_iter.csv'))
print(y_best)
print("{} segundos".format(time.time() - start_time))