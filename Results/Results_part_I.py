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
configuration = 'n=50'
experiments = ['E1']
machines = list(range(2,36))
iterations = list(range(201))

methodology = 'DPSO'                #'DDE'
path_results = os.path.join(r'D:\1_PaperI', methodology, configuration) 

#---    Lectura archivos h5
df_y = pd.DataFrame()
df_y_log = pd.DataFrame()
for i in experiments:
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
    df_y.to_csv(os.path.join(path_results, i, 'df_y_' + methodology + '_' + i + '.csv'))

df_y['iteration'] = range(len(df_y))
df_y.set_index('iteration',inplace = True)

df_y['Min_values'] = df_y.min(axis = 1)
df_y['Max_values'] = df_y.max(axis = 1)
df_y['Mean_values'] =df_y.mean(axis = 1)
print(df_y)

#---    Resultados en escala logarítmica
df_y_log = np.log(df_y)
print(df_y_log)
df_y_log.to_csv(os.path.join(path_results, i, 'Graficas', 'df_y_log_' + methodology + '_' + i + '.csv'))        ## GENERAL

#---    Gráfico de áreas
df = df_y_log   #df_y - Depende como se desea presentar resultados
outlier_bound = 5

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(df.iloc[:,0:-3], color = "black", linewidth = 0.25)
ax.fill_between(x = range(len(df)), y1 = df.loc[:,'Min_values'], y2 = df.loc[:,'Max_values'],  alpha = 0.2, color = "#1f77b4") # Polígono
ax.plot(range(len(df_y)), df.loc[:,'Mean_values'], color = "#1f77b4") 

xlim, ylim = len(iterations), round(df['Max_values'].max(axis = 0)) + 5
plt.xticks(range(0, xlim + 1, 10), fontsize = 10)
#plt.yticks(range(0, ylim + 1, 5), fontsize = 10)
plt.xlim(0, xlim)
#plt.ylim(55, ylim)

plt.title("n = 35", fontsize = 14, weight = "bold")
plt.xlabel("Iterations", fontsize = 10)
plt.ylabel("E", fontsize = 10)

plt.savefig(os.path.join(path_results, i, 'Graficas', 'error_vs_iteration_' + methodology + '_' + i + '.png'))  ## GENERAL
plt.clf()

#---    BOXPLOT
column_list = df.columns
df_concat = df.iloc[:,0]
for m in range(len(column_list) - 4):
    df_concat = pd.concat([df_concat, df.iloc[:,m+1]])
df_concat = df_concat.reset_index()
del df_concat['iteration']
df_concat = df_concat.dropna()

fig, ax = plt.subplots(figsize=(8, 6))
ax.boxplot(df_concat)
plt.savefig(os.path.join(path_results, i, 'Graficas', 'Boxplot_error_' + methodology + '_' + i + '.png'))       ## GENERAL
plt.clf()