import matplotlib.pyplot as plt
import numpy as np

file = 'C:\\Users\\ethan\\Github_Repositories\\LAS_Ion_Optics_CTS_Cup_In\\TuningScans\\AllFullTarget\\data\\ke_20\\2DElectrodeScan_extLens1_extLens2_ke_20_centered_-2500_1500_nvolts_25.csv'
file = 'C:\\Users\\ethan\\Github_Repositories\\LAS_Ion_Optics_CTS_Cup_In\\TuningScans\\AllFullTarget\\data\\ke_20\\2DElectrodeScan_extLens1_selFocus_ke_20_centered_-2500_-1800_nvolts_15.csv'
file = 'C:\\Users\\ethan\\Github_Repositories\\LAS_Ion_Optics_CTS_Cup_In\\TuningScans\\AllFullTarget\\data\\ke_20\\2DElectrodeScan_extLens1_selFocus_ke_20_centered_-2800_-1550_nvolts_15.csv'
file = 'C:\\Users\\ethan\\Github_Repositories\\LAS_Ion_Optics_CTS_Cup_In\\TuningScans\\AllFullTarget\\data\\ke_20\\2DElectrodeScan_extLens1_extLens2_ke_20_centered_1000_1200_nvolts_25.csv'
file = 'C:\\Users\\ethan\\Github_Repositories\\LAS_Ion_Optics_CTS_Cup_In\\TuningScans\\AllFullTarget\\data\\ke_20\\2DElectrodeScan_extLens1_extLens2_ke_20_centered_800_1000_nvolts_25.csv'
file = 'C:\\Users\\ethan\\Github_Repositories\\LAS_Ion_Optics_CTS_Cup_In\\TuningScans\\AllFullTarget\\data\\ke_20\\2DElectrodeScan_selFocus_extLens2_ke_20_centered_-1525_925_nvolts_20.csv'
file = 'C:\\Users\\ethan\\Github_Repositories\\LAS_Ion_Optics_CTS_Cup_In\\TuningScans\\AllFullTarget\\data\\ke_20\\2DElectrodeScan_selFocus_extLens2_ke_20_centered_-1800_925_nvolts_20.csv'
file = 'C:\\Users\\ethan\\Github_Repositories\\LAS_Ion_Optics_CTS_Cup_In\\TuningScans\\AllFullTarget\\data\\ke_20\\2DElectrodeScan_selFocus_extLens1_ke_20_centered_-1850_800_nvolts_20.csv'
data = np.loadtxt(file,skiprows = 2, delimiter=',', usecols = [0,1,2,3])
e1 = data[:,0]
e2 = data[:,1]
efficiency = data[:,2]
#mean_dist = data[:,3]
#med_dist = data[:,4]
#max_dist = data[:,5]
#min_dist = data[:,6]

print(np.mean(efficiency))
plt.figure('Efficiency Distance Bender Center')
plt.scatter(e1,e2,c=efficiency, s =20)
plt.xlabel('e1 (V)')
plt.ylabel('e2 (V)')
plt.colorbar(label="Efficiency")
plt.title('Efficiency at Faraday Cup')
plt.gca().set_aspect('equal')
plt.tight_layout()

"""
plt.figure('Maximum Distance Bender Center')
plt.scatter(e1,e2,c=max_dist, s =20)
plt.xlabel('Ext Lens1 (V)')
plt.ylabel('Ext Lens2 (V)')
plt.colorbar(label="maximum distance (mm)")
plt.title('Maximum Distance from Optical Axis at Bender Center')
plt.gca().set_aspect('equal')
plt.tight_layout()



plt.figure('Mean Distance Bender Center')
plt.scatter(e1,e2,c=mean_dist, s =20)
plt.xlabel('Ext Lens1 (V)')
plt.ylabel('Ext Lens2 (V)')
plt.colorbar(label="Mean distance (mm)")
plt.title('Mean Distance from Optical Axis at Bender Center')
plt.gca().set_aspect('equal')
plt.tight_layout()

plt.figure('Median Distance Bender Center')
plt.scatter(e1,e2,c=med_dist, s =20)
plt.xlabel('Ext Lens1 (V)')
plt.ylabel('Ext Lens2 (V)')
plt.colorbar(label="Median distance (mm)")
plt.title('Median Distance from Optical Axis at Bender Center')
plt.gca().set_aspect('equal')
plt.tight_layout()

plt.figure('Min Distance Bender Center')
plt.scatter(e1,e2,c=min_dist, s =20)
plt.xlabel('Ext Lens1 (V)')
plt.ylabel('Ext Lens2 (V)')
plt.colorbar(label="Min distance (mm)")
plt.title('Min Distance from Optical Axis at Bender Center')
plt.gca().set_aspect('equal')
plt.tight_layout()
"""
plt.show()



