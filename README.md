# LAS ION OPTICS CTS CUP IN #

This repository contains simulation code and results for inspection and analysis of TITAN's laser ablation ion source being developed at the University of Calgary. The included directories focus largely on the focus and steering tuning of the electrodes in the LAS that are responsible for ion transport. The geometry file included (.gem) has been compiled in SIMION and represents the geometry of the laser ablation source while the faraday cup before the drift tube is collecting the beam. For simulations and code dealing with the scenario with the faraday cup out and a longer drift time for ions before detection, see the LAS-ION-OPTICS-CTS repository. 

To use any of the .lua scripts in the following folders, one must refine the .gem file in simion and generate the potential arrays in their local storage (they are too large to reasonably store and pull from this repository). 

## IonInitialConditions ##
This workbench tests the impact of initial conditions (starting kinetic energy and cone angle) on the dynamic steering defined by the fits done with the dynamic steering tuning scans. Ion efficiencies through specified points in the optics are recorded.
## IonTOFResolvability ## 
This package can be used to determine the time of flight and compare drift distances requred to resolve a number of species. It uses the switching time and laserr jitter to estimate the time window restricting species sepereation. 
## Sandbox-1300eV ##
This workbench can be used to fast adjust manually and test specific voltage configurations. 

the following are found within the TunungScans directory:
## 2DFullTargetScan ##
This workbench flies ions in a large beam the size of the full target (4mm radius) and scans voltages in 2D across any two specified focusing electrodes. The efficiency of the configuration at the faraday cup is recorded and can then be plotted with the 2DFullTargetPlotter python script.
## BenderSel2DScan ##
This workbench scans the bender and split einzel lens focusing voltages to inspect optimal focusing. The bender electrodes are given an scanned offset from their typical +-920V such that all potentials applied are shifted in the positive direction. 
## DeflectorCollector2DScan ##
This workbench scans the deflector and collector voltages to determine if "last minute" focusing into the faraday cup can be achieved to improve efficiency.
## ExtractionSteering2DScan ##
This workbench flies ions in a large beam the size of the full target (4mm radius) and scans the third and fifth extraction electrodes to determine optimal voltages to focus into the center of the bender. The 2DFullTargetScan workbench is reccomended to be used instead for most cases. 
## ExtrctionSteeringYaxisScan ##

## ExtractionSteeringZaxisScan ##

## SelFocusScan ##
This workbench scans the split einzel lens focusing voltage.
## SelSteering2DScan ##
This workbench scans the split einzel lens steering voltage to determine the coeffiicients for dynamic steering
## SelSteeringTester ## 
This workbench tests the efficiency of the dynamic steering on the SEL given the coefficients aquired from the fit to the SelSteeringScan.


