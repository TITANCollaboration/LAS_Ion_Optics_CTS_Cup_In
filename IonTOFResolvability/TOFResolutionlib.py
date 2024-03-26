import numpy as np

def amu_to_eV(m):
    return m*931.5e6

def amu_to_kg(m):
    return m*1.660540e-27

def kg_to_amu(m):
    return m*6.0221374e+26

def eV_to_J(K):
    return K*(1.60218e-19)

def get_t_drift(L, m, K=1300.):
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

def get_m_drift(L, t, K=1300.):
    """
    Calculates and returns mass in amu given a certain drift.
    @param: 
    L - length of drift tube in m
    K - Kinetic energy of the ion in eV
    t - Drift time of ion species in seconds

    @returns: 
    Ion mass in amu 
    """
    m = kg_to_amu(t**2*2*eV_to_J(K)/L**2)
    return m

def get_t0(x,a = 11433748.958080072):
    """
    Determines the time (in seconds) of flight of the ion for some initial flight with approximately constant speed given the ion mass, x (in kg)
    a - Regression coefficient determined from mass vs. time of flight simulated dataset. Default value given for initial flight from center of the target to the end of the einzel lens.  
    """

    return a * np.sqrt(x)

def get_mass_window(mass, t_window, L_dt, L_extra, K=1300, reg_coeff = 11433748.958080072):
    """
    Calculates the minimum and maximum masses within the unresolvable mass window such that masses outside of this window can be resolved.
    @param:
    mass - the mass (in amu) of the reference ion for which to calculate the mass window
    t_window - the total window width in seconds (note that the reference ion will at most be seperated from other species in the window by t_window/2)
    L_dt - the length of the drift tube in meters
    L_extra - the distance travelled from the end of the einzel lens to the beginning of the drift tube in meters
    K - The kinetic energy of the ions in eV
    reg_coeff - the regression coefficient obtained from the SIMION simulation of t0
    @returns:
    m_max, m_min - masses in amu with the maximum/minimum TOF within the time window
    """
    K_J = eV_to_J(K)

    t_0 = get_t0(amu_to_kg(mass))
    
    t_drift = get_t_drift(L_dt,mass, K)

    t_post_einz = get_t_drift(L_extra, mass, K)

    t_total = t_0 + t_drift + t_post_einz

    m_max = (  (t_total+t_window/2)/( reg_coeff+(L_dt+L_extra)*np.sqrt(1/(2*K_J)) )  )**2

    m_min = (  (t_total-t_window/2)/( reg_coeff+(L_dt+L_extra)*np.sqrt(1/(2*K_J)) )  )**2

    return kg_to_amu(m_max), kg_to_amu(m_min)

def get_Ldt(m_0, t_window, L_extra, m_max, m_min, K = 1300., reg_coeff = 11433748.958080072):
    """
    Calculates the drift tube length in meters required to resolve m_max and m_min from m_0. If the length for only one side of the mass window 
    is required, set the other m_max/m_min to some arbitrary number other than m_0.
    @param:
    m_0 - the reference mass in amu
    t_window - the total window width in seconds (note that the reference ion will at most be seperated from other species in the window by t_window/2)
    L_extra - the distance travelled from the end of the einzel lens to the beginning of the drift tube in meters
    m_max - the mass in amu with the maximum TOF within the time window
    m_min - the mass in amu with the minimum TOF within the time window
    K - The kinetic energy of the ions in eV
    reg_coeff - The regression coefficient obtained from the SIMION simulation of t0
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