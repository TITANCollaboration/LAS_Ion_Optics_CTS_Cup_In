# This script will get the efficiency from the simulated data files and plot as a function of energy and cone size

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import os
import csv

datadir = 'ke_20'
outputfile = 'ExtractionSteering2DScan_data.csv'
gen_plots = False

os.chdir(os.path.realpath(os.path.dirname(__file__))+'\\data\\'+datadir)

# look for csv file and import
for f in os.listdir():
    if f.split('.')[-1] != 'csv':
        continue
    if f == outputfile:
        continue
    data = pd.read_csv(f, delimiter=',', skiprows=6)

y_vals = data['Ypos'].unique()
z_vals = np.sort(data['Zpos'].unique())
p_step = y_vals[1] - y_vals[0]
exty_vals = data['Ext_y'].unique()
extz_vals = np.sort(data['Ext_z'].unique())
ext_step = exty_vals[1] - exty_vals[0]

scan_min = []
exty_min = []
extz_min = []
y_plot = []
z_plot =[]
scan_min_file = open(outputfile, 'w', newline='')
writer = csv.writer(scan_min_file)
writer.writerow(['Ypos','Zpos','Scan_min','Ext_y_min','Ext_z_min'])

data_slice = data.groupby(['Ypos'])
for y in y_vals:
    data_yslice = data_slice.get_group(y).groupby(['Zpos'])
    print('Y =',y)
    for z in z_vals:
        if z in data_yslice['Zpos'].unique():
            data_zslice = data_yslice.get_group(z).groupby(['Ext_y'])
            scan_data, exty_plot, extz_plot = [], [], []
            for exty in exty_vals:
                data_eyslice = data_zslice.get_group(exty).groupby(['Ext_z'])
                for extz in extz_vals:
                    data_ezslice = data_eyslice.get_group(extz)
                    if not math.isnan(data_ezslice['IonPosition']):
                        scan_data.append(float(data_ezslice['IonPosition']))
                        exty_plot.append(exty)
                        extz_plot.append(extz)
            scan_min.append(min(scan_data))
            exty_min.append(exty_plot[np.argmin(scan_data)])
            extz_min.append(extz_plot[np.argmin(scan_data)])
            y_plot.append(y)
            z_plot.append(z)
            if gen_plots == True:
                plt.figure(str(y)+','+str(z))
                plt.scatter(exty_plot, extz_plot, c=scan_data, s=10)
                plt.plot(exty_min, extz_min, 'ro', ms=5)
                plt.xlabel('Y Extraction Steering (V)')
                plt.ylabel('Z Extraction Steering (V)')
                plt.xlim(min(exty_vals)-ext_step, max(exty_vals)+ext_step)
                plt.ylim(min(extz_vals)-ext_step, max(extz_vals)+ext_step)
                plt.colorbar(label="Ion displacement from axis in bender plane (mm)")
                plt.title('Extraction Steering Sweep\nIon Start Position: ('+str(y)+', '+str(z)+')')
                plt.gca().set_aspect('equal')
                plt.tight_layout()
                plt.savefig('ExtractionAndBenderScan_y_'+str(y)+'_z_'+str(z)+'.png')
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

plt.figure('BestExtractionYSteering')
plt.scatter(y_plot,z_plot,c=exty_min, s=10)
plt.xlabel('Y Position (mm)')
plt.ylabel('Z Position(mm)')
plt.xlim(min(y_plot)-p_step, max(y_plot)+p_step)
plt.ylim(min(z_plot)-p_step, max(z_plot)+p_step)
plt.colorbar(label="Optimal Y Extraction Steering (V)")
plt.title('Y-axis Extraction Steering')
plt.gca().set_aspect('equal')
plt.tight_layout()
plt.savefig('OptimalYaxisSteeringSweep.png')

plt.figure('BestExtractionZSteering')
plt.scatter(y_plot,z_plot,c=extz_min, s=10)
plt.xlabel('Y Position (mm)')
plt.ylabel('Z Position(mm)')
plt.xlim(min(y_plot)-p_step, max(y_plot)+p_step)
plt.ylim(min(z_plot)-p_step, max(z_plot)+p_step)
plt.colorbar(label="Optimal Z Extraction Steering (V)")
plt.title('Z-axis Extraction Steering')
plt.gca().set_aspect('equal')
plt.tight_layout()
plt.savefig('OptimalZaxisSteeringSweep.png')

data2write = np.transpose(np.vstack((y_plot,z_plot,scan_min,exty_min,extz_min)))
writer.writerows(data2write)
scan_min_file.close()

plt.show()