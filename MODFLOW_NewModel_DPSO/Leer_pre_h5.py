# -*- coding: utf-8 -*-

#---    Packages
import h5py
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

path = 'PRE_DPSO_historial.h5'

with h5py.File(path, 'r') as f:
    x = f["pob_x"][:]

print(x[34])