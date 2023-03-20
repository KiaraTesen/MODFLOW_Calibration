# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 2023
@author: Kiara Tesen
"""

# Packages
import geopandas as gpd
import pandas as pd
import numpy as np
import flopy.modflow as fpm

import win32com.client as win32

#--------------------------------------------------------------
#---    Modification of Hydraulic Properties - MODFLOW    ----
#--------------------------------------------------------------

path_model = r'..\data\MODFLOW_Model'
path_nwt_exe = r'..\data\MODFLOW-NWT_1.2.0\bin\MODFLOW-NWT_64.exe'
path_GIS = r'..\data\GIS'

#K_values = [0.328, 0.512, 0.656, 0.82, 1.28, 1.64, 2.56, 3.28, 4.48, 5.12, 6.56, 8.2, 12.8, 16.4, 25.6, 32.8, 44.8, 51.2, 65.6]

def get_HP(Shape_HP, variable):
    rows = Shape_HP["ROW"].max()
    columns = Shape_HP["COLUMN"].max()

    matriz = np.zeros((rows,columns))
    for i in range(0,len(Shape_HP['ROW'])):
        matriz[Shape_HP['ROW'][i]-1][Shape_HP['COLUMN'][i]-1] = Shape_HP[variable][i]# AQUÍ HACER LA OPERACION
    return matriz

Shape_original_HP = gpd.read_file(path_GIS + '/Elements_FA_2.shp')
matriz_kx = get_HP(Shape_original_HP, ('HK_m_day_M'))
matriz_kz = get_HP(Shape_original_HP, ('VK_m_day_M'))
matriz_ss = get_HP(Shape_original_HP, ('Ss'))
matriz_sy = get_HP(Shape_original_HP, ('Sy'))
#print(np.shape(matriz_kx))

model = fpm.Modflow.load(path_model + '/SyntheticAquifer_NY.nam', version = 'mfnwt', exe_name = path_nwt_exe)
model.write_input()
model.remove_package("UPW")
upw = fpm.ModflowUpw(model = model, laytyp=1, layavg=0, chani=-1.0, layvka=0, laywet=0, hdry=-888, iphdry=1, hk=matriz_kx, hani=1.0, vka=matriz_kz, ss=matriz_ss, sy=matriz_sy, extension='upw')
upw.write_file()

model.run_model()

"""
#-------------------------------------
#---    Run WEAP-MODFLOW model    ----
#-------------------------------------

WEAP = win32.Dispatch("WEAP.WEAPApplication")
WEAP.ActiveArea = "SyntheticProblem_WEAPMODFLOW"
WEAP.ActiveScenario = WEAP.Scenarios("Current Accounts")

WEAP.Calculate()
"""