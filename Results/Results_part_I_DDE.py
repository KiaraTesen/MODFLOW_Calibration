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
configuration = 'n = 50'
title = 'n = 50'
experiments = ['E1']
machines = list(range(2,52))
iterations = list(range(201))

methodology = 'DDE'                #'DDE'
path_results = os.path.join(r'D:\1_PaperI', methodology, configuration) 

#---    Lectura archivos h5
df_y = pd.DataFrame()
df_y_log = pd.DataFrame()
for i in experiments:
    df_y_exp = pd.DataFrame()
    for j in machines:
        path_experiment = os.path.join(path_results, i, methodology + '_historial_vm' + str(j) + '.h5')

        with h5py.File(path_experiment, 'r') as f:
            x = f["pob_x"][:]
            y = f["pob_y"][:]

        for k in iterations:
            df_y.loc[k,"Y-vm" + str(j) + '-' + str(i)] = y[k, 0]
            df_y.loc[df_y["Y-vm" + str(j) + '-' + str(i)] == 0, "Y-vm" + str(j) + '-' + str(i)] = np.nan
    
            df_y_exp.loc[k,"Y-vm" + str(j) + '-' + str(i)] = y[k, 0]
            df_y_exp.loc[df_y_exp["Y-vm" + str(j) + '-' + str(i)] == 0, "Y-vm" + str(j) + '-' + str(i)] = np.nan

    df_y_exp['iteration'] = range(len(df_y_exp))
    df_y_exp.set_index('iteration',inplace = True)

    df_y_exp['Min_values'] = df_y_exp.min(axis = 1)
    df_y_exp['Max_values'] = df_y_exp.max(axis = 1)
    df_y_exp['Mean_values'] =df_y_exp.mean(axis = 1)

    df_y_exp.to_csv(os.path.join(path_results, i, 'df_y_exp_' + methodology + '_' + i + '.csv'))

    #---    Resultados en escala logarítmica
    df_y_exp_log = np.log(df_y_exp)
    df_y_exp_log.to_csv(os.path.join(path_results, i, 'Graficas', 'df_y_exp_log_' + methodology + '_' + i + '.csv'))        ## GENERAL

    #---    Gráfico de áreas
    df_exp = df_y_exp_log   #df_y - Depende como se desea presentar resultados
    outlier_bound = 5

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(df_exp.iloc[:,0:-3], color = "black", linewidth = 0.25)
    ax.fill_between(x = range(len(df_exp)), y1 = df_exp.loc[:,'Min_values'], y2 = df_exp.loc[:,'Max_values'],  alpha = 0.2, color = "#1f77b4") # Polígono
    ax.plot(range(len(df_y)), df_exp.loc[:,'Mean_values'], color = "#1f77b4") 

    xlim, ylim = len(iterations), round(df_exp['Max_values'].max(axis = 0)) + 5
    plt.xticks(range(0, xlim + 1, 10), fontsize = 10)
    #plt.yticks(range(0, ylim + 1, 5), fontsize = 10)
    plt.xlim(0, xlim)
    #plt.ylim(55, ylim)

    plt.title(str(title), fontsize = 14, weight = "bold")
    plt.xlabel("Iterations", fontsize = 10)
    plt.ylabel("log E", fontsize = 10)

    plt.savefig(os.path.join(path_results, i, 'Graficas', 'error_vs_iteration_' + methodology + '_' + i + '.png'))  ## GENERAL
    plt.clf()

df_y.to_csv(os.path.join(path_results, 'df_y_' + methodology + '_' + configuration + '.csv'))

df_y['iteration'] = range(len(df_y))
df_y.set_index('iteration',inplace = True)

df_y['Min_values'] = df_y.min(axis = 1)
df_y['Max_values'] = df_y.max(axis = 1)
df_y['Mean_values'] =df_y.mean(axis = 1)
#print(df_y)

#---    Resultados en escala logarítmica
df_y_log = np.log(df_y)
df_y_log.to_csv(os.path.join(path_results, 'Graficas', 'df_y_log_' + methodology + '_' + configuration + '.csv'))        ## GENERAL

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

plt.title(str(configuration), fontsize = 14, weight = "bold")
plt.xlabel("Iterations", fontsize = 10)
plt.ylabel("Fitness Function (E)", fontsize = 10)

plt.savefig(os.path.join(path_results, 'Graficas', 'error_vs_iteration_' + methodology + '_' + i + '.png'))  ## GENERAL
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
plt.savefig(os.path.join(path_results, 'Graficas', 'Boxplot_error_' + methodology + '_' + i + '.png'))       ## GENERAL
plt.clf()