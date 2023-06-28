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
def get_HP(Shape_HP, new_Shape, variable, particle, begin, end):
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

def Run_WEAP_MODFLOW(path_output, iteration, initial_shape_HP, HP, active_cells, sample_scaled, path_init_model, path_model, path_nwt_exe, path_obs_data):
    dir_iteration = os.path.join(path_output, "iter_" + str(iteration))
    if not os.path.isdir(dir_iteration):
        os.mkdir(dir_iteration)
    
    #--------------------------
    #---    Run MODFLOW    ----
    #--------------------------
    #---    Modified matriz
    new_shape_HP = initial_shape_HP.copy()
    for m in HP:
        if m == "kx":
            begin = 0
            end = active_cells
        elif m == "sy":
            begin = active_cells
            end = active_cells * 2
        globals()["matriz_" + str(m)] = get_HP(initial_shape_HP, new_shape_HP, str(m), sample_scaled, begin, end)
        globals()["vector_" + str(m)] = globals()["matriz_" + str(m)].flatten()

    #---    Other variables that MODFLOW require
    matriz_kz = matriz_kx/10
    matriz_ss = matriz_sy/100
    new_shape_HP['kz'] = matriz_kz.flatten()
    new_shape_HP['ss'] = matriz_ss.flatten()
    
    new_shape_HP.to_file(os.path.join(dir_iteration, 'Elements_iter_' + str(iteration) + '.shp'))
    
    #---    Generate new native files
    model = fpm.Modflow.load(path_init_model + '/SyntheticAquifer_NY.nam', version = 'mfnwt', exe_name = path_nwt_exe)
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
        if h.endswith('.py') or h == '__pycache__' or h == 'sp' or h.endswith('.txt') or h == 'output':
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
    df_q = df_q.set_index('Statistic')
    df_q = df_q.set_index(pd.to_datetime(df_q.index))
    df_q = df_q.iloc[36:,:]

    df_q_obs = get_data(os.path.join(path_obs_data, 'StreamflowGauges_KPR_vf.csv'), 2)
    
    mse_q = mean_squared_error(df_q_obs['Observed'], df_q['Modeled'])
    rmse_q = math.sqrt(mse_q)
    print(rmse_q)

    """
    #---    Subject to
    kx_min = 0.280
    kx_max = 67.056
    sy_min = 0.01
    sy_max = 0.1282

    for i in HP:
        globals()["vector_modif_" + str(i)] = get_eliminate_zeros(globals()["vector_" + str(i)].tolist())
        globals()["P_" + str(i)] = get_evaluate_st_bounds((locals()[str(i) + "_min"]), (locals()[str(i) + "_max"]), globals()["vector_modif_" + str(i)])
    """
    #---    Total Objective Function
    #---    There are 31 observation wells and 1 streamflow gauge (32 monitoring elements. If each of them has the same weighting factor: 1/32 = 0.03125 (3.125%))
    g1 = 0.4
    g2 = 0.2
    #g3 = 0.4

    #of = g1*srmse_well + g2*rmse_q + g3*(P_kx + P_sy)
    of = g1*srmse_well + g2*rmse_q
    return of
