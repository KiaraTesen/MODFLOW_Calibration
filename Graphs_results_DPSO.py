# -*- coding: utf-8 -*-

#---    Packages
import os
import pandas as pd

path_results_DPSO = 'results_DPSO'
experiment = ['P1']
machines = range(3,23)

for i in experiment:
    for j in machines:
        path_experiment = os.path.join(path_results_DPSO, i, 'log_iteration_vm' + str(j) + '.txt')

        file = open(path_experiment, 'r')
        lines = file.readlines()

        df = pd.DataFrame()
        iteration = 0
        for line in lines:
            if line[0:11] == "('Pob.y: ',":
                pob_y_value = line[12:-2]
                df.loc[iteration, 'y'] = pob_y_value
            if line[0:16] == "('Pob.y_best: ',":
                pob_y_best_value = line[17:-2]
                df.loc[iteration, 'y_best'] = pob_y_best_value
                iteration += 1
        print(df)

