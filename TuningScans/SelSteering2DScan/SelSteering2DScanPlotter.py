# This script will get the efficiency from the simulated data files and plot as a function of energy and cone size

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import os
import csv

datadir = 'ke_20_sel_-1870'
gen_plots = False

os.chdir(os.path.realpath(os.path.dirname(__file__))+'\\data\\'+datadir)
"""
# look for csv file and import
for f in os.listdir():
    if f.split('.')[-1] != 'csv':
        continue
    if f == 'ExtractionSteering2DScan_data.csv':
        continue
    print(f)
    data = pd.read_csv(f, delimiter=',', skiprows=6)
"""
f = 'IonStartLocationSteering_ke_20_sel_1870.csv'
data = pd.read_csv(f,delimiter = ',', skiprows = 4)
y_vals = data['Ypos'].unique()
z_vals = np.sort(data['Zpos'].unique())
p_step = y_vals[1] - y_vals[0]
exty_vals = data['Sel_x'].unique()
extz_vals = np.sort(data['Sel_z'].unique())
ext_step = exty_vals[1] - exty_vals[0]

scan_min = []
exty_min = []
extz_min = []
y_plot = []
z_plot =[]
scan_min_file = open('ExtractionSteering2DScan_data.csv', 'w', newline='')
writer = csv.writer(scan_min_file)
writer.writerow(['Ypos','Zpos','Scan_min','Sel_x_min','Sel_z_min'])

data_slice = data.groupby(['Ypos'])
for y in y_vals:
    #Take the data grouped for each y in y_vals
    data_yslice = data_slice.get_group(y).groupby(['Zpos'])
    print('Y =',y)
    for z in z_vals:
        if z in data_yslice['Zpos'].unique():
            #Take the data grouped for each z in z_vals
            data_zslice = data_yslice.get_group(z).groupby(['Sel_x'])
            scan_data, exty_plot, extz_plot = [], [], []
            for exty in exty_vals:
                #Take the data grouped for each SEL_x value 
                data_eyslice = data_zslice.get_group(exty).groupby(['Sel_z'])
                for extz in extz_vals:
                    data_ezslice = data_eyslice.get_group(extz)
                    if not math.isnan(data_ezslice['IonPosition']):
                        scan_data.append(float(data_ezslice['IonPosition']))
                        exty_plot.append(exty)
                        extz_plot.append(extz)
            if not len(scan_data) ==0:
                scan_min.append(min(scan_data))
                exty_min.append(exty_plot[np.argmin(scan_data)])
                extz_min.append(extz_plot[np.argmin(scan_data)])
                y_plot.append(y)
                z_plot.append(z)
                if gen_plots == True:
                    plt.figure(str(y)+','+str(z))
                    plt.scatter(exty_plot, extz_plot, c=scan_data, s=10)
                    plt.plot(exty_min[-1], extz_min[-1], 'ro', ms=5)
                    plt.xlabel('X Sel Steering (V)')
                    plt.ylabel('Z Sel Steering (V)')
                    plt.xlim(min(exty_vals)-ext_step, max(exty_vals)+ext_step)
                    plt.ylim(min(extz_vals)-ext_step, max(extz_vals)+ext_step)
                    plt.colorbar(label="Ion displacement from axis in bender plane (mm)")
                    plt.title('Extraction Steering Sweep\nIon Start Position: ('+str(y)+', '+str(z)+')')
                    plt.gca().set_aspect('equal')
                    plt.tight_layout()
                    plt.savefig('SelScan_x_'+str(y)+'_z_'+str(z)+'.png')
                    plt.close()

plt.figure('MinimumDistance')
plt.scatter(y_plot,z_plot,c=scan_min, s=10)
plt.xlabel('Y Position (mm)')
plt.ylabel('Z Position(mm)')
plt.xlim(min(y_plot)-p_step, max(y_plot)+p_step)
plt.ylim(min(z_plot)-p_step, max(z_plot)+p_step)
plt.colorbar(label="Minimum Distance (mm)")
plt.title('Minimum Distance from Optical Axis in SEL')
plt.gca().set_aspect('equal')
plt.tight_layout()
plt.savefig('MinimumAxialDistance.png')

plt.figure('BestSelYSteering')
plt.scatter(y_plot,z_plot,c=exty_min, s=10)
plt.xlabel('Y Position (mm)')
plt.ylabel('Z Position(mm)')
plt.xlim(min(y_plot)-p_step, max(y_plot)+p_step)
plt.ylim(min(z_plot)-p_step, max(z_plot)+p_step)
plt.colorbar(label="Optimal X Sel Steering (V)")
plt.title('X-axis Sel Steering')
plt.gca().set_aspect('equal')
plt.tight_layout()
plt.savefig('OptimalXaxisSteeringSweep.png')

plt.figure('BestSelZSteering')
plt.scatter(y_plot,z_plot,c=extz_min, s=10)
plt.xlabel('Y Position (mm)')
plt.ylabel('Z Position(mm)')
plt.xlim(min(y_plot)-p_step, max(y_plot)+p_step)
plt.ylim(min(z_plot)-p_step, max(z_plot)+p_step)
plt.colorbar(label="Optimal Z Sel Steering (V)")
plt.title('Z-axis Sel Steering')
plt.gca().set_aspect('equal')
plt.tight_layout()
plt.savefig('OptimalZaxisSteeringSweep.png')

# make 1-D plot using average of each row(column) of scan for the optimal z(x) steering

# get average x and z steering for each y position on target
y_avg_xsteer, y_avg_zsteer = [], []
for y in y_vals:
    vals, vals2 = [], []
    for i in range(len(y_plot)):
        if y_plot[i] == y:
            vals.append(exty_min[i])
            vals2.append(extz_min[i])
    y_avg_xsteer.append(np.mean(vals))
    y_avg_zsteer.append(np.mean(vals2))

# plot the avearge x steering
plt.figure('Y-axis X Steering')
plt.plot(y_vals,y_avg_xsteer, 'bo')
plt.xlabel('Y Position (mm)')
plt.ylabel('Average Optimal X Steering (V)')
plt.xlim(min(y_plot)-p_step, max(y_plot)+p_step)
plt.tight_layout()
plt.savefig('OptimalYaxisXSteering1D.png')

# plot the average y steering
plt.figure('Y-axis Z Steering')
plt.plot(y_vals,y_avg_zsteer, 'bo')
plt.xlabel('Y Position (mm)')
plt.ylabel('Average Optimal Z Steering (V)')
plt.xlim(min(y_plot)-p_step, max(y_plot)+p_step)
plt.tight_layout()
plt.savefig('OptimalYaxisZSteering1D.png')

# get average x and z steering for each z position on target
z_avg_xsteer, z_avg_zsteer = [], []
for z in z_vals:
    vals, vals2 = [], []
    for i in range(len(z_plot)):
        if z_plot[i] == z:
            vals.append(exty_min[i])
            vals2.append(extz_min[i])
    z_avg_xsteer.append(np.mean(vals))
    z_avg_zsteer.append(np.mean(vals2))

# plot the average x steering
plt.figure('Z-axis X Steering')
plt.plot(z_vals,z_avg_xsteer, 'bo')
plt.xlabel('Z Position (mm)')
plt.ylabel('Average Optimal X Steering (V)')
plt.xlim(min(z_plot)-p_step, max(z_plot)+p_step)
plt.tight_layout()
plt.savefig('OptimalZaxisXSteering1D.png')

# plot the average z steering
plt.figure('Z-axis Z Steering')
plt.plot(z_vals,z_avg_zsteer, 'bo')
plt.xlabel('Z Position (mm)')
plt.ylabel('Average Optimal Z Steering (V)')
plt.xlim(min(z_plot)-p_step, max(z_plot)+p_step)
plt.tight_layout()
plt.savefig('OptimalZaxisZSteering1D.png')


data2write = np.transpose(np.vstack((y_plot,z_plot,scan_min,exty_min,extz_min)))
writer.writerows(data2write)
scan_min_file.close()

plt.show()
