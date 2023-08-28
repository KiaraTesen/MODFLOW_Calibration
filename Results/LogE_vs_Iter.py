# -*- coding: utf-8 -*-

#---    Packages
import h5py
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

#---    Initial information
methodology = 'DDE'                #'DDE'
configuration = 'n = 50'
title = 'n = 50'
experiments = ['E1']
machines = list(range(2,52))
iterations = list(range(201))

path_results = os.path.join(r'D:\1_PaperI', methodology, configuration) 

alpha_value = 90

#---    Lectura archivos h5
df_y = pd.DataFrame()

for i in experiments:
#    df_y_exp = pd.DataFrame()
    for j in machines:
        path_experiment = os.path.join(path_results, i, methodology + '_historial_vm' + str(j) + '.h5')

        with h5py.File(path_experiment, 'r') as f:
            x = f["pob_x"][:]
            #v = f["pob_v"][:]
            y = f["pob_y"][:]
            #x_best = f["pob_x_best"][:]
            #y_best = f["pob_y_best"][:]
            #w = f["w"][:]

        for k in iterations:
            df_y.loc[k,"Y-vm" + str(j) + '-' + str(i)] = y[k, 0]
            df_y.loc[df_y["Y-vm" + str(j) + '-' + str(i)] == 0, "Y-vm" + str(j) + '-' + str(i)] = np.nan

#---    Resultados en escala logarítmica
df_y_log = np.log(df_y)

#---    Transpose to reorder
df_y_T = df_y.transpose()
df_y_log_T = df_y_log.transpose()

#print(df_y_T)
#print(df_y_log['Y-vm6-E2'].dropna())

#---    Confidence Intervals
df_register = pd.DataFrame(index = ['Upper CI - ' + str(alpha_value) + '%', 'Lower CI - ' + str(alpha_value) + '%', 'Mean'])

for m in iterations:
    df_value = df_y_log_T.iloc[:,m]
    df_value = df_value.dropna()

    CI = st.norm.interval(alpha = alpha_value/100, loc = np.mean(df_value), scale = st.sem(df_value))
    mean_value = np.mean(df_value)
    #print(m, mean_value, CI, df_value.size)

    Lower_CI, Upper_CI = CI[0], CI[1]
    
    df_register.loc['Upper CI - ' + str(alpha_value) + '%', str(m)] = Upper_CI
    df_register.loc['Lower CI - ' + str(alpha_value) + '%', str(m)] = Lower_CI
    df_register.loc['Mean', str(m)] = mean_value

df_register_T = df_register.transpose()
print(df_register_T)

#---    Graph 1
Lower_bound = 3.5
Upper_bound = 6.0

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(range(len(df_register_T)), df_register_T.loc[:,'Upper CI - ' + str(alpha_value) + '%'], color = "black", linewidth = 0.5, linestyle = 'dashed', label = 'Upper CI - ' + str(alpha_value) + '%')
ax.plot(range(len(df_register_T)), df_register_T.loc[:,'Lower CI - ' + str(alpha_value) + '%'], color = "black", linewidth = 0.5, linestyle = 'dotted', label = 'Lower CI - ' + str(alpha_value) + '%')
ax.plot(range(len(df_register_T)), df_register_T.loc[:,'Mean'], color = "#A52A2A", linewidth = 0.5, linestyle = 'solid', label = 'Mean')
#ax.fill_between(x = range(len(df_register_T)), y1 = df_register_T.loc[:,'Upper CI - ' + str(alpha_value) + '%'], y2 =  df_register_T.loc[:,'Lower CI - ' + str(alpha_value) + '%'],  alpha = 0.2, color = "#1f77b4") # Polígono

xlim = len(iterations)
plt.xticks(range(0, xlim, 10), fontsize = 10)
plt.xlim(0, xlim)
plt.ylim(Lower_bound, Upper_bound)

plt.title(str(title), fontsize = 14, weight = "bold")
plt.xlabel("Iterations", fontsize = 10)
plt.ylabel("log E", fontsize = 10)
plt.legend(loc='upper right')

plt.savefig(os.path.join(r'D:\1_PaperI', methodology, 'Graficas', 'error_vs_iteration_' + methodology + '_' + configuration + '_' + str(alpha_value) + '.png'))  ## GENERAL
plt.clf()

#---    Convert .PNG to .EPS
image_png = os.path.join(r'D:\1_PaperI', methodology, 'Graficas', 'error_vs_iteration_' + methodology + '_' + configuration + '_' + str(alpha_value) + '.png')
im = Image.open(image_png)
#print(im.mode)

fig = im.convert('CMYK')                #L, RGB, CMYK
fig.save(os.path.join(r'D:\1_PaperI', methodology, 'Graficas', 'error_vs_iteration_' + methodology + '_' + configuration + '_' + str(alpha_value) + '.eps'), lossless = True)