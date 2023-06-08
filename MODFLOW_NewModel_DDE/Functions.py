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

#---    Sampling by Latin Hypecube
def get_sampling_LH(n_var, n, l_bounds, u_bounds):
    engine = LatinHypercube(d=n_var)
    sample = engine.random(n=n)
    sample_scaled = scale(sample, l_bounds, u_bounds)
    return np.around(sample_scaled, 4)

#---    Modification of HP
def get_HP(Shape_HP, variable, active_matriz, decimals, kernel):
    rows = Shape_HP["ROW"].max()
    columns = Shape_HP["COLUMN"].max()

    matriz = np.zeros((rows,columns))
    for i in range(0,len(Shape_HP['ROW'])):
        matriz[Shape_HP['ROW'][i]-1][Shape_HP['COLUMN'][i]-1] = Shape_HP[variable][i] # AQUÍ HACER LA OPERACION

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

def Run_WEAP_MODFLOW(path_output, iteration, initial_shape_HP, HP, sample_scaled, n_var_1_kx, n_var_1_sy, n_var_2_kx, n_var_2_sy, n_var, kernel_shape_1_kx, kernel_shape_1_sy, 
                     kernel_shape_2_kx, kernel_shape_2_sy, active_matriz, path_model, path_nwt_exe, path_obs_data):
    dir_iteration = os.path.join(path_output, "iter_" + str(iteration))
    if not os.path.isdir(dir_iteration):
        os.mkdir(dir_iteration)
    
    #--------------------------
    #---    Run MODFLOW    ----
    #--------------------------
    #---    Modified matriz
    shape_k1_HP = initial_shape_HP
    new_shape_HP = initial_shape_HP

    for m in HP:
        decimals_kx = 4
        decimals_sy = 4
        # First kernel
        kernel_1_kx = sample_scaled[:int(n_var_1_kx)].reshape(kernel_shape_1_kx)
        kernel_1_sy = sample_scaled[int(n_var_1_kx):int(n_var_1_kx + n_var_1_sy)].reshape(kernel_shape_1_sy)
        
        globals()["matriz_1_" + str(m)] = get_HP(initial_shape_HP, str(m), active_matriz, locals()["decimals_" + str(m)], locals()["kernel_1_" + str(m)])
        globals()["vector_1_" + str(m)] = globals()["matriz_1_" + str(m)].flatten()
        shape_k1_HP[m] = globals()["vector_1_" + str(m)]

        # Second kernel
        kernel_2_kx = sample_scaled[int(n_var_1_kx + n_var_1_sy):int(n_var_1_kx + n_var_1_sy + n_var_2_kx)].reshape(kernel_shape_2_kx)
        kernel_2_sy = sample_scaled[int(n_var_1_kx + n_var_1_sy + n_var_2_kx):n_var].reshape(kernel_shape_2_sy)

        globals()["matriz_" + str(m)] = get_HP(shape_k1_HP, str(m), active_matriz, locals()["decimals_" + str(m)], locals()["kernel_2_" + str(m)])
        globals()["vector_" + str(m)] = globals()["matriz_" + str(m)].flatten()
        new_shape_HP[m] = globals()["vector_" + str(m)]

    #---    Other variables that MODFLOW require
    matriz_kz = matriz_kx/10
    matriz_ss = matriz_sy/100
    new_shape_HP['kz'] = matriz_kz.flatten()
    new_shape_HP['ss'] = matriz_ss.flatten()
    new_shape_HP.to_file(os.path.join(dir_iteration, 'Elements_iter_' + str(iteration) + '.shp'))
    
    #---    Generate new native files
    model = fpm.Modflow.load(path_model + '/SyntheticAquifer_NY.nam', version = 'mfnwt', exe_name = path_nwt_exe)
    model.write_input()
    model.remove_package("UPW")
    upw = fpm.ModflowUpw(model = model, laytyp=1, layavg=0, chani=-1.0, layvka=0, laywet=0, hdry=-888, iphdry=1, hk=matriz_kx, hani=1.0, vka=matriz_kz, ss=matriz_ss, sy=matriz_sy, extension='upw')
    upw.write_file()
    model.run_model()
    
    #---    Move native files to WEAP
    get_old_files = os.listdir(path_model)
    get_new_files = os.listdir(os.getcwd())

    #---    Delete old files
    for g in get_old_files:
        try:
            os.remove(os.path.join(path_model, g))
        except:
            print('No hay archivos')

    #---    Move new files
    for h in get_new_files:
        if h.endswith('.py') or h == '__pycache__' or h == 'sp' or h.endswith('.txt'):
            pass 
        else:
            shutil.move(os.path.join(os.getcwd(), h), os.path.join(path_model, h))
    
    #-------------------------------------
    #---    Run WEAP-MODFLOW model    ----
    #-------------------------------------
    WEAP = win32.Dispatch("WEAP.WEAPApplication")
    WEAP.ActiveArea = "SyntheticProblem_WEAPMODFLOW"
    WEAP.Calculate()

    #---    Export results
    favorites = pd.read_excel(r"C:\Users\vagrant\Documents\MODFLOW_Calibration\data\Favorites_WEAP.xlsx")
    for i,j in zip(favorites["BranchVariable"],favorites["WEAP Export"]):
        WEAP.LoadFavorite(i)
        WEAP.ExportResults(os.path.join(dir_iteration, f"iter_{str(iteration)}_{j}.csv"), True, True, True, False, False)

    #---------------------------------
    #---    Objective Function    ----
    #---------------------------------
    #---    Well analysis
    obs_well = get_data(os.path.join(path_obs_data, 'Wells_observed.csv'), 3)
    ow = obs_well.columns

    sim_well = get_data(os.path.join(dir_iteration, f"iter_{str(iteration)}_Wells_simulation.csv"), 3)

    srmse_well = 0
    for i in ow:
        mse_well = mean_squared_error(obs_well[i], sim_well[i])
        rmse_well = math.sqrt(mse_well)
        srmse_well += rmse_well

    #---    Streamflow analysis
    df_q = pd.read_csv(os.path.join(dir_iteration, f"iter_{str(iteration)}_Streamflow_gauges.csv"), skiprows = 3)
    mse_q = mean_squared_error(df_q['Observed'], df_q['Modeled'])
    rmse_q = math.sqrt(mse_q)

    #---    Subject to
    kx_min = 0.280
    kx_max = 67.056
    sy_min = 0.0074
    sy_max = 0.1282

    for i in HP:
        globals()["vector_modif_" + str(i)] = get_eliminate_zeros(globals()["vector_" + str(i)].tolist())
        globals()["P_" + str(i)] = get_evaluate_st_bounds((locals()[str(i) + "_min"]), (locals()[str(i) + "_max"]), globals()["vector_modif_" + str(i)])

    #---    Total Objective Function
    gw = 0.8
    gq = 1 - gw
    gk = 0.5
    gs = 1 - gk

    of = gw*srmse_well + gq*rmse_q + gk*P_kx + gs*P_sy
    return of