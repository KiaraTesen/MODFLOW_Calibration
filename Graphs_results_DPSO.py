# -*- coding: utf-8 -*-

#---    Packages
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path_results_DPSO = 'results_DPSO'
experiment = ['P1', 'P2']
machines = range(3,23)

df = pd.DataFrame()
df_log = pd.DataFrame()
for i in experiment:
    for j in machines:
        path_experiment = os.path.join(path_results_DPSO, i, 'log_iteration_vm' + str(j) + '.txt')

        file = open(path_experiment, 'r')
        lines = file.readlines()

        iteration = 0
        for line in lines:
            if line[0:11] == "('Pob.y: ',":
                column_name_y = 'y-vm' + str(j) + '-' + str(i)
                pob_y_value = float(line[12:-2])
                df.loc[iteration, column_name_y] = pob_y_value
            #if line[0:16] == "('Pob.y_best: ',":
                #pob_y_best_value = line[17:-2]
                #df.loc[iteration, 'y_best'] = pob_y_best_value
                iteration += 1

df['iteration'] = range(21)
df.set_index('iteration',inplace = True)
df['Min_values'] = df.min(axis = 1)
df['Max_values'] = df.max(axis = 1)
df['Mean_values'] =df.mean(axis = 1)

df_log = np.log(df)
print(df)
#print(df_log.iloc[:,0:-3])

# Gráfico de áreas
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(df_log.iloc[:,0:-3], color = "black", linewidth = 0.25)
ax.fill_between(x = range(21), y1 = df_log.loc[:,'Min_values'], y2 = df_log.loc[:,'Max_values'],  alpha = 0.2, color = "#1f77b4") # Polígono
ax.plot(range(21), df_log.loc[:,'Mean_values'], color = "#1f77b4") 

xlim, ylim = 20, 50
plt.xticks(range(0, xlim + 1, 5), fontsize = 10)
plt.yticks(range(0, ylim + 1, 10), fontsize = 10)
plt.xlim(0, xlim)
plt.ylim(0, ylim)

plt.title("n = 20", fontsize = 14, weight = "bold")
plt.xlabel("Iterations", fontsize = 10)
plt.ylabel("log(E)", fontsize = 10)

plt.savefig("results_DPSO/DPSO.png")
plt.clf()

#---    BOXPLOT

column_list = df_log.columns
df_concat = df_log.iloc[:,0]
for m in range(len(column_list) - 4):
    df_concat = pd.concat([df_concat, df_log.iloc[:,m+1]])
df_concat = df_concat.reset_index()
del df_concat['iteration']
df_concat = df_concat.dropna()
#print(df_concat)

# Graph Boxplot
fig, ax = plt.subplots(figsize=(8, 6))
ax.boxplot(df_concat)
plt.savefig("results_DPSO/DPSO_boxplot")


