# This script will get the efficiency from the simulated data files and plot as a function of energy and cone size

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mycolorpy import colorlist as mcp
import scipy.optimize as opt
import os

datadir = 'ke_40'
gen_plots = False

os.chdir(os.path.realpath(os.path.dirname(__file__))+'\\data\\'+datadir)

# look for csv file and import
for f in os.listdir():
    if f.split('.')[-1] != 'csv':
        continue
    data = pd.read_csv(f, delimiter=',', skiprows=6)

y_vals = data['Ypos'].unique()
exty_vals = data['Ext_y'].unique()
bend_vals = data['Bender'].unique()
exty_step = exty_vals[1] - exty_vals[0]
bend_step = bend_vals[1] - bend_vals[0]
bend_centers = bend_vals

scan_data = []
exty_best = []

data_y = data.groupby(['Ypos'])
for y in y_vals:
    sd, exty_vals2, bend_vals2 = [], [], []
    data_bend = data_y.get_group(y).groupby(['Bender'])
    for bend_center in bend_centers:
        data_bend_center = data_bend.get_group(bend_center)
        best_val = data_bend_center['IonPosition'].idxmin()
        if not math.isnan(best_val):
            exty_best.append(np.float64(data_bend_center['Ext_y'].loc[best_val]))
            if abs(exty_best[-1] - exty_best[-2]) > 2*bend_step:
                exty_best[-1] = np.float64('nan')
        if math.isnan(best_val):
            exty_best.append(np.float64('nan'))
    for bend in bend_vals:
        data_exty = data_bend.get_group(bend).groupby(['Ext_y'])
        for exty in exty_vals:
            data_slice = data_exty.get_group(exty)
            if len(data_slice) != 0:
                sd.append(data_slice['IonPosition'])
                exty_vals2.append(exty)
                bend_vals2.append(bend)
    if gen_plots == True:
        plt.figure('y='+str(y))
        plt.scatter(bend_vals2,exty_vals2,c=sd)
        plt.ylabel('Extraction Steering (V)')
        plt.xlabel('Bender Voltage (V)')
        plt.colorbar(label="Ion displacement from axis in bender plane (mm)")
        plt.title('Extraction/Bender Steering Sweep\nIon Start Position: ('+str(y)+', 35)')
        plt.ylim(min(exty_vals) - exty_step, max(exty_vals) + exty_step)
        plt.xlim(min(bend_vals) - bend_step, max(bend_vals) + bend_step)
        plt.tight_layout()
        plt.savefig('ExtractionAndBenderScan_y_'+str(y)+'.png')
    scan_data.append(sd)

exty_best = np.reshape(exty_best,(len(y_vals), len(bend_centers)))
exty_best_center = np.mean(exty_best[:,5:10], axis=1)
exty_is_nan = np.argwhere(np.isnan(exty_best_center))[:,0]
exty_best_center = np.delete(exty_best_center,exty_is_nan)
y_vals_center = np.delete(y_vals,exty_is_nan)

y_val_lim = [np.where(y_vals == 31.1)[0][0], np.where(y_vals == 38.9)[0][0]]
def line(x,m,b):
    return m*x + b
popt,cov = opt.curve_fit(line,y_vals_center[y_val_lim[0]:y_val_lim[1]],exty_best_center[y_val_lim[0]:y_val_lim[1]],p0=[-40,2000])

plt.figure('BendCenter')
col = mcp.gen_color(cmap="jet",n=len(bend_centers))
for i in range(len(bend_centers)):
    plt.plot(y_vals,exty_best[:,i],marker='o',linestyle='None',color=col[i],label=str(bend_centers[i])+'V')
#plt.vlines([31,39],[min(exty_vals)],[max(exty_vals)],linestyles='--',color='k')
plt.plot(y_vals, line(y_vals,popt[0],popt[1]), 'k--')
plt.xlabel('Ion Y Start Position')
plt.ylabel('Best Value for Extraction Y-axis Steering')
plt.title('Optimal Extraction Y-axis Steering')
plt.legend(loc=1, title="Bender Voltage")
plt.xlim(30,43)
plt.text(34,275,'Slope: '+str(round(popt[0]))+' V/mm on target\nIntercept: '+str(round(popt[1]))+' V')
plt.tight_layout()
plt.savefig('Ext_y_Optimum.png')

plt.show()