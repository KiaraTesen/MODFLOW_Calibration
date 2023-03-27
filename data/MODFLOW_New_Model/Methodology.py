# -*- coding: utf-8 -*-

#---    Packages
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from functools import reduce
from scipy import signal
import flopy.modflow as fpm
import shutil

import win32com.client as win32

from sklearn.metrics import mean_squared_error
import math

#---    Paths
path_WEAP = r'C:\Users\Francisco Suárez P\Documents\WEAP Areas\SyntheticProblem_WEAPMODFLOW'
path_model = r'..\MODFLOW_Model'
path_nwt_exe = r'..\MODFLOW-NWT_1.2.0\bin\MODFLOW-NWT_64.exe'
path_GIS = r'..\GIS'
path_output = r'C:\Users\Francisco Suárez P\Desktop\GitHub - KT\MODFLOW_Calibration\data\output' # Necesita ruta completa por WEAP Export
path_obs_data = r'..\ObservedData'

iteration = 1
dir_iteration = os.path.join(path_output, "iter_" + str(iteration))
if not os.path.isdir(dir_iteration):
    os.mkdir(dir_iteration)

#-------------------------------------------------------------
#---    Modification of Hydraulic Properties - MODFLOW    ----
#-------------------------------------------------------------
variables = ['kx', 'kz', 'sy']

#---    Visualization of the matriz
def get_image_matriz(matriz, variable, path_out):
    fig=plt.figure(figsize = (16,8))
    ax = plt.axes()
    im = ax.imshow(matriz)
    plt.title(variable)
    plt.xlabel('Column')
    plt.ylabel('Row')
    cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
    plt.colorbar(im, cax=cax)
    plt.savefig(path_out)
    
#---    Generate new shape of HP
def get_HP(Shape_HP, variable, active_matriz):
    rows = Shape_HP["ROW"].max()
    columns = Shape_HP["COLUMN"].max()

    #---    Particle Swarm Optimization (PSO)
    kernel_shape = (5,5)
    n_kernels = 1
    n_hp = 3
    n_var = reduce(lambda x,y: x*y, kernel_shape)*n_kernels*n_hp

    kernel = np.random.uniform(0.9, 1.1, reduce(lambda x,y: x*y, kernel_shape)).reshape(kernel_shape)

    matriz = np.zeros((rows,columns))
    for i in range(0,len(Shape_HP['ROW'])):
        matriz[Shape_HP['ROW'][i]-1][Shape_HP['COLUMN'][i]-1] = Shape_HP[variable][i] # AQUÍ HACER LA OPERACION

        #---    Convolution
        new_matriz = signal.convolve2d(matriz, kernel, boundary = 'symm', mode = 'same')
        new_matriz = new_matriz * active_matriz

    return new_matriz

#---    Initial matriz
initial_shape_HP = gpd.read_file(path_GIS + '/Elements_init.shp') # El shape que se use depende del mejor resultado (?)
active_matriz = initial_shape_HP['Active'].to_numpy().reshape((84,185))

for k in variables:
    locals()["init_matriz_" + str(k)] = initial_shape_HP[k].to_numpy().reshape((84,185))
    get_image_matriz(locals()["init_matriz_" + str(k)], str(k), os.path.join(path_GIS, str(k) +'.png'))
    plt.clf()

#---    Modified matriz
new_shape_HP = initial_shape_HP
for m in variables:
    locals()["matriz_" + str(m)] = get_HP(initial_shape_HP, str(m), active_matriz)
    get_image_matriz(locals()["matriz_" + str(m)], str(m), os.path.join(dir_iteration, str(m) +'.png'))
    plt.clf()

    locals()["vector_" + str(m)] = locals()["matriz_" + str(m)].flatten()
    new_shape_HP[m] = locals()["vector_" + str(m)]

matriz_ss = matriz_sy/100
vector_ss = matriz_ss.flatten()
new_shape_HP['ss'] = vector_ss

new_shape_HP.to_file(os.path.join(dir_iteration, 'Elements_iter_' + str(iteration) + '.shp'))

"""
#-----------------------------------------
#---    New native files - MODFLOW    ----
#-----------------------------------------

model = fpm.Modflow.load(path_model + '/SyntheticAquifer_NY.nam', version = 'mfnwt', exe_name = path_nwt_exe)
model.write_input()
model.remove_package("UPW")
upw = fpm.ModflowUpw(model = model, laytyp=1, layavg=0, chani=-1.0, layvka=0, laywet=0, hdry=-888, iphdry=1, hk=matriz_kx, hani=1.0, vka=matriz_kz, ss=matriz_ss, sy=matriz_sy, extension='upw')
upw.write_file()
model.run_model()

#----------------------------------------
#---    Move native files to WEAP    ----
#----------------------------------------

path_MODFLOW_WEAP = os.path.join(path_WEAP, 'ModflowModel')
get_old_files = os.listdir(path_MODFLOW_WEAP)
get_new_files = os.listdir(os.getcwd())

#---    Delete old files
for g in get_old_files:
    try:
        os.remove(os.path.join(path_MODFLOW_WEAP, g))
    except:
        print('No hay archivos')

#---    Move new files
for h in get_new_files:
    if h == 'Methodology.py':
        pass
    else:
        shutil.copy(os.path.join(os.getcwd(), h), os.path.join(path_MODFLOW_WEAP, h))

#-------------------------------------
#---    Run WEAP-MODFLOW model    ----
#-------------------------------------

WEAP = win32.Dispatch("WEAP.WEAPApplication")
WEAP.ActiveArea = "SyntheticProblem_WEAPMODFLOW"
WEAP.ActiveScenario = WEAP.Scenarios("Current Accounts")
WEAP.Calculate()

#---    Export results
favorites = pd.read_excel("../Favorites_WEAP.xlsx")

for i,j in zip(favorites["BranchVariable"],favorites["WEAP Export"]):
    WEAP.LoadFavorite(i)
    WEAP.ExportResults(os.path.join(dir_iteration, f"iter_{str(iteration)}_{j}.csv"), True, True, True, False, False)
"""
#---------------------------------
#---    Objective Function    ----
#---------------------------------

def get_data(path,skr):
    df_data = pd.read_csv(path, skiprows = skr)
    df_data = df_data.set_index('Branch')
    df_data = df_data.set_index(pd.to_datetime(df_data.index))
    df_data = df_data.iloc[36:,:]
    return df_data

#---    Well analysis
obs_well = get_data(os.path.join(path_obs_data, 'Wells_observed.csv'), 3)
ow = obs_well.columns

sim_well = get_data(os.path.join(dir_iteration, f"iter_{str(iteration)}_Wells_simulation.csv"), 3)

srmse_well = 0
for i in ow:
    mse_well = mean_squared_error(obs_well[i], sim_well[i])
    rmse_well = math.sqrt(mse_well)
    #print(f"RMSE - well {i}: {rmse_well}")
    srmse_well += rmse_well
#print(f"SRMSE - well: {srmse_well}")

#---    Streamflow analysis
df_q = pd.read_csv(os.path.join(dir_iteration, f"iter_{str(iteration)}_Streamflow_gauges.csv"), skiprows = 3)
mse_q = mean_squared_error(df_q['Observed'], df_q['Modeled'])
rmse_q = math.sqrt(mse_q)
#print(f"SRMSE - q: {rmse_q}")

#---    Subject to
kx_min = 0.280
kx_max = 67.056
sy_min = 0.0074
sy_max = 0.1282

def get_eliminate_zeros(lista):
    position = 0
    while position < len(lista):
        if lista[position] == 0:
            lista.pop(position)
        else:
            position += 1
    return lista 

def get_evaluate_st_bounds(min_v, max_v, vector_modif):
    if min_v > min(vector_modif):
        P_min = min_v - min(vector_modif)
    else:
        P_min = 0

    if max_v < max(vector_modif):
        P_max = max(vector_modif) - max_v
    else:
        P_max = 0
    return P_min + P_max

for n in variables:
    if n == 'kz':
        pass
    else:
        locals()["vector_modif_" + str(n)] = get_eliminate_zeros(locals()["vector_" + str(n)].tolist())
        locals()["P_" + str(n)] = get_evaluate_st_bounds((locals()[str(n) + "_min"]), (locals()[str(n) + "_max"]), locals()["vector_modif_" + str(n)])

#---    Total Objective Function
gw = 0.8
gq = 1 - gw
gk = 0.8
gs = 1 - gk

of = gw*srmse_well + gq*rmse_q + gk*P_kx + gs*P_sy
print(f"Objective function: {of}")


