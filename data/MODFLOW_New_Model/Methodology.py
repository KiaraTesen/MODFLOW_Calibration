# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 2023
@author: Kiara Tesen
"""

#---    Packages
import geopandas as gpd
import pandas as pd
import numpy as np
import flopy.modflow as fpm
import os
import shutil
import win32com.client as win32

#---    Paths
path_WEAP = r'C:\Users\Francisco Suárez P\Documents\WEAP Areas\SyntheticProblem_WEAPMODFLOW_Prueba'
path_model = r'..\MODFLOW_Model'
path_nwt_exe = r'..\MODFLOW-NWT_1.2.0\bin\MODFLOW-NWT_64.exe'
path_GIS = r'..\GIS'
path_output = r'C:\Users\Francisco Suárez P\Desktop\GitHub - KT\MODFLOW_Calibration\data\output' # Necesita ruta completa por WEAP Export

iteration = 1

dir_iteration = os.path.join(path_output, "iter_" + str(iteration))
if not os.path.isdir(dir_iteration):
    os.mkdir(dir_iteration)

"""
#-------------------------------------------------------------
#---    Modification of Hydraulic Properties - MODFLOW    ----
#-------------------------------------------------------------

#K_values = [0.328, 0.512, 0.656, 0.82, 1.28, 1.64, 2.56, 3.28, 4.48, 5.12, 6.56, 8.2, 12.8, 16.4, 25.6, 32.8, 44.8, 51.2, 65.6]

#---    Generate new shape of HP
def get_HP(Shape_HP, variable):
    rows = Shape_HP["ROW"].max()
    columns = Shape_HP["COLUMN"].max()

    matriz = np.zeros((rows,columns))
    for i in range(0,len(Shape_HP['ROW'])):
        matriz[Shape_HP['ROW'][i]-1][Shape_HP['COLUMN'][i]-1] = Shape_HP[variable][i] * 5 # AQUÍ HACER LA OPERACION
    return matriz

original_shape_HP = gpd.read_file(path_GIS + '/Elements_FA.shp') # El shape que se use depende del mejor resultado (?)
variables = ['kx', 'kz', 'ss', 'sy']
new_shape_HP = original_shape_HP

for i in variables:
    locals()["matriz_" + str(i)] = get_HP(original_shape_HP, str(i)) # El shape que se use depende del mejor resultado (?)
    vector = locals()["matriz_" + str(i)].flatten()
    new_shape_HP[i] = vector
#print(matriz_kx)
#print(new_shape_HP)

#---    Save new shape of HP
dir_iteration = os.path.join(path_output, "iter_" + str(iteration))
if not os.path.isdir(dir_iteration):
    os.mkdir(dir_iteration)
new_shape_HP.to_file(os.path.join(dir_iteration, 'Elements_FA_iter_' + str(iteration) + '.shp'))

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
"""
#-------------------------------------
#---    Run WEAP-MODFLOW model    ----
#-------------------------------------

WEAP = win32.Dispatch("WEAP.WEAPApplication")
WEAP.ActiveArea = "SyntheticProblem_WEAPMODFLOW_Prueba"
WEAP.ActiveScenario = WEAP.Scenarios("Current Accounts")
WEAP.Calculate()

#---    Export results
favorites = pd.read_excel("../Favorites_WEAP.xlsx")

for i,j in zip(favorites["BranchVariable"],favorites["WEAP Export"]):
    WEAP.LoadFavorite(i)
    WEAP.ExportResults(os.path.join(dir_iteration, f"iter_{str(iteration)}_{j}.csv"), True, True, True, False, False)

#---------------------------------
#---    Objective Function    ----
#---------------------------------

#---    Subject to

