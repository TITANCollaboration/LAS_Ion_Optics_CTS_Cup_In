import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv("C:\\Users\\ethan\\Github_Repositories\\LAS-Ion-Optics-CTS\\TuningScans\\DeflectorCollector2DScan\\data\\ke_20\\DeflectorCollector_sel-1870_bender920.csv", skiprows=1)
# Extract columns
collector = df['Collector']
deflector = df['Deflector']
efficiency = df['Efficiency']

# Create a scatter plot
plt.scatter(collector, deflector, c=efficiency, cmap='viridis', s =100)
plt.colorbar(label='Efficiency')
plt.xlabel('Collector')
plt.ylabel('Deflector')
plt.title('Efficiency vs Collector and Deflector')
plt.show()