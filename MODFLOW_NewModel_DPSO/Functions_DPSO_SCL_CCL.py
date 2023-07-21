import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.qmc import LatinHypercube,scale
from scipy import signal
import pandas as pd
import os
import flopy.modflow as fpm
import shutil
import win32com.client as win32
from sklearn.metrics import mean_squared_error
import math
import warnings
warnings.filterwarnings('ignore')

#---    Visualization of the matriz -
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

#---    Sampling by Latin Hypecube
def get_sampling_LH(n_var, n, l_bounds, u_bounds):
    engine = LatinHypercube(d=n_var)
    sample = engine.random(n=n)
    sample_scaled = scale(sample, l_bounds, u_bounds)
    return np.around(sample_scaled, 4)

#---    Modification 1 of HP
def get_pre_HP(Shape_HP, new_Shape, variable, particle, begin, end):
    count = 0
    x = particle[begin : end]
    for i in range(len(new_Shape)):
         if new_Shape[variable][i] == 0:
             pass
         else:
            #print(count, x[count], Shape_HP[variable][i])
            new_Shape[variable][i] = round(x[count] * Shape_HP[variable][i],4)
            count += 1
        
    rows = new_Shape["ROW"].max()
    columns = new_Shape["COLUMN"].max()

    matriz = np.zeros((rows,columns))
    for i in range(0,len(new_Shape['ROW'])):
        matriz[new_Shape['ROW'][i]-1][new_Shape['COLUMN'][i]-1] = new_Shape[variable][i] 
    return matriz

#---    Modification 2 of HP
def get_HP(Shape_HP, variable, active_matriz, decimals, kernel):
    rows = Shape_HP["ROW"].max()
    columns = Shape_HP["COLUMN"].max()

    matriz = np.zeros((rows,columns))
    for i in range(0,len(Shape_HP['ROW'])):
        matriz[Shape_HP['ROW'][i]-1][Shape_HP['COLUMN'][i]-1] = Shape_HP[variable][i] 

        #---    Convolution
        new_matriz = signal.convolve2d(matriz, kernel, boundary = 'symm', mode = 'same')
        new_matriz = np.around(new_matriz * active_matriz, decimals = decimals)
    return new_matriz

#---    Order data
def get_data(path,skr):
    df_data = pd.read_csv(path, skiprows = skr)
    df_data = df_data.set_index('Branch')
    df_data = df_data.set_index(pd.to_datetime(df_data.index))
    df_data = df_data.iloc[36:,:]
    return df_data

def get_eliminate_zeros(lista):
    position = 0
    while position < len(lista):
        if lista[position] == 0:
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

def Run_WEAP_MODFLOW(path_output, iteration, initial_shape_HP, HP, active_cells, sample_scaled, n_var_1, n_var_2, n_var_3, n_var, 
                     k_shape_1, k_shape_2, k_shape_3, k_shape_4, active_matriz, path_init_model, path_model, path_nwt_exe, 
                     path_obs_data):

    dir_iteration = os.path.join(path_output, "iter_" + str(iteration))
    if not os.path.isdir(dir_iteration):
        os.mkdir(dir_iteration)
    
    #--------------------------
    #---    Run MODFLOW    ----
    #--------------------------
    #---    Modified matriz
    pre_shape_HP = initial_shape_HP.copy()
    shape_k1_HP = initial_shape_HP.copy()
    new_shape_HP = initial_shape_HP.copy()

    for m in HP:
        if m == "kx":
            begin = 0
            end = active_cells
        elif m == "sy":
            begin = active_cells
            end = active_cells * 2
        globals()["matriz_pre_" + str(m)] = get_pre_HP(initial_shape_HP, pre_shape_HP, str(m), sample_scaled, begin, end)
        get_image_matriz(globals()["matriz_pre_" + str(m)], str(m), os.path.join(dir_iteration, 'Pre_' + str(m) +'.png'))
        plt.clf

        # CONVOLUTIONAL LAYERS
        decimals_kx = 4
        decimals_sy = 4

        # First kernel
        kernel_1_kx = sample_scaled[int(active_cells * 2):int(active_cells * 2 + n_var_1)].reshape(k_shape_1)
        kernel_1_sy = sample_scaled[int(active_cells * 2 + n_var_1):int(active_cells * 2 + n_var_1 + n_var_2)].reshape(k_shape_2)

        globals()["matriz_1_" + str(m)] = get_HP(pre_shape_HP, str(m), active_matriz, locals()["decimals_" + str(m)], locals()["kernel_1_" + str(m)])
        get_image_matriz(globals()["matriz_1_" + str(m)], str(m), os.path.join(dir_iteration, '1_' + str(m) +'.png'))
        plt.clf()
        globals()["vector_1_" + str(m)] = globals()["matriz_1_" + str(m)].flatten()
        shape_k1_HP[m] = globals()["vector_1_" + str(m)]

        # Second kernel
        kernel_2_kx = sample_scaled[int(active_cells * 2 + n_var_1 + n_var_2):int(active_cells * 2 + n_var_1 + n_var_2 + n_var_3)].reshape(k_shape_3)
        kernel_2_sy = sample_scaled[int(active_cells * 2 + n_var_1 + n_var_2 + n_var_3):int(n_var)].reshape(k_shape_4)
        
        globals()["matriz_" + str(m)] = get_HP(shape_k1_HP, str(m), active_matriz, locals()["decimals_" + str(m)], locals()["kernel_2_" + str(m)])
        get_image_matriz(globals()["matriz_" + str(m)], str(m), os.path.join(dir_iteration, 'Final_' + str(m) +'.png'))
        plt.clf()
        globals()["vector_" + str(m)] = globals()["matriz_" + str(m)].flatten()
        new_shape_HP[m] = globals()["vector_" + str(m)]

    #---    Other variables that MODFLOW require
    matriz_kz = matriz_kx/10
    matriz_ss = matriz_sy/100
    new_shape_HP['kz'] = matriz_kz.flatten()
    new_shape_HP['ss'] = matriz_ss.flatten()
    new_shape_HP.to_file(os.path.join(dir_iteration, 'Elements_iter_' + str(iteration) + '.shp'))
