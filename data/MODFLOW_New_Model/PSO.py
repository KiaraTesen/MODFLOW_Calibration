import numpy as np
from functools import reduce
from scipy.stats.qmc import LatinHypercube,scale


# Tamaño de la población
n = 400

# Número de variables
kernel_shape = (5,5)
n_kernels = 1
n_hp = 3
n_var = reduce(lambda x,y: x*y, kernel_shape)*n_kernels*n_hp
#print(n_var, np.repeat(-5,75))

engine = LatinHypercube(d=n_var)
sample = engine.random(n=n)

l_bounds = np.repeat(-5,75)
u_bounds = np.repeat(5,75) #np.array([-5,-5,-5])

sample_scaled = scale(sample,l_bounds, u_bounds)
print(sample_scaled)
print(len(sample_scaled))
