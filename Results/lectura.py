# -*- coding: utf-8 -*-

#---    Packages
import h5py
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

#---    Initial information
configuration = 'n = 35'
title = 'n = 35'
experiments = ['E6']
machines = list(range(2,3))
iterations = list(range(201))

methodology = 'DPSO'                #'DDE'
path_results = os.path.join(r'D:\1_PaperI\DPSO\n = 35') 

#---    Lectura archivos h5
df_y = pd.DataFrame()
df_y_log = pd.DataFrame()
for i in experiments:
    df_y_exp = pd.DataFrame()
    for j in machines:
        path_experiment = os.path.join(path_results, i, methodology + '_historial_vm' + str(j) + '.h5')

        with h5py.File(path_experiment, 'r') as f:
            x = f["pob_x"][:]
            v = f["pob_v"][:]
            y = f["pob_y"][:]
            x_best = f["pob_x_best"][:]
            y_best = f["pob_y_best"][:]
            w = f["w"][:]

        for k in iterations:
            df_y.loc[k,"Y-vm" + str(j) + '-' + str(i)] = y[k, 0]
            df_y.loc[df_y["Y-vm" + str(j) + '-' + str(i)] == 0, "Y-vm" + str(j) + '-' + str(i)] = np.nan
    
            df_y_exp.loc[k,"Y-vm" + str(j) + '-' + str(i)] = y[k, 0]
            df_y_exp.loc[df_y_exp["Y-vm" + str(j) + '-' + str(i)] == 0, "Y-vm" + str(j) + '-' + str(i)] = np.nan

print(df_y_exp)
df_y_exp.to_csv('prueba.csv')