# -*- coding: utf-8 -*-

#---    Packages
import h5py
import os
import pandas as pd
import geopandas as gpd
import numpy as np
from sklearn.metrics import mean_squared_error
import math
from functools import reduce
import warnings
warnings.filterwarnings('ignore')

#---    Required info
HP = ['kx', 'sy']
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

#---    Particle
class Particle:
    def __init__(self,y):                     # initial velocity = zeros
        self.y = y
pob = Particle(10000000000)

path_output = r'D:\PaperI_Results\Sensitivity Analysis - Hyperparameters'
path_obs_data = r'C:\Users\aimee\Desktop\Github\MODFLOW_Calibration\data\ObservedData'

#---    Functions used to estimate pob.y
def get_data(path,skr):
    df_data = pd.read_csv(path, skiprows = skr)
    df_data = df_data.set_index('Branch')
    df_data = df_data.set_index(pd.to_datetime(df_data.index))
    df_data = df_data.iloc[36:,:]
    return df_data

def get_eliminate_zeros(lista):
    position = 0
    while position < len(lista):
        if lista[position] == 0.000001728:
            lista.pop(position)
        else:
            position += 1
    return lista 

#---    Evaluate "Subject to" bounds
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

def get_HP(Shape_HP, variable):
    rows = Shape_HP["ROW"].max()
    columns = Shape_HP["COLUMN"].max()

    matriz = np.zeros((rows,columns))
    for i in range(0,len(Shape_HP['ROW'])):
        matriz[Shape_HP['ROW'][i]-1][Shape_HP['COLUMN'][i]-1] = Shape_HP[variable][i]
    return matriz

#---    EXECUTIONS
algorithm = 'ADPSO-CL'                   # or 'ADDE-CL'
variation = 'var3'                       # or 'var2', 'var3'
experiment = 'E2'                        # or 'E2', 'E3'
vm = 18                                   # 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21
FINAL_ITERATION = 201                     # en vm3 es 41 or 201
path_out = os.path.join(path_output, str(algorithm), str(variation), str(experiment), "vm" + str(vm))

iteration = list(range(FINAL_ITERATION)) # 

#---    Create iteration register file
with h5py.File('DPSO_historial_vm' + str(vm) + '.h5', 'w') as f:
    iter_h5py = f.create_dataset("iteration", (201, 1))
    pob_y_h5py = f.create_dataset("pob_y", (201, 1))
f.close()

for b in iteration:
    dir_iteration = os.path.join(path_out, "iter_"+str(b))
    new_shape_HP = gpd.read_file(os.path.join(dir_iteration, 'Elements_iter_' + str(b) + '.shp'))

    #---    Well analysis
    obs_well = get_data(os.path.join(path_obs_data, 'Wells_observed.csv'), 3)
    ow = obs_well.columns

    sim_well = get_data(os.path.join(dir_iteration, f"iter_{str(b)}_Wells_simulation.csv"), 3)

    g_srmse_well = 0
    srmse_well = 0
    for i in ow:
        if i == "OW51" or i == "OW87" or i == "OW97" or i == "OW100" or i == "OW157" or i == "OW167" or i == "OW181" or i == "OW188" or i == "OW233" or i == "OW234" or i == "OW235":
            g = 0.8
        else:
            g = 0.8

        mse_well = mean_squared_error(obs_well[i], sim_well[i])
        rmse_well = math.sqrt(mse_well)
        g_rmse_well = g * rmse_well

        srmse_well += rmse_well
        g_srmse_well += g_rmse_well
        
    #---    Streamflow analysis
    df_q = pd.read_csv(os.path.join(dir_iteration, f"iter_{str(b)}_Streamflow_gauges.csv"), skiprows = 3)
    df_q = df_q.set_index('Statistic')
    df_q = df_q.set_index(pd.to_datetime(df_q.index))
    df_q = df_q.iloc[36:,:]

    df_q_obs = get_data(os.path.join(path_obs_data, 'StreamflowGauges_KPR_vf.csv'), 2)
    
    mse_q = mean_squared_error(df_q_obs['Observed'], df_q['Modeled'])
    rmse_q = math.sqrt(mse_q)

    #---    Subject to
    kx_min = 0.280
    kx_max = 67.056
    sy_min = 0.01
    sy_max = 0.1282

    for i in HP:
        globals()["vector_" + str(i)] = get_HP(new_shape_HP, str(i)).flatten()
        globals()["vector_modif_" + str(i)] = get_eliminate_zeros(globals()["vector_" + str(i)].tolist())
        globals()["P_" + str(i)] = get_evaluate_st_bounds((locals()[str(i) + "_min"]), (locals()[str(i) + "_max"]), globals()["vector_modif_" + str(i)])

    #---    Total Objective Function
    g2 = 0.6
    g3 = 0.6

    of = g_srmse_well + g2*rmse_q + g3*(P_kx + P_sy)
    print(vm, b, of)

    pob.y = of

    #---    Iteration register
    with h5py.File('DPSO_historial_vm' + str(vm) + '.h5', 'a') as f:
        f["iteration"][b] = b
        f["pob_y"][b] = pob.y
    f.close()