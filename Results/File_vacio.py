import h5py

FINAL_ITERATION = 202
n_var = 15119

with h5py.File('DPSO_historial.h5', 'w') as f:
    iter_h5py = f.create_dataset("iteration", (FINAL_ITERATION, 1))
    pob_x_h5py = f.create_dataset("pob_x", (FINAL_ITERATION, n_var))
    pob_y_h5py = f.create_dataset("pob_y", (FINAL_ITERATION, 1))
    pob_v_h5py = f.create_dataset("pob_v", (FINAL_ITERATION, n_var))
    pob_x_best_h5py = f.create_dataset("pob_x_best", (FINAL_ITERATION, n_var))
    pob_y_best_h5py = f.create_dataset("pob_y_best", (FINAL_ITERATION, 1))
    pob_w_h5py = f.create_dataset("w", (FINAL_ITERATION, 1))