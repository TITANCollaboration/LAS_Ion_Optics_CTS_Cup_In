# Ion TOF Resolvability

This project aims to provide insight into the resolvability of any  species of interest for the LAS ion optical geometry to be built for testing in Calgary. The LAS ion optical time of flight equations and their python implementation are outlined below. 

## Calgary test stand TOF derivations
The bin size for time of flight measurement on the Calgary setup is determined by: 

$$
t_{window} = t_{switch} + t_{jitter} \text{ (1)}
$$

Where $t_{switch}$ is the switching time for the deflecting electrode and $t_{jitter}$ is the jitter of the laser. Values of $t_{switch} = 1\mu s$ and $t_{jitter} = 0.8\mu s$ were used for all calculations.

This $t_{window}$ determines the resolving power of the Calgary setup. Any pair masses with time of flight seperation less than half this window length will be binned into the same measurement and will therefore be unresolvable. The relationship between the time of flight of a reference mass $m_0$ and the time of flight corresponding to mass $m_1$ on the boundary of the unresolvable region around $m_0$ is given by:

$$
TOF(m_0, L_{dt})\pm \frac{t_{window}}{2} = TOF(m_1,L_{dt}) \text{ (2)}
$$

where

$$
TOF(m, L_{dt}) = t_0 + t_{dt} + t_{extra} \text{ (3)}
$$

Here $t_0$ is the initial time of flight of the ion from the ablation target to the end of the einzel lens, $t_{dt}$ is the time taken to traverse the drift tube, and $t_{extra}$ accounts for the intermediate drift time taken for the ion to travel from the end of the einzel lens to the begining of the drift tube. 

The time of flight of a drifting ion can be determined by: 

$$
t_{drift} = L_{drift} \sqrt{\frac{m}{2K}} \text{ (4)}
$$


where $L_{drift}$ is the distance drifted, $m$ is the mass of the ion, and $K$ is the kinetic energy of the ion.  

A simulation in SIMION (see `LAS-Ion-Optics\Sandbox-1300eV`) was run to generate a dataset of $t_0$ for integer masses ranging from 1 to 300. A regression was then performed on the dataset and $t_0$ was determined to follow: 

$$
t_0 = c\sqrt{m} \text{ (5)}
$$

for c ~= 1.14e7. 

Combining (3-5) produces: 

$$
TOF(m,L_{dt}) = c\sqrt{m} + L_{dt}\sqrt{\frac{m}{2K}}+L_{extra}\sqrt{\frac{m}{2K}} \text{ (6)}
$$

A value of $L_{extra}=0.05$ m was used for all calculations.

Combining (6) and (2) and solving for $m_1$ gives the bounds of the unresolvable mass window for reference mass, $m_0$:

$$
m_1 = \left( \frac{c\sqrt{m_0}+ L_{dt}\sqrt{\frac{m_0}{2K}}+L_{extra}\sqrt{\frac{m_0}{2K}}\pm \frac{t_{window}}{2}}{c+L_{dt}\sqrt{\frac{1}{2K}}+L_{extra}\sqrt{\frac{1}{2K}}}\right )^2 \text{ (7)}
$$

Alternatively, one can solve for $L_{dt}$, given the window-bounding mass $m_1$:

| $L_{dt} = \frac{c\left(\sqrt{m_0}-\sqrt{m_1}\right) + L_{extra}\left( \sqrt{\frac{m_0}{2K}}-\sqrt{\frac{m_1}{2K}} \right)+\frac{t_{window}}{2}}{\sqrt{\frac{m_1}{2K}}-\sqrt{\frac{m_0}{2K}}}$ | $m_1>m_0$ 
|-------------|---------------
| $L_{dt} = \frac{c\left(\sqrt{m_0}-\sqrt{m_1}\right) + L_{extra}\left( \sqrt{\frac{m_0}{2K}}-\sqrt{\frac{m_1}{2K}} \right)-\frac{t_{window}}{2}}{\sqrt{\frac{m_1}{2K}}-\sqrt{\frac{m_0}{2K}}}$ | $m_1 \< m_0$ 

$$ \text{ (8)}$$

## Table of constants
| Constant |   Value       | Description |
|----------|---------------|-------------|
| $t_{switch}$ | $1 \mu s$ |Switching time for deflecting electrode.| 
| $t_{jitter}$ | $0.8 \mu s$ |Jitter on laser pulse.|  
| $t_{window}$ | $1.8 \mu s$ |Total unresolvable time window.| 
| $K$          | $1300 eV$ |Kinetic energy of ions.|   
| $c$          | $11433748.958080072$ |Regression coefficient from simulated target-einzel lens TOF.|  
| $L_{extra}$  | $0.05m$ |Distance from the end of the einel lens to the start of the drift tube.|  

## TOFResolutionlib.py
This module has been inspired by the various functions from  `DT_length.py` used to determine TOF values, mass windows and drift lengths. It's functions can be imported and used by other python codes via `import TOFResolutionlib` so long as `TOFResolutionlib.py` is visible for the given path.

## DT_length.py
The script `DT_length.py` specifies an array of drift tube lengths and calculates times of flight for various expected species (declared in a dictionary - see periodic_dict in the code). It calculates the upper and lower bounds of the unresolvable mass window around each species, prints the minimum drift tube length required to resolve adjacent masses in the dictionary of species, makes a table with the minimum drift tube length for every combination of species pairs and generates 3 plots. 

It should be noted that negative drift tube lengths output indicate that the two masses in question will be resolvable no matter the length of the drift tube.

All functions take mass in units of amu (WITH THE EXCEPTION OF **get_t0()**) and energy in eV, convert to kg/J for use in equations, and convert back to amu/eV for return output. Time is always specified in seconds and the unresolvable window time ($t_{window}$) is always passed to functions as the entire 1.8e-6s and left for the function itself to halve for the upper and lower boundary calculations (as in the equations above). 

Eq (7) is implemented via **get_mass_window()** and Eq (8) is implemented via **get_Ldt()**. Both functions return both of the corresponding output bounds in order [upper, lower].

Note as of 2024-02-02 - `DT_length.py` will soon be seperated into a module soley containing functions and several visualization scripts that utilize the functions to plot or produce tables. 

Note as of 2024-02-07 - `DT_length.py` has been seperated into `TOFResolutionlib.py`, `DT_length_table.py`, and `DT_length_plots.py`. 

