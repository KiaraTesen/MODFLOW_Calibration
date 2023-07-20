# -*- coding: utf-8 -*-

#---    Packages
from Functions_DDE_SCL_CCL import *
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

#---    Configure IP and PORT
#MY_IP = sys.argv[1]  
#MY_PORT = sys.argv[2]
VM = int(sys.argv[1])
print(VM)

MY_IP = f"10.0.0.{10+VM}"
print(MY_IP)
MY_IP_PORT = f"{MY_IP}:8888"

ITERATION = int(sys.argv[2])
TOTAL_ITERATION = int(sys.argv[3])
FINAL_ITERATION = int(sys.argv[4])

VMS = int(sys.argv[5])

