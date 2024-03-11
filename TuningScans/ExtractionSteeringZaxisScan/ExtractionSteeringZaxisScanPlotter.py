# This script will get the efficiency from the simulated data files and plot as a function of energy and cone size

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mycolorpy import colorlist as mcp
import scipy.optimize as opt
import os

datadir = 'ke_20'
gen_plots = False

os.chdir(os.path.realpath(os.path.dirname(__file__))+'\\data\\'+datadir)

# look for csv file and import
for f in os.listdir():
    if f.split('.')[-1] != 'csv':
        continue
    data = pd.read_csv(f, delimiter=',', skiprows=6)

z_vals = data['Zpos'].unique()
z_step = z_vals[1] - z_vals[0]
extz_vals = data['Ext_z'].unique()
extz_step = extz_vals[1] - extz_vals[0]

scan_data = []
z_vals2 = []
extz_vals2 = []

data_z = data.groupby(['Zpos'])
for z in z_vals:
    data_extz = data_z.get_group(z).groupby(['Ext_z'])
    for extz in extz_vals:
        data_slice = data_extz.get_group(extz)
        if len(data_slice) != 0:
            scan_data.append(data_slice['IonPosition'])
            extz_vals2.append(extz)
            z_vals2.append(z)

plt.figure('zscan')
plt.scatter(z_vals2,extz_vals2,c=scan_data)
plt.ylabel('Extraction Steering (V)')
plt.xlabel('Z Start Position (mm)')
plt.colorbar(label="Ion displacement from axis in bender plane (mm)")
plt.title('Extraction Z Steering Sweep')
plt.ylim(min(extz_vals) - extz_step, max(extz_vals) + extz_step)
plt.xlim(min(z_vals) - z_step, max(z_vals) + z_step)
plt.tight_layout()
plt.savefig('ExtractionZaxisScan.png')

plt.show()