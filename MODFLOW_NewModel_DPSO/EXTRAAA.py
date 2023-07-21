##### METHODOLOGY

    pob.y = y_init
    pob.y_best = y_init

    #---    Create iteration register file
    with h5py.File('DPSO_historial.h5', 'w') as f:
        iter_h5py = f.create_dataset("iteration", (FINAL_ITERATION, 1))
        pob_x_h5py = f.create_dataset("pob_x", (FINAL_ITERATION, n_var))
        pob_y_h5py = f.create_dataset("pob_y", (FINAL_ITERATION, 1))
        pob_v_h5py = f.create_dataset("pob_v", (FINAL_ITERATION, n_var))
        pob_x_best_h5py = f.create_dataset("pob_x_best", (FINAL_ITERATION, n_var))
        pob_y_best_h5py = f.create_dataset("pob_y_best", (FINAL_ITERATION, 1))
        pob_w_h5py = f.create_dataset("w", (FINAL_ITERATION, 1))

    #---    Iteration register
        iter_h5py[0] = ITERATION
        pob_x_h5py[0] = np.copy(pob.x)
        pob_y_h5py[0] = pob.y
        pob_v_h5py[0] = np.copy(pob.v)
        pob_x_best_h5py[0] = np.copy(pob.x_best)
        pob_y_best_h5py[0] = pob.y_best
        pob_w_h5py[0] = 0.5
    f.close()

else:
    #---    PSO
    α = 0.8                                                    # Cognitive scaling parameter  # 0.8 # 1.49
    β = 0.8                                                    # Social scaling parameter     # 0.8 # 1.49
    #w = 0.5                                                    # inertia velocity
    w_min = 0.4                                                 # minimum value for the inertia velocity
    w_max = 0.9                                                 # maximum value for the inertia velocity
    vMax = np.around(np.multiply(u_bounds-l_bounds,0.8),4)      # Max velocity # De 0.8 a 0.4
    vMin = -vMax                                                # Min velocity

    with h5py.File('DPSO_historial.h5', 'r') as f:
        pob.x = np.copy(f["pob_x"][ITERATION - 1])
        pob.y = f["pob_y"][ITERATION - 1]
        pob.v = np.copy(f["pob_v"][ITERATION - 1])
        pob.x_best = np.copy(f["pob_x_best"][ITERATION - 1])
        pob.y_best = f["pob_y_best"][ITERATION - 1]

        w = f["w"][ITERATION - 1]
    f.close()
    
    gbest = send_request_py(IP_SERVER_ADD, pob.y, pob.x)           # Update global particle
    
    time.sleep(1)

    #---    Update particle velocity
    ϵ1,ϵ2 = np.around(np.random.uniform(),4), np.around(np.random.uniform(),4)            # [0, 1]

    pob.v = np.around(np.around(w*pob.v,4) + np.around(α*ϵ1*(pob.x_best - pob.x),4) + np.around(β*ϵ2*(gbest - pob.x),4),4)

    #---    Adjust particle velocity
    index_vMax = np.where(pob.v > vMax)
    index_vMin = np.where(pob.v < vMin)

    if np.array(index_vMax).size > 0:
        pob.v[index_vMax] = vMax[index_vMax]
    if np.array(index_vMin).size > 0:
        pob.v[index_vMin] = vMin[index_vMin]

    #---    Update particle position
    pob.x += pob.v

    #---    Adjust particle position
    index_pMax = np.where(pob.x > u_bounds)
    index_pMin = np.where(pob.x < l_bounds)

    if np.array(index_pMax).size > 0:
        pob.x[index_pMax] = u_bounds[index_pMax]
    if np.array(index_pMin).size > 0:
        pob.x[index_pMin] = l_bounds[index_pMin]

    #---    Evaluate the fitnness function
    y = Run_WEAP_MODFLOW(path_output, str(ITERATION), initial_shape_HP, HP, active_cells, pob.x, n_var_1, n_var_2, n_var, 
                         k_shape_1, k_shape_2, active_matriz, path_init_model, path_model, path_nwt_exe, 
                         path_obs_data)
    #gbest = send_request_py(IP_SERVER_ADD, y, pob.x)
    
    if y < pob.y_best:
        pob.x_best = np.copy(pob.x)
        pob.y_best = y
        pob.y = y
    else:
        pob.y = y

    #---    Update the inertia velocity
    w = w_max - (ITERATION) * ((w_max-w_min)/FINAL_ITERATION)

    #---    Iteration register
    with h5py.File('DPSO_historial.h5', 'a') as f:
        f["iteration"][ITERATION] = ITERATION
        f["pob_x"][ITERATION] = np.copy(pob.x)
        f["pob_y"][ITERATION] = pob.y
        f["pob_v"][ITERATION] = np.copy(pob.v)
        f["pob_x_best"][ITERATION] = np.copy(pob.x_best)
        f["pob_y_best"][ITERATION] = pob.y_best

        f["w"][ITERATION] = w
    f.close()


##########  FUNCTIONS


    #---    Generate new native files
    model = fpm.Modflow.load(path_init_model + '/SyntheticAquifer_NY.nam', version = 'mfnwt', exe_name = path_nwt_exe)
    model.write_input()
    model.remove_package("UPW")
    upw = fpm.ModflowUpw(model = model, laytyp=1, layavg=0, chani=-1.0, layvka=0, laywet=0, hdry=-888, iphdry=1, hk=matriz_kx, hani=1.0, vka=matriz_kz, ss=matriz_ss, sy=matriz_sy, extension='upw')
    upw.write_file()
    model.run_model()
    
    #---    Move native files to WEAP
    get_old_files = os.listdir(path_model)
    get_new_files = os.listdir(os.getcwd())

    #---    Delete old files
    for g in get_old_files:
        try:
            os.remove(os.path.join(path_model, g))
        except:
            print('No hay archivos')

    #---    Move new files
    for h in get_new_files:
        if h.endswith('.py') or h == '__pycache__' or h == 'sp' or h.endswith('.txt') or h == 'output' or h.endswith('.ps1') or h.endswith('.h5') or h == 'PRUEBAAAAAAS':
            pass 
        else:
            shutil.move(os.path.join(os.getcwd(), h), os.path.join(path_model, h))
    
    #-------------------------------------
    #---    Run WEAP-MODFLOW model    ----
    #-------------------------------------
    WEAP = win32.Dispatch("WEAP.WEAPApplication")
    WEAP.ActiveArea = "SyntheticProblem_WEAPMODFLOW"
    WEAP.Calculate()

    #---    Export results
    favorites = pd.read_excel(r"C:\Users\vagrant\Documents\MODFLOW_Calibration\data\Favorites_WEAP.xlsx")
    for i,j in zip(favorites["BranchVariable"],favorites["WEAP Export"]):
        WEAP.LoadFavorite(i)
        WEAP.ExportResults(os.path.join(dir_iteration, f"iter_{str(iteration)}_{j}.csv"), True, True, True, False, False)

    #---------------------------------
    #---    Objective Function    ----
    #---------------------------------
    #---    Well analysis
    obs_well = get_data(os.path.join(path_obs_data, 'Wells_observed.csv'), 3)
    ow = obs_well.columns
    #print(ow)

    sim_well = get_data(os.path.join(dir_iteration, f"iter_{str(iteration)}_Wells_simulation.csv"), 3)

    g_srmse_well = 0
    srmse_well = 0
    for i in ow:
        if i == "OW51" or i == "OW87" or i == "OW97" or i == "OW100" or i == "OW157" or i == "OW167" or i == "OW181" or i == "OW188" or i == "OW233" or i == "OW234" or i == "OW235":
            g = 0.8 # 0.8
            #print(i, g)
        else:
            g = 0.8
            #print(i, g) 

        mse_well = mean_squared_error(obs_well[i], sim_well[i])
        rmse_well = math.sqrt(mse_well)
        g_rmse_well = g * rmse_well

        srmse_well += rmse_well
        g_srmse_well += g_rmse_well
    #print(srmse_well)

    #---    Streamflow analysis
    df_q = pd.read_csv(os.path.join(dir_iteration, f"iter_{str(iteration)}_Streamflow_gauges.csv"), skiprows = 3)
    df_q = df_q.set_index('Statistic')
    df_q = df_q.set_index(pd.to_datetime(df_q.index))
    df_q = df_q.iloc[36:,:]

    df_q_obs = get_data(os.path.join(path_obs_data, 'StreamflowGauges_KPR_vf.csv'), 2)
    
    mse_q = mean_squared_error(df_q_obs['Observed'], df_q['Modeled'])
    rmse_q = math.sqrt(mse_q)
    #print(rmse_q)

    #---    Subject to
    kx_min = 0.280
    kx_max = 67.056
    sy_min = 0.01
    sy_max = 0.1282

    for i in HP:
        globals()["vector_modif_" + str(i)] = get_eliminate_zeros(globals()["vector_" + str(i)].tolist())
        globals()["P_" + str(i)] = get_evaluate_st_bounds((locals()[str(i) + "_min"]), (locals()[str(i) + "_max"]), globals()["vector_modif_" + str(i)])

    #---    Total Objective Function
    #---    There are 31 observation wells and 1 streamflow gauge (32 monitoring elements. If each of them has the same weighting factor: 1/32 = 0.03125 (3.125%))
    #g1 = 0.6
    g2 = 0.6
    g3 = 0.6

    #of = g1*srmse_well + g2*rmse_q + g3*(P_kx + P_sy)
    #of = g1*srmse_well + g2*rmse_q
    of = g_srmse_well + g2*rmse_q + g3*(P_kx + P_sy)
    return of

### PRUEBA!!