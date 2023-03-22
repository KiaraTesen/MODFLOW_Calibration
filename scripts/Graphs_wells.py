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
dir_iteration = os.path.join(path_output, "iter_" + str(iteration))

ows = ['OW22', 'OW29', 'OW35', 'OW36', 'OW43', 'OW48', 'OW51', 'OW83', 'OW87', 'OW97', 'OW100', 'OW157', 'OW159', 'OW167', 'OW169', 'OW181', 'OW188', 'OW209', 'OW233', 
       'OW234', 'OW235', 'OW236', 'OW237', 'OW238', 'OW239', 'OW240', 'OW241', 'OW242', 'OW243', 'OW244', 'OW249']

export_ows = pd.read_csv(os.path.join(dir_iteration, f"iter_{str(iteration)}_Wells_simulation.csv"), skiprows = 3)
export_ows = export_ows.set_index('Branch')
export_ows = export_ows.set_index(pd.to_datetime(export_ows.index))
export_ows = export_ows.iloc[36:,:]
print(export_ows)

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
            #print(sim_NAS.min())

            locals()[f'ax{k+1}'].plot(sim_NAS, 'k-', label = 'simulado')
            locals()[f'ax{k+1}'].set_title(str(vector[k]), size = 11, fontweight="bold")
            locals()[f'ax{k+1}'].legend(loc = "best")
            locals()[f'ax{k+1}'].tick_params(axis='both',labelsize=8)
            locals()[f'ax{k+1}'].set_xlim(np.datetime64('1985-10-01'), np.datetime64('2009-10-01'))
            locals()[f'ax{k+1}'].xaxis.set_major_locator(mdates.MonthLocator(interval=36))
            locals()[f'ax{k+1}'].set_ylim(math.floor(sim_NAS.min()), math.ceil(sim_NAS.max()))
            #print(int(math.floor(math.floor(sim_NAS.min())/5)*5), int(math.ceil(math.ceil(sim_NAS.max())/5)*5))
            plt.setp(locals()[f'ax{k+1}'].get_xticklabels(), rotation=90, ha='right')

        plt.subplots_adjust(wspace=0.25,hspace=0.4)
        fig.delaxes(ax6)
        plt.savefig(os.path.join(dir_iteration, f"DW_ObsWell_{str(j+1)}.png"))
        
    else:
        fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2,3, figsize = (15, 8))
        
        for k in range(len(vector)):
            sim_NAS = export_ows[vector[k]]
            #print(sim_NAS)
            locals()[f'ax{k+1}'].plot(sim_NAS, 'k-', label = 'simulado')
            locals()[f'ax{k+1}'].set_title(str(vector[k]), size = 11, fontweight="bold")
            locals()[f'ax{k+1}'].legend(loc = "best")
            locals()[f'ax{k+1}'].tick_params(axis='both',labelsize=8)
            locals()[f'ax{k+1}'].set_xlim(np.datetime64('1985-10-01'), np.datetime64('2009-10-01'))
            locals()[f'ax{k+1}'].xaxis.set_major_locator(mdates.MonthLocator(interval=36))
            locals()[f'ax{k+1}'].set_ylim(math.floor(sim_NAS.min()), math.ceil(sim_NAS.max()))
            #print(int(math.floor(math.floor(sim_NAS.min())/5)*5), int(math.ceil(math.ceil(sim_NAS.max())/5)*5))
            plt.setp(locals()[f'ax{k+1}'].get_xticklabels(), rotation=90, ha='right')

        plt.subplots_adjust(wspace=0.25,hspace=0.4)
        
        plt.subplots_adjust(wspace=0.2,hspace=0.35)
        plt.savefig(os.path.join(dir_iteration, f"DW_ObsWell_{str(j+1)}.png"))


#print(ows_1, ows_2, ows_3, ows_4, ows_5, ows_6)
"""

for j in SHACs:     

    if j == 'L01' or j == 'L12':
        fig, ((ax1)) = plt.subplots(1,1, figsize = (8, 4))
        #fig.suptitle('SHAC - ' + str(j))
        for i in range(len(locals()[j])):
            observed_NAS = pd.read_excel(ruta_data + '/NAS_observed_DGA.xlsx', sheet_name = locals()[j][i])
            observed_NAS = observed_NAS.set_index('Fecha')
            observed_NAS = observed_NAS.set_index(pd.to_datetime(observed_NAS.index))
            #print(observed_NAS)

            sim_NAS = WEAP_export['Sim_' + locals()[j][i]]
            #print(sim_NAS)

            locals()[f'ax{i+1}'].plot(observed_NAS, 'o', markersize=4, label = 'observado')
            locals()[f'ax{i+1}'].plot(sim_NAS, 'k-', label = 'simulado')
            locals()[f'ax{i+1}'].set_title(str(locals()[j][i]), size = 11, fontweight="bold")
            locals()[f'ax{i+1}'].legend(loc = "best")
            locals()[f'ax{i+1}'].tick_params(axis='both',labelsize=8)

        plt.subplots_adjust(wspace=0.2,hspace=0.35)
        plt.savefig(ruta_results + '/' + version + '/NAS/Pozos_SHAC_' + str(j) + '.png')
"""