import  numpy as np
from functools import reduce
from scipy.stats.qmc import LatinHypercube,scale

a = np.array([1, 2, 3])
b = np.copy(a)
print(b)