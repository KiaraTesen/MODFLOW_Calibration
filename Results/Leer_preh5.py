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
experiments = ['P14-SCL-ps1']
machines = list(range(2,22))
iterations = list(range(201))

methodology = 'DPSO'                #'DDE'
path_results = r'..\results_' + methodology   #r'..\results_DDE'

#---    Lectura archivos h5
df_y = pd.DataFrame()
df_y_log = pd.DataFrame()
for i in experiments:
    for j in machines:
        path_experiment = os.path.join(path_results, i, methodology + '_historial_vm' + str(j) + '.h5')

        with h5py.File(path_experiment, 'r') as f:
            x = f["pob_x"][:]
