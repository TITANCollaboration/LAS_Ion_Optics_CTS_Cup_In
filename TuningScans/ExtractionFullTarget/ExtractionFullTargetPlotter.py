import matplotlib.pyplot as plt
import numpy as np

file = "C:\\Users\\ethan\\Github_Repositories\\LAS_Ion_Optics_CTS_Cup_In\\TuningScans\\ExtractionFullTarget\\data\\ke_20\\2DIonExtractionLens_ke_20_V12_-2500_1500_nvolts_25.csv"
#file = "C:\\Users\\ethan\\Github_Repositories\\LAS_Ion_Optics_CTS_Cup_In\\TuningScans\\ExtractionFullTarget\\data\\ke_20\\2DIonExtractionLens_ke_20_V12_1000_1200_nvolts_25.csv"
data = np.loadtxt(file,skiprows = 2, delimiter=',')
V_ext_lens1 = data[:,0]
V_ext_lens2 = data[:,1]
efficiency = data[:,2]
mean_dist = data[:,3]
med_dist = data[:,4]
max_dist = data[:,5]
min_dist = data[:,6]

plt.figure('Maximum Distance Bender Center')
plt.scatter(V_ext_lens1,V_ext_lens2,c=max_dist, s =20)
plt.xlabel('Ext Lens1 (V)')
plt.ylabel('Ext Lens2 (V)')
plt.colorbar(label="maximum distance (mm)")
plt.title('Maximum Distance from Optical Axis at Bender Center')
plt.gca().set_aspect('equal')
plt.tight_layout()

plt.figure('Efficiency Distance Bender Center')
plt.scatter(V_ext_lens1,V_ext_lens2,c=efficiency, s =20)
plt.xlabel('Ext Lens1 (V)')
plt.ylabel('Ext Lens2 (V)')
plt.colorbar(label="Efficiency")
plt.title('Efficiency at Bender Center')
plt.gca().set_aspect('equal')
plt.tight_layout()


"""
plt.figure('Mean Distance Bender Center')
plt.scatter(V_ext_lens1,V_ext_lens2,c=mean_dist, s =20)
plt.xlabel('Ext Lens1 (V)')
plt.ylabel('Ext Lens2 (V)')
plt.colorbar(label="Mean distance (mm)")
plt.title('Mean Distance from Optical Axis at Bender Center')
plt.gca().set_aspect('equal')
plt.tight_layout()

plt.figure('Median Distance Bender Center')
plt.scatter(V_ext_lens1,V_ext_lens2,c=med_dist, s =20)
plt.xlabel('Ext Lens1 (V)')
plt.ylabel('Ext Lens2 (V)')
plt.colorbar(label="Median distance (mm)")
plt.title('Median Distance from Optical Axis at Bender Center')
plt.gca().set_aspect('equal')
plt.tight_layout()

plt.figure('Min Distance Bender Center')
plt.scatter(V_ext_lens1,V_ext_lens2,c=min_dist, s =20)
plt.xlabel('Ext Lens1 (V)')
plt.ylabel('Ext Lens2 (V)')
plt.colorbar(label="Min distance (mm)")
plt.title('Min Distance from Optical Axis at Bender Center')
plt.gca().set_aspect('equal')
plt.tight_layout()
"""
plt.show()



