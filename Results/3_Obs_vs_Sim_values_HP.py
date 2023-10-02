# -*- coding: utf-8 -*-

#---    Packages
#import matplotlib as mpl
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import math
import hydroeval as he
import warnings
warnings.filterwarnings('ignore')

#---    Initial information

#---    DPSO
methodology = 'DPSO'        
configuration = 'n = 50'
best_experiment = 'E2'
best_result = 'vm41'
best_iteration = 199
best_shape = 'Elements_iter_' + str(best_iteration) + '.shp'
best_q = 'iter_' + str(best_iteration) + '_Streamflow_gauges.csv'
best_w = 'iter_' + str(best_iteration) + '_Wells_simulation.csv'
path_results = os.path.join(r'D:\1_PaperI', methodology, configuration) 

#---    DDE
methodology_2 = 'DDE'        
configuration_2 = 'n = 35'
best_experiment_2 = 'E7'
best_result_2 = 'vm27'
best_iteration_2 = 192
best_shape_2 = 'Elements_iter_' + str(best_iteration_2) + '.shp'
best_q_2 = 'iter_' + str(best_iteration_2) + '_Streamflow_gauges.csv'
best_w_2 = 'iter_' + str(best_iteration_2) + '_Wells_simulation.csv'
path_results_2 = os.path.join(r'D:\1_PaperI', methodology_2, configuration_2) 

elements_init = 'Elements_initial_unique_value_v2'

variables = ['kx', 'sy'] #

#---    Streamflow analysis
df_q = pd.read_csv(os.path.join(path_results, best_experiment, best_result, 'iter_' + str(best_iteration), best_q), skiprows = 3)
df_q = df_q.set_index('Statistic')
df_q = df_q.set_index(pd.to_datetime(df_q.index))
df_q = df_q.iloc[36:,:]
#print(df_q)

df_q_2 = pd.read_csv(os.path.join(path_results_2, best_experiment_2, best_result_2, 'iter_' + str(best_iteration_2), best_q_2), skiprows = 3)
df_q_2 = df_q_2.set_index('Statistic')
df_q_2 = df_q_2.set_index(pd.to_datetime(df_q_2.index))
df_q_2 = df_q_2.iloc[36:,:]
#print(df_q_2)

df_q_obs = pd.read_csv(r'..\data\ObservedData\StreamflowGauges_KPR_vf.csv', skiprows = 2)
df_q_obs = df_q_obs.iloc[36:,:]
#print(df_q_obs)

DF_q = pd.DataFrame()
DF_q['Modeled - ADPSO-CL'] = np.array(df_q['Modeled'])
DF_q['Modeled - ADDE-CL'] = np.array(df_q_2['Modeled'])
DF_q['Observed'] = np.array(df_q_obs['Observed'])
#DF_q['Initial value'] = np.array(df_q_init['Modeled'])
DF_q = DF_q.set_index(pd.to_datetime(df_q.index))

#---    Metrics
print('DPSO')
rmse_q = he.evaluator(he.rmse, DF_q['Modeled - ADPSO-CL'], DF_q['Observed'])
nse_q = he.evaluator(he.nse, DF_q['Modeled - ADPSO-CL'], DF_q['Observed'])
kge_q, r, alpha, beta = he.evaluator(he.kge, DF_q['Modeled - ADPSO-CL'], DF_q['Observed']) # kge, r, alpha, beta
pbias_q = he.evaluator(he.pbias, DF_q['Modeled - ADPSO-CL'], DF_q['Observed'])
mae_q = mean_absolute_error(DF_q['Observed'], DF_q['Modeled - ADPSO-CL'])
r2_q = r2_score(DF_q['Observed'], DF_q['Modeled - ADPSO-CL'])
print(round(rmse_q[0],3), round(nse_q[0],3), round(kge_q[0],3), round(r2_q,3))

print('DDE')
rmse_q_2 = he.evaluator(he.rmse, DF_q['Modeled - ADDE-CL'], DF_q['Observed'])
nse_q_2 = he.evaluator(he.nse, DF_q['Modeled - ADDE-CL'], DF_q['Observed'])
kge_q_2, r_2, alpha_2, beta_2 = he.evaluator(he.kge, DF_q['Modeled - ADDE-CL'], DF_q['Observed']) # kge, r, alpha, beta
pbias_q_2 = he.evaluator(he.pbias, DF_q['Modeled - ADDE-CL'], DF_q['Observed'])
mae_q_2 = mean_absolute_error(DF_q['Observed'], DF_q['Modeled - ADDE-CL'])
r2_q_2 = r2_score(DF_q['Observed'], DF_q['Modeled - ADDE-CL'])
print(round(rmse_q_2[0],3), round(nse_q_2[0],3), round(kge_q_2[0],3), round(r2_q_2,3))

#---    Graph
fig = plt.subplots(figsize=(14, 7))
plt.plot(DF_q['Observed'], label = 'Obs', color = "black", linewidth = 0.75)
plt.plot(DF_q['Modeled - ADPSO-CL'], label = 'ADPSO-CL', color = "red", linewidth = 0.75)
plt.plot(DF_q['Modeled - ADDE-CL'], label = 'ADDE-CL', color = "blue", linewidth = 0.75)
#plt.plot(DF_q['Initial value'], label = 'Init', color = "blue", linewidth = 0.25)

ymin = min(DF_q['Modeled - ADPSO-CL'].to_numpy().min(), DF_q['Modeled - ADDE-CL'].to_numpy().min(), DF_q['Observed'].to_numpy().min())
ymax = max(DF_q['Modeled - ADPSO-CL'].to_numpy().max(), DF_q['Modeled - ADDE-CL'].to_numpy().max(), DF_q['Observed'].to_numpy().max())
dif_v = ymax - ymin

plt.ylim(0, ymax + dif_v)
plt.ylabel('Streamflow ($m^{3}/s$)', fontsize = 18)
plt.xlabel('Years', fontsize = 18)
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
plt.title('Streamflow gauge', fontsize = 21, fontweight='bold')
plt.legend(loc='upper right', fontsize = 18)

plt.savefig(os.path.join(r'D:\1_PaperI\Graphs', 'Obs_vs_Sim_Q_.png'))
plt.clf()

#---    Observation wells
obs_well = pd.read_csv(r'..\data\ObservedData\Wells_observed.csv', skiprows = 3)
obs_well = obs_well.iloc[36:,:]
obs_well = obs_well.set_index(pd.to_datetime(df_q.index))
#print(obs_well)

ow = obs_well.columns

#---    ADPSO-CL
sim_well = pd.read_csv(os.path.join(path_results, best_experiment, best_result, 'iter_' + str(best_iteration), best_w), skiprows = 3)
sim_well = sim_well.iloc[36:,:]
sim_well = sim_well.set_index(pd.to_datetime(df_q.index))

#---    ADDE-CL
sim_well_2 = pd.read_csv(os.path.join(path_results_2, best_experiment_2, best_result_2, 'iter_' + str(best_iteration_2), best_w_2), skiprows = 3)
sim_well_2 = sim_well_2.iloc[36:,:]
sim_well_2 = sim_well_2.set_index(pd.to_datetime(df_q_2.index))
#print(sim_well)

for p in ow[1:]:
    print(p)

    print('DPSO')
    #---    Metrics
    rmse_w = he.evaluator(he.rmse, sim_well[p], obs_well[p])
    nse_w = he.evaluator(he.nse, sim_well[p], obs_well[p])
    kge_w, r, alpha, beta = he.evaluator(he.kge, sim_well[p], obs_well[p]) # kge, r, alpha, beta
    pbias_w = he.evaluator(he.pbias, sim_well[p], obs_well[p])
    mae_w = mean_absolute_error(obs_well[p], sim_well[p])
    r2_w = r2_score(obs_well[p], sim_well[p])
    print(round(rmse_w[0],3), round(nse_w[0],3), round(kge_w[0],3), round(r2_w,3))

    print('DDE')
    #---    Metrics
    rmse_w_2 = he.evaluator(he.rmse, sim_well_2[p], obs_well[p])
    nse_w_2 = he.evaluator(he.nse, sim_well_2[p], obs_well[p])
    kge_w_2, r_2, alpha_2, beta_2 = he.evaluator(he.kge, sim_well_2[p], obs_well[p]) # kge, r, alpha, beta
    pbias_w_2 = he.evaluator(he.pbias, sim_well_2[p], obs_well[p])
    mae_w_2 = mean_absolute_error(obs_well[p], sim_well_2[p])
    r2_w_2 = r2_score(obs_well[p], sim_well_2[p])
    print(round(rmse_w_2[0],3), round(nse_w_2[0],3), round(kge_w_2[0],3), round(r2_w_2,3))

    #---    Graph
    fig = plt.subplots(figsize=(14, 7))
    plt.plot(obs_well[p], label = 'Obs', color = "black", linewidth = 0.75)
    plt.plot(sim_well[p], label = 'ADPSO-CL', color = "red", linewidth = 0.75)
    plt.plot(sim_well_2[p], label = 'ADDE-CL', color = "blue", linewidth = 0.75)

    ymin = min(obs_well[p].to_numpy().min(), sim_well[p].to_numpy().min(), sim_well_2[p].to_numpy().min())
    ymax = max(obs_well[p].to_numpy().max(), sim_well[p].to_numpy().max(), sim_well_2[p].to_numpy().max())
    dif_v = ymax - ymin

    plt.ylim(ymin - (dif_v/10), ymax + dif_v)
    plt.ylabel('Groundwater table (m)', fontsize = 18)
    plt.xlabel('Years', fontsize = 18)
    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
    plt.title('Observation well - ' + str(p), fontsize = 21, fontweight='bold')
    plt.legend(loc='upper right', fontsize = 18)

    plt.savefig(os.path.join(r'D:\1_PaperI\Graphs', 'Obs_vs_Sim_Well_' + str(p) + '.png'))
    plt.clf()

"""


#---    Graph
fig = plt.subplots(figsize=(10, 6))
plt.plot(DF_q['Observed'], label = 'Obs', color = "black", linewidth = 0.25)
plt.plot(DF_q['Modeled'], label = 'DPSO', color = "red", linewidth = 0.25)
plt.plot(DF_q['Initial value'], label = 'Init', color = "blue", linewidth = 0.25)

ymin = min(DF_q['Modeled'].to_numpy().min(), DF_q['Observed'].to_numpy().min(), DF_q['Initial value'].to_numpy().min())
ymax = max(DF_q['Modeled'].to_numpy().max(), DF_q['Observed'].to_numpy().max(), DF_q['Initial value'].to_numpy().max())
dif_v = ymax - ymin

plt.ylim(0, ymax + dif_v)
plt.ylabel('Streamflow ($m^{3}/s$)', fontsize = 12)
plt.xlabel('Years', fontsize = 12)
plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
plt.title('Streamflow gauge', fontsize = 16, fontweight='bold')

fs_text = 8
plt.text(13200, ymax + dif_v - dif_v/8, 'NSE:    ' + str(round(nse_q[0],3)), fontsize = fs_text)
plt.text(13200, ymax + dif_v - 2*(dif_v/8), 'KGE:    ' + str(round(kge_q[0],3)), fontsize = fs_text)
plt.text(13200, ymax + dif_v - 3*(dif_v/8), 'PBIAS: ' + str(round(pbias_q[0],3)), fontsize = fs_text)
plt.text(13200, ymax + dif_v - 4*(dif_v/8), 'RMSE: ' + str(round(rmse_q[0],3)) + ' $m^{3}/s$', fontsize = fs_text)
plt.text(13200, ymax + dif_v - 5*(dif_v/8), 'MAE:   ' + str(round(mae_q,3)) + ' $m^{3}/s$', fontsize = fs_text)
plt.text(13200, ymax + dif_v - 6*(dif_v/8), '$R^{2}$:      ' + str(round(r2_q,3)), fontsize = fs_text)

plt.savefig(os.path.join(path_results, best_experiment, 'Graficas', 'Q_' + methodology + '_' + best_experiment + '.png'))
plt.clf()

#---    Observation wells
obs_well = pd.read_csv(r'..\data\ObservedData\Wells_observed.csv', skiprows = 3)
obs_well = obs_well.iloc[36:,:]
obs_well = obs_well.set_index(pd.to_datetime(df_q.index))
#print(obs_well)

ow = obs_well.columns

sim_well = pd.read_csv(os.path.join(path_results, best_experiment, best_result, 'iter_' + str(best_iteration), best_w), skiprows = 3)
sim_well = sim_well.iloc[36:,:]
sim_well = sim_well.set_index(pd.to_datetime(df_q.index))
#print(sim_well)

init_well = pd.read_csv(os.path.join(r'..\results_base', elements_init, 'Wells_simulation.csv'), skiprows = 3)
init_well = init_well.iloc[36:,:]
init_well = init_well.set_index(pd.to_datetime(df_q.index))
#print(init_well)

for p in ow[1:]:
    #---    Metrics
    rmse_w = he.evaluator(he.rmse, sim_well[p], obs_well[p])
    nse_w = he.evaluator(he.nse, sim_well[p], obs_well[p])
    kge_w, r, alpha, beta = he.evaluator(he.kge, sim_well[p], obs_well[p]) # kge, r, alpha, beta
    pbias_w = he.evaluator(he.pbias, sim_well[p], obs_well[p])
    mae_w = mean_absolute_error(obs_well[p], sim_well[p])
    r2_w = r2_score(obs_well[p], sim_well[p])

    #---    Graph
    fig = plt.subplots(figsize=(10, 6))
    plt.plot(obs_well[p], label = 'Obs', color = "black", linewidth = 0.25)
    plt.plot(sim_well[p], label = 'DPSO', color = "red", linewidth = 0.25)
    plt.plot(init_well[p], label = 'Init', color = "blue", linewidth = 0.25)

    ymin = min(obs_well[p].to_numpy().min(), sim_well[p].to_numpy().min(), init_well[p].to_numpy().min())
    ymax = max(obs_well[p].to_numpy().max(), sim_well[p].to_numpy().max(), init_well[p].to_numpy().max())
    dif_v = ymax - ymin

    plt.ylim(ymin - (dif_v/10), ymax + dif_v)
    plt.ylabel('Groundwater table (m)', fontsize = 12)
    plt.xlabel('Years', fontsize = 12)
    plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
    plt.title('Observation well - ' + str(p), fontsize = 16, fontweight='bold')

    fs_text = 8
    plt.text(13200, ymax + dif_v - dif_v/8, 'NSE:    ' + str(round(nse_w[0],3)), fontsize = fs_text)
    plt.text(13200, ymax + dif_v - 2*(dif_v/8), 'KGE:    ' + str(round(kge_w[0],3)), fontsize = fs_text)
    plt.text(13200, ymax + dif_v - 3*(dif_v/8), 'PBIAS: ' + str(round(pbias_w[0],3)), fontsize = fs_text)
    plt.text(13200, ymax + dif_v - 4*(dif_v/8), 'RMSE: ' + str(round(rmse_w[0],3)) + ' $m^{3}/s$', fontsize = fs_text)
    plt.text(13200, ymax + dif_v - 5*(dif_v/8), 'MAE:   ' + str(round(mae_w,3)) + ' $m^{3}/s$', fontsize = fs_text)
    plt.text(13200, ymax + dif_v - 6*(dif_v/8), '$R^{2}$:      ' + str(round(r2_w,3)), fontsize = fs_text)

    plt.savefig(os.path.join(path_results, best_experiment, 'Graficas', 'Obs_well_' + str(p) + '_' + methodology + '_' + best_experiment + '.png'))
    plt.clf()
"""




"""
#---    ERROR PORCENTUAL - K y Sy
shape = gpd.read_file(os.path.join(path_results, best_experiment, best_result, 'iter_' + str(best_iteration), best_shape))
shape_obs = gpd.read_file(r'..\data\GIS\Final_version\Elements_FA_vf.shp')

for n in variables:
    globals()[n + '_obs'] = shape_obs[n]
    globals()[n + '_sim'] = shape[n]

    locals()['dif_' + n] = abs(globals()[n + '_sim'] - globals()[n + '_obs'])   
    globals()['error_' + n] = (locals()['dif_' + n] / globals()[n + '_obs']) * 100
    #globals()['error_' + n] = globals()['error_' + n].fillna(0)

    globals()['matriz_error_' + n] = (globals()['error_' + n].to_numpy()).reshape((84, 185))

    #---    Graph
    plt.figure(figsize = (16,8))
    plt.imshow(globals()['matriz_error_' + n], cmap = 'viridis')

    im_ratio = globals()['matriz_error_' + n].shape[0]/globals()['matriz_error_' + n].shape[1]
    plt.colorbar(fraction=0.047*im_ratio, extend='max')
    plt.clim(0, 100)

    plt.title('Relative error (%) - ' + n)
    plt.xlabel('Column')
    plt.ylabel('Row')
    
    plt.savefig(os.path.join(path_results, best_experiment, 'Graficas', 'Error_relativo_' + n + '_' + methodology + '_' + best_experiment + '.png'))
    plt.clf()
    
    #---    Graph 2
    plt.figure(figsize = (16,8))
    plt.imshow(globals()['matriz_error_' + n], cmap = 'viridis')

    im_ratio = globals()['matriz_error_' + n].shape[0]/globals()['matriz_error_' + n].shape[1]
    plt.colorbar(fraction=0.047*im_ratio, extend='max')
    plt.clim(0, 1000)

    plt.title('Relative error (%) - ' + n)
    plt.xlabel('Column')
    plt.ylabel('Row')
    
    plt.savefig(os.path.join(path_results, best_experiment, 'Graficas', 'Error_relativo_2_' + n + '_' + methodology + '_' + best_experiment + '.png'))
    plt.clf()
"""