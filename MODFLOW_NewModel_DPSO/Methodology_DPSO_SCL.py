# -*- coding: utf-8 -*-

#---    Packages
from Functions_DPSO_SCL import *
import geopandas as gpd
import pandas as pd
import numpy as np
import h5py
import matplotlib.pyplot as plt
import os
from functools import reduce
import time
import sys
from request_server.request_server import send_request_py
import warnings
warnings.filterwarnings('ignore')

IP_SERVER_ADD = sys.argv[1]
ITERATION = int(sys.argv[2])
TOTAL_ITERATION = int(sys.argv[3])
FINAL_ITERATION = int(sys.argv[4])

print(FINAL_ITERATION)

