# -*- coding: utf-8 -*-
"""
Created on Tue Mar 3 12:37:58 2023
@author: Kiara Tesen
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
import cv2
import os
import numpy as np

iteration = 1

#---    Paths
path_output = r'C:\Users\Francisco Suárez P\Desktop\GitHub - KT\MODFLOW_Calibration\data\output' # Necesita ruta completa por WEAP Export
path_obs_values = r'../data/ObservedData'
dir_iteration = os.path.join(path_output, "iter_" + str(iteration))

ows = ['OW22', 'OW29', 'OW35', 'OW36', 'OW43', 'OW48', 'OW51', 'OW83', 'OW87', 'OW97', 'OW100', 'OW157', 'OW159', 'OW167', 'OW169', 'OW181', 'OW188', 'OW209', 'OW233', 
       'OW234', 'OW235', 'OW236', 'OW237', 'OW238', 'OW239', 'OW240', 'OW241', 'OW242', 'OW243', 'OW244', 'OW249']

export_ows = pd.read_csv(os.path.join(dir_iteration, f"iter_{str(iteration)}_Wells_simulation.csv"), skiprows = 3)
export_ows = export_ows.set_index('Branch')
export_ows = export_ows.set_index(pd.to_datetime(export_ows.index))
export_ows = export_ows.iloc[36:,:]

owo = pd.read_csv(os.path.join(path_obs_values, 'Wells_observed.csv'), skiprows = 3)
owo = owo.set_index('Branch')
owo = owo.set_index(pd.to_datetime(owo.index))
owo = owo.iloc[36:,:]

for i in range(0,6):
    if i < 5:
        locals()[f"ows_{i+1}"] = ows[5*i:5*i+5] 
    else:
        locals()[f"ows_{i+1}"] = ows[5*i:5*i+6]

for j in range(0,6):
    vector = locals()[f"ows_{j+1}"]

    if len(vector) == 5:
        fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2,3, figsize = (15, 8))
        
        for k in range(len(vector)):
            sim_NAS = export_ows[vector[k]]
            obs_NAS = owo[vector[k]]
            min_value = min(math.floor(sim_NAS.min()), math.floor(obs_NAS.min()))
            max_value = max(math.ceil(sim_NAS.max()), math.ceil(obs_NAS.max()))
            
            locals()[f'ax{k+1}'].plot(sim_NAS, 'k-', label = 'simulado')
            locals()[f'ax{k+1}'].plot(obs_NAS, 'r-', label = 'observado')
            locals()[f'ax{k+1}'].set_title(str(vector[k]), size = 11, fontweight="bold")
            locals()[f'ax{k+1}'].legend(loc = "best")
            locals()[f'ax{k+1}'].tick_params(axis='both',labelsize=8)
            locals()[f'ax{k+1}'].set_xlim(np.datetime64('1985-10-01'), np.datetime64('2009-10-01'))
            locals()[f'ax{k+1}'].xaxis.set_major_locator(mdates.MonthLocator(interval=36))
            locals()[f'ax{k+1}'].set_ylim(min_value, max_value)
            plt.setp(locals()[f'ax{k+1}'].get_xticklabels(), rotation=90, ha='right')

        plt.subplots_adjust(wspace=0.25,hspace=0.4)
        fig.delaxes(ax6)
        plt.savefig(os.path.join(dir_iteration, f"DW_ObsWell_{str(j+1)}.png"))
        
    else:
        fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2,3, figsize = (15, 8))
        
        for k in range(len(vector)):
            sim_NAS = export_ows[vector[k]]
            obs_NAS = owo[vector[k]]
            min_value = min(math.floor(sim_NAS.min()), math.floor(obs_NAS.min()))
            max_value = max(math.ceil(sim_NAS.max()), math.ceil(obs_NAS.max()))

            locals()[f'ax{k+1}'].plot(sim_NAS, 'k-', label = 'simulado')
            locals()[f'ax{k+1}'].plot(obs_NAS, 'r-', label = 'observado')
            locals()[f'ax{k+1}'].set_title(str(vector[k]), size = 11, fontweight="bold")
            locals()[f'ax{k+1}'].legend(loc = "best")
            locals()[f'ax{k+1}'].tick_params(axis='both',labelsize=8)
            locals()[f'ax{k+1}'].set_xlim(np.datetime64('1985-10-01'), np.datetime64('2009-10-01'))
            locals()[f'ax{k+1}'].xaxis.set_major_locator(mdates.MonthLocator(interval=36))
            locals()[f'ax{k+1}'].set_ylim(min_value, max_value)
            plt.setp(locals()[f'ax{k+1}'].get_xticklabels(), rotation=90, ha='right')

        plt.subplots_adjust(wspace=0.25,hspace=0.4)
        plt.savefig(os.path.join(dir_iteration, f"DW_ObsWell_{str(j+1)}.png"))