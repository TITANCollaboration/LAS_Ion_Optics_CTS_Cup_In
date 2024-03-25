import numpy as np
import pandas as pd
import TOFResolutionlib as tr

#Setting the equation parameters:

L_dt = np.arange(0,1.,0.0001)

L_dt = np.arange(0.075,1.,0.0001)

L_dt = np.arange(0.2,1.,0.0001)

L_extra = 0.050 #50mm

K = 1300 #eV same as the MR-TOF floated potential

switch_time = 1e-6

optical_jitter = 4e-7

#Below are the masses for common stable isotopes of interest 
mass_dict = {"Cu63":63, "Cu65":65, "Nb93":93, "Pd100":100, "Pd103":103,
             "Ag107":107, "Pd107":107, "Ag109":109, "Au197":197, 
             "Pb204":204, "Pb206":206, "Pb207":207, "Pb208":208, 
             "Pa231":231,"Th232":232, "U235":235, "U238":238, "Ac277":277}


periodic_dict = {"Al":26.982, "Cu":63.546, "Ag":107.87, 
                "Au":196.97, "Pb":207.20, "Th":232.04, 
                "Fe":55.845, "Cr":51.99, "W":183.84,"Ni":58.693, "Mo": 95.95} #stainless steel 304 contains Fe, Cr, Ni, Mn, Mo

periodic_dict = dict(sorted(periodic_dict.items(), key=lambda item: item[1]))

table_data_mass = {}
table_rows_mass = []

table_data_time = {}
table_rows_time = []
L_dt_fixed = 0.6096 # 2ft


for key in periodic_dict:

    mass = periodic_dict[key]

    t_window = switch_time+2*optical_jitter

    t_total_fixedL = tr.get_t0(tr.amu_to_kg(mass)) + tr.get_t_drift(L_dt_fixed,mass,K) + tr.get_t_drift(L_extra,mass,K)

    m_max, m_min = tr.get_mass_window(mass, t_window, L_dt, L_extra, K)

    mass_window = m_max-m_min

    mass_window_p = m_max-mass

    mass_window_m = mass-m_min

    mass_resolving_power = mass/(mass_window/2)

    #Printing drift tube requirements for each adjacent mass species in periodic_dict:
    
    if list(periodic_dict.keys()).index(key) == 0 and len(list(periodic_dict.keys()))>1:
        nextkey = list(periodic_dict.keys())[1]
        L_p, L_m = tr.get_Ldt(mass, t_window, L_extra, periodic_dict[nextkey], 1, K)
        #print("Analytical drift tube length to resove " + nextkey + " from " + key +": " + str(L_p) + "m")
    elif list(periodic_dict.keys()).index(key) == len(periodic_dict)-1:
        prevkey = list(periodic_dict.keys())[len(periodic_dict)-2]
        L_p, L_m = tr.get_Ldt(mass, t_window, L_extra, 1, periodic_dict[prevkey], K)
        #print("Analytical drift tube length to resove " + prevkey + " from " + key +": " + str(L_m) + "m")
    else:
        i = list(periodic_dict.keys()).index(key)
        prevkey = list(periodic_dict.keys())[i-1]
        nextkey = list(periodic_dict.keys())[i+1]
        L_p, L_m = tr.get_Ldt(mass, t_window, L_extra, periodic_dict[nextkey], periodic_dict[prevkey], K)
        #print("Analytical drift tube length to resove " + prevkey + " from " + key +": " + str(L_m) + "m")
        #print("Analytical drift tube length to resove " + nextkey + " from " + key +": " + str(L_p) + "m")


    #Making a table with dt length requirements for every combination of elements:
    table_rows_mass.append(key)
    table_data_mass[key] = []

    for other_key in periodic_dict:
        if periodic_dict[other_key]>periodic_dict[key]: #Add the length required to resolve the greater mass 
            L_p, L_m = tr.get_Ldt(mass, t_window, L_extra, periodic_dict[other_key], 1, K) #Smaller mass set arbitrarily to 1
            table_data_mass[key].append(L_p)

        elif periodic_dict[other_key]<periodic_dict[key]: #Add the length required to resolve the smaller mass
            L_p, L_m = tr.get_Ldt(mass, t_window, L_extra, 1, periodic_dict[other_key], K) #Greater mass set arbitrarily to 1
            table_data_mass[key].append(L_m)

        else: #Same mass on diagonal
            table_data_mass[key].append("N/a")


    #Making the table of time windows required to resolve masses:
    table_rows_time.append(key)  
    table_data_time[key] = []

    for other_key in periodic_dict:
        if periodic_dict[other_key]>periodic_dict[key]: #Append the time required to resolve the larger mass
            m_other = periodic_dict[other_key]
            t_total_other = tr.get_t0(tr.amu_to_kg(m_other)) + tr.get_t_drift(L_dt_fixed,m_other,K) + tr.get_t_drift(L_extra,m_other,K)
            table_data_time[key].append((t_total_other-t_total_fixedL)*2e6)

        elif periodic_dict[other_key]<periodic_dict[key]: #Append the time required to resolve the smaller mass
            m_other = periodic_dict[other_key]
            t_total_other = tr.get_t0(tr.amu_to_kg(m_other)) + tr.get_t_drift(L_dt_fixed,m_other,K) + tr.get_t_drift(L_extra,m_other,K)
            table_data_time[key].append((t_total_fixedL-t_total_other)*2e6)

        else: #Same mass on diagonal
            table_data_time[key].append("N/a")
                  


#Run code in jupyter notebook with display() to make the table look better
L_dt_table = pd.DataFrame(table_data_mass)
L_dt_table.index = table_rows_mass
#L_dt_table = L_dt_table.style.set_caption("Minimum Drift Tube Lengths (m)")
#display(L_dt_table)

t_table = pd.DataFrame(table_data_time)
t_table.index = table_rows_time
#t_table = t_table.style.set_caption("Maximum Time Window for Resolution (us)")
#display(t_table)

print(L_dt_table)
print(t_table)