import numpy as np
import matplotlib.pyplot as plt
import TOFResolutionlib as tr

#Setting the equation parameters:

#L_dt = np.arange(0,1.,0.0001)

#L_dt = np.arange(0.075,1.,0.0001)

L_dt = np.arange(0.2,1.,0.0001)

#L_dt = 0.6096 #2ft

L_extra = 0.050 #50mm

K = 1300 #eV same as the MR-TOF floated potential

switch_time = 1e-6 #Total on-->off-->on time  

optical_jitter = 4e-7 #This value is for the one-sided window (needs doubling to match switch_time window see t_window below)

#Below are the masses for common stable isotopes of interest 
mass_dict = {"Cu63":63, "Cu65":65, "Nb93":93, "Pd100":100, "Pd103":103,
             "Ag107":107, "Pd107":107, "Ag109":109, "Au197":197, 
             "Pb204":204, "Pb206":206, "Pb207":207, "Pb208":208, 
             "Pa231":231,"Th232":232, "U235":235, "U238":238, "Ac277":277}


periodic_dict = {"Al":26.982, "Cu":63.546, "Ag":107.87, 
                "Au":196.97, "Pb":207.20, "Th":232.04, 
                "Fe":55.845, "Cr":51.99, "W":183.84, "Ni":58.693, "Mo": 95.95} #Stainless steel 304 contains Fe, Cr, Ni, Mn, Mo 

#periodic_dict = {"Ba136":135.90458, "Xe136":135.907219} #note the resolving power for these masses match the value from Murray's thesis 
#periodic_dict = {"CuTest": 63.546, "AlTest": 26.982}

periodic_dict = dict(sorted(periodic_dict.items(), key=lambda item: item[1]))

if isinstance(L_dt,np.ndarray):
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
    fig4, ax4 = plt.subplots()
    fig5, ax5 = plt.subplots()
    fig6, ax6 = plt.subplots()
    fig7, ax7 = plt.subplots(1,2)
    colors= ['purple','blue','cyan', 'green','yellow', 'red']
else:
    fig, ax = plt.subplots()


color_ind = 0

prevkey = None

for key in periodic_dict:

    mass = periodic_dict[key]

    t_window = switch_time+2*optical_jitter

    m_max, m_min = tr.get_mass_window(mass, t_window, L_dt, L_extra, K)

    mass_window = m_max-m_min

    mass_window_p = m_max-mass

    mass_window_m = mass-m_min

    mass_resolving_power = mass/(mass_window/2)

    if isinstance(L_dt,np.ndarray):
        ax.plot(L_dt, mass_window/2, label = key)
        
        ax2.plot(L_dt, mass_resolving_power, label = key)
        
        ax3.plot(L_dt, np.abs(mass_window/2-mass_window_p)/mass_window_p, label = key)

        ax4.plot(L_dt, np.abs((mass-mass_window_p)-(mass-mass_window_m))/(mass_window), label = key)

        ax5.fill_between(L_dt, mass_window_m,mass_window_p, color = colors[color_ind], label = key, alpha = 0.3)

        ax6.fill_between(L_dt,m_max, m_min, color = colors[color_ind], alpha = 0.3)
        ax6.axhline(mass, linestyle = "--", color = colors[color_ind], label = key)

        if key in ['Cu','Fe',"Cr"]:
            ax7[0].fill_between(L_dt, m_max,m_min, color = colors[color_ind], alpha = 0.3)
            ax7[0].axhline(mass, linestyle = "--", color = colors[color_ind], label = key)
        
        elif key in ['Th', 'Pb', 'Au', "W"]:
            ax7[1].fill_between(L_dt, m_max,m_min, color = colors[color_ind], alpha = 0.4)
            ax7[1].axhline(mass, linestyle = "--", color = colors[color_ind], label = key)
        
        color_ind = (color_ind+1)%len(colors)

    else:
        ax.scatter(mass, mass_window, label = key)

        



    



    #Printing drift tube requirements for each adjacent mass species in periodic_dict:
    
    if list(periodic_dict.keys()).index(key) == 0 and len(list(periodic_dict.keys()))>1:
        nextkey = list(periodic_dict.keys())[1]
        L_p, L_m = tr.get_Ldt(mass, t_window, L_extra, K, periodic_dict[nextkey], 1)
        #print("Analytical drift tube length to resove " + nextkey + " from " + key +": " + str(L_p) + "m")
    elif list(periodic_dict.keys()).index(key) == len(periodic_dict)-1:
        prevkey = list(periodic_dict.keys())[len(periodic_dict)-2]
        L_p, L_m = tr.get_Ldt(mass, t_window, L_extra, K, 1, periodic_dict[prevkey])
        #print("Analytical drift tube length to resove " + prevkey + " from " + key +": " + str(L_m) + "m")
    else:
        i = list(periodic_dict.keys()).index(key)
        prevkey = list(periodic_dict.keys())[i-1]
        nextkey = list(periodic_dict.keys())[i+1]
        L_p, L_m = tr.get_Ldt(mass, t_window, L_extra, K, periodic_dict[nextkey], periodic_dict[prevkey])
        #print("Analytical drift tube length to resove " + prevkey + " from " + key +": " + str(L_m) + "m")
        #print("Analytical drift tube length to resove " + nextkey + " from " + key +": " + str(L_p) + "m")

if isinstance(L_dt,np.ndarray):
    ax.legend()
    ax.set_xlabel("Length Tube of Drift Tube (m)")
    ax.set_ylabel("Symetric Unresolvable Mass Half Window Width (u)")
    ax.set_title("Mass Resolvability of " + ', '.join(periodic_dict.keys()))

    ax2.legend()
    ax2.set_xlabel("Length of Drift Tube(m)")
    ax2.set_ylabel("Symetric Mass Resolving Power")
    ax2.set_title("Symetric Mass Resolving Powers of " + ', '.join(periodic_dict.keys()))

    ax3.legend()
    ax3.set_xlabel("Length of Drift Tube(m)")
    ax3.set_ylabel("Error in Symetric Window Assumption")
    ax3.set_title("Positive Error Symetrical Assumption " + ', '.join(periodic_dict.keys()))

    ax4.legend()
    ax4.set_xlabel("Length of Drift Tube(m)")
    ax4.set_ylabel("Error in Symetric Window Assumption")
    ax4.set_title("Balanced Error in Symetrical Assumption " + ', '.join(periodic_dict.keys()))

    ax5.legend()
    ax5.set_xlabel("Length of Drift Tube(m)")
    ax5.set_ylabel("Unresolvable Mass Window")
    ax5.set_title("Unresolvable Mass Window of " + ', '.join(periodic_dict.keys()))

    ax6.legend()
    ax6.set_xlabel("Length of Drift Tube(m)")
    ax6.set_ylabel("Mass (amu)")
    ax6.set_title("Unresolvable Mass Window of " + ', '.join(periodic_dict.keys()))

    ax7[0].legend()
    ax7[0].set_xlabel("Length of Drift Tube(m)")
    ax7[0].set_ylabel("Mass (amu)")
    ax7[1].legend()
    ax7[1].set_xlabel("Length of Drift Tube(m)")
    ax7[1].set_ylabel("Mass (amu)")
    fig7.suptitle("Unresolvable Mass Window Groupings")
else:
    # Mass vs Mass Windows for set drift tube length 
    all_masses = np.arange(0,250, 0.001)

    m_max_all, m_min_all = tr.get_mass_window(all_masses, t_window, L_dt, L_extra, K)

    mass_window_all = m_max_all - m_min_all 

    ax.plot(all_masses, mass_window_all, label = "L_dt = " + str(L_dt))
    ax.legend()
    ax.set_xlabel("Mass (u)")
    ax.set_ylabel("Unresolvable mass window (u)")
    ax.set_title("Unresolvable Mass Window For Masses "+str(int(np.round(all_masses[0]))) + "-" + str(int(np.round(all_masses[-1]))))
#Choose which plots to show
#[plt.close(f) for f in plt.get_fignums() if (f!=2)]
# Save all currently open figures
#[plt.figure(fignum).savefig(f"figure_{fignum}.png") for fignum in plt.get_fignums()]
plt.show()