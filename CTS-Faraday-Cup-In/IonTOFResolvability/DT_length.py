import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from IPython.display import display

def amu_to_eV(m):
    return m*931.5e6

def amu_to_kg(m):
    return m*1.660540e-27

def kg_to_amu(m):
    return m*6.0221374e+26

def eV_to_J(K):
    return K*(1.60218e-19)

def get_t_drift(L, K, m):
    """
    Calculates and returns drift time in seconds.
    @param: 
    L - length of drift tube in m
    K - Kinetic energy of the ion in eV
    m - atomic mass unit of ion species

    @returns 
    Ion drift time in seconds 
    """
    return L*np.sqrt(amu_to_kg(m)/(2*eV_to_J(K)))

def get_m_drift(L, K, t):
    """
    Calculates and returns mass in amu.
    @param: 
    L - length of drift tube in m
    K - Kinetic energy of the ion in eV
    t - Drift time of ion species in seconds

    @returns: 
    Ion mass in amu 
    """
    m = kg_to_amu(t**2*2*eV_to_J(K)/L**2)
    return m

def get_t0(x,a):
    """
    Determines the time (in seconds) of flight of the ion from the ablation source to the end of the einzel lens given the mass, x (in kg)
    """
    return a * np.sqrt(x)

#Setting the equation parameters:

L_dt = np.arange(0,1.,0.0001)

L_extra = 0.050 #50mm

K = 1300 #eV same as the MR-TOF floated potential + 50eV from initial ablation kinetic energy

switch_time = 1e-6

optical_jitter = 4e-7

#Below are the masses for common stable isotopes of interest 
mass_dict = {"Cu63":63, "Cu65":65, "Nb93":93, "Pd100":100, "Pd103":103,
             "Ag107":107, "Pd107":107, "Ag109":109, "Au197":197, 
             "Pb204":204, "Pb206":206, "Pb207":207, "Pb208":208, 
             "Pa231":231,"Th232":232, "U235":235, "U238":238, "Ac277":277}


periodic_dict = {"Al":26.982, "Cu":63.546, "Ag":107.87, 
                "Au":196.97, "Pb":207.20, "Th":232.04, 
                "Fe":55.845, "Cr":51.99} #stainless steel 304 contains Fe, Cr, Ni, Mn 

#periodic_dict = {"Ba136":135.90458, "Xe136":135.907219} #note the resolving power for these masses match the value from Murray's thesis 
#periodic_dict = {"CuTest": 63.546, "AlTest": 26.982}
periodic_dict = dict(sorted(periodic_dict.items(), key=lambda item: item[1]))

#Performing the regression
"""
#Reading in the output from SIMION
sim_data = np.loadtxt("mass_1_to_300_to_einzel_end", skiprows = 12)
sim_t0 = sim_data[:,0]*1e-6  
sim_mass = amu_to_kg(sim_data[:,1])
popt, pcov = curve_fit(get_t0, sim_mass, sim_t0)
"""

#Regression value (see a in get_t0)
popt = [11433748.958080072]

#Test the regression 
"""
test_t0 = get_t0(sim_mass,popt[0])
plt.plot(sim_mass,sim_t0, "bo")
plt.plot(sim_mass, test_t0, color = "red")
#plt.show()
"""


def get_mass_window(t_total, t_window, reg_coeff, L_dt, L_extra, K):
    """
    Calculates the minimum and maximum masses within the unresolvable mass window such that masses outside of this window can be resolved.
    @param:
    t_total - the total time of flight of the reference ion in seconds
    t_window - the total window width in seconds (note that the reference ion will at most be seperated from other species in the window by t_window/2)
    reg_coeff - the regression coefficient obtained from the SIMION simulation of t0
    L_dt - the length of the drift tube in meters
    L_extra - the distance travelled from the end of the einzel lens to the beginning of the drift tube in meters
    K - The kinetic energy of the ions in eV
    @returns:
    m_max, m_min - masses in amu with the maximum/minimum TOF within the time window
    """
    K_J = eV_to_J(K)

    m_max = (  (t_total+t_window/2)/( reg_coeff+(L_dt+L_extra)*np.sqrt(1/(2*K_J)) )  )**2
    m_min = (  (t_total-t_window/2)/( reg_coeff+(L_dt+L_extra)*np.sqrt(1/(2*K_J)) )  )**2

    m_ref = (  (t_total)/( reg_coeff+(L_dt+L_extra)*np.sqrt(1/(2*K_J)) )  )**2

    #print("Ref mass is: " + str(kg_to_amu(m_ref[0])))
    #print("Maximum mass in the window is "+str(kg_to_amu(m_max[0])))
    #print("Minimum mass in the window is "+str(kg_to_amu(m_min[0])))
    return kg_to_amu(m_max), kg_to_amu(m_min)

def get_Ldt(m_0, t_window, reg_coeff, L_extra, K, m_max, m_min):
    """
    Calculates the drift tube length in meters required to resolve m_max and m_min from m_0  
    @param:
    m_0 - the reference mass in amu
    t_window - the total window width in seconds (note that the reference ion will at most be seperated from other species in the window by t_window/2)
    reg_coeff - The regression coefficient obtained from the SIMION simulation of t0
    L_extra - the distance travelled from the end of the einzel lens to the beginning of the drift tube in meters
    K- The kinetic energy of the ions in eV
    m_max - the mass in amu with the maximum TOF within the time window
    m_min - the mass in amu with the minimum TOF within the time window
    @returns:
    L_p, L_m - The lengths of the drift tube in meters such that m_max, m_min are resolvable from m_0
    """
    K = eV_to_J(K)

    m_0 = amu_to_kg(m_0)

    m_max = amu_to_kg(m_max)

    m_min = amu_to_kg(m_min)

    L_p = (reg_coeff*(np.sqrt(m_0)-np.sqrt(m_max))+L_extra*(np.sqrt(m_0/(2*K))-np.sqrt(m_max/(2*K)))+t_window/2)/(np.sqrt(m_max/(2*K))-np.sqrt(m_0/(2*K)))

    L_m = (reg_coeff*(np.sqrt(m_0)-np.sqrt(m_min))+L_extra*(np.sqrt(m_0/(2*K))-np.sqrt(m_min/(2*K)))-t_window/2)/(np.sqrt(m_min/(2*K))-np.sqrt(m_0/(2*K)))

    return L_p, L_m


fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

prevkey = None
skip1 = True

table_data = {}
table_rows = []

for key in periodic_dict:

    mass = periodic_dict[key]

    t_0 = get_t0(amu_to_kg(mass), popt[0])
    
    t_drift = get_t_drift(L_dt,K,mass)

    t_window = switch_time+2*optical_jitter

    #print("t window is: "+str(t_window))

    t_post_einz = get_t_drift(L_extra, K, mass)

    t_total = t_0 + t_drift + t_post_einz

    #print("t_total is: "+ str(t_total))

    print(key)

    m_max, m_min = get_mass_window(t_total, t_window, popt[0], L_dt, L_extra, K)

    mass_window = m_max-m_min

    mass_window_p = m_max-mass

    mass_window_m = mass-m_min

    mass_resolving_power = mass/mass_window

    #print("Ref mass (given drift for t_total and L_0 =248.5mm)  is: " + str(get_m_drift(0.2485+L_dt+L_extra, K, t_total)[0]))

    ax.plot(L_dt, mass_window, label = key)
    
    ax2.plot(L_dt, mass_resolving_power, label = key)
    
    ax3.plot(L_dt, np.abs(mass_window/2-mass_window_p), label = key)

    #Pringing drift tube requirements for each adjacent mass species in periodic_dict:
    
    if list(periodic_dict.keys()).index(key) == 0 and len(list(periodic_dict.keys()))>1:
        nextkey = list(periodic_dict.keys())[1]
        L_p, L_m = get_Ldt(mass, t_window, popt[0], L_extra, K, periodic_dict[nextkey], 1)
        print("Analytical drift tube length to resove " + nextkey + " from " + key +": " + str(L_p) + "m")
    elif list(periodic_dict.keys()).index(key) == len(periodic_dict)-1:
        prevkey = list(periodic_dict.keys())[len(periodic_dict)-2]
        L_p, L_m = get_Ldt(mass, t_window, popt[0], L_extra, K, 1, periodic_dict[prevkey])
        print("Analytical drift tube length to resove " + prevkey + " from " + key +": " + str(L_m) + "m")
    else:
        i = list(periodic_dict.keys()).index(key)
        prevkey = list(periodic_dict.keys())[i-1]
        nextkey = list(periodic_dict.keys())[i+1]
        L_p, L_m = get_Ldt(mass, t_window, popt[0], L_extra, K, periodic_dict[nextkey], periodic_dict[prevkey])
        print("Analytical drift tube length to resove " + prevkey + " from " + key +": " + str(L_m) + "m")
        print("Analytical drift tube length to resove " + nextkey + " from " + key +": " + str(L_p) + "m")


    #Making a table with dt length requirements for every combination of elements:
    table_rows.append(key)
    table_data[key] = []

    for other_key in periodic_dict:
        if periodic_dict[other_key]>periodic_dict[key]: #Add the length required to resolve the greater mass 
            L_p, L_m = get_Ldt(mass, t_window, popt[0], L_extra, K, periodic_dict[other_key], 1) #Smaller mass set arbitrarily to 1
            table_data[key].append(L_p)

        elif periodic_dict[other_key]<periodic_dict[key]: #Add the length required to resolve the smaller mass
            L_p, L_m = get_Ldt(mass, t_window, popt[0], L_extra, K, 1, periodic_dict[other_key]) #Greater mass set arbitrarily to 1
            table_data[key].append(L_m)

        else: #Same mass on diagonal
            table_data[key].append("N/a")

#Run code in jupyter notebook with display() to make the table look better
L_dt_table = pd.DataFrame(table_data)
L_dt_table.index = table_rows
#display(L_dt_table)
print(L_dt_table.to_string())

        
ax.legend()
ax.set_xlabel("Length Tube of Drift Tube (m)")
ax.set_ylabel("Unresolvable Mass Window Width (u)")
ax.set_title("Mass Resolvability of " + ', '.join(periodic_dict.keys()))

ax2.legend()
ax2.set_xlabel("Length of Drift Tube(m)")
ax2.set_ylabel("Mass Resolving Power")
ax2.set_title("Mass Resolving Powers of " + ', '.join(periodic_dict.keys()))

ax3.legend()
ax3.set_xlabel("Length of Drift Tube(m)")
ax3.set_ylabel("abs(mass_window/2-mass_window_p)")
ax3.set_title("Error in assuming mass_window is symettrical " + ', '.join(periodic_dict.keys()))
#plt.show()