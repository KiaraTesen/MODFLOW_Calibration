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
experiments = ['P16-pre']
machines = list(range(2,22))
iterations = list(range(201))

methodology = 'DDE'                #'DDE'
path_results = r'..\results_' + methodology   #r'..\results_DDE'

#---    Lectura archivos h5
df_y = pd.DataFrame()
df_y_log = pd.DataFrame()
df_x = pd.DataFrame()
for i in experiments:
    for j in machines:
        path_experiment = os.path.join(path_results, i, methodology + '_historial_vm' + str(j) + '.h5')

        with h5py.File(path_experiment, 'r') as f:
            x = f["pob_x"][:]
            y = f["pob_y"][:]

        for k in iterations:
            df_y.loc[k,"Y-vm" + str(j) + '-' + str(i)] = y[k, 0]
            df_y.loc[df_y["Y-vm" + str(j) + '-' + str(i)] == 0, "Y-vm" + str(j) + '-' + str(i)] = np.nan

            df_x.loc[k,"X-vm" + str(j) + '-' + str(i)] = x[k, 0]
    df_y.to_csv(os.path.join(path_results, i, 'df_y_' + methodology + '_' + i + '.csv'))

df_y['iteration'] = range(len(df_y))
df_y.set_index('iteration',inplace = True)

df_x['iteration'] = range(len(df_x))
df_x.set_index('iteration',inplace = True)
print(df_x)

df_y['Min_values'] = df_y.min(axis = 1)
df_y['Max_values'] = df_y.max(axis = 1)
df_y['Mean_values'] =df_y.mean(axis = 1)
print(df_y)
