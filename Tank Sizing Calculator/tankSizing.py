import numpy as np
import math
import time

#constants and variables
burntime = 10 # seconds
ullageRatio = 1.15 # percentage of tank that is ullage
p_chamber = 360 #psi
OF = 1.4

density_LOX = 1141 #kg/m^3
density_kero = 820 #kg/m^3
volume_N2 = 9 * 0.001 #m^3

massflow = 1.862805164 #kg/s

massflow_kero = massflow / (OF + 1)
massflow_LOX = massflow / (1/OF + 1)

combined_CDA_LOX = 1.827e-4 * 0.092903 #experimental data converted from ft^2 to m^2 on ALI stand
combined_CDA_kero = 1.486e-4 * 0.092903 



def propVolumeCalc(burntime, massflow, ullageRatio, density):
    mass=burntime*massflow
    volume=mass/density
    volumeFinal=volume*ullageRatio #m^3

    return volumeFinal

volume_LOX = propVolumeCalc(burntime,massflow_LOX,ullageRatio, density_LOX)
volume_kero = propVolumeCalc(burntime,massflow_LOX/OF,ullageRatio, density_kero)

thickness = 0.125 #inches
radiusOut = 4 #outer diameter, inches
radiusIn = radiusOut - thickness

def tankHeight(radius, propellantVolume):
    propellantVolume *= 35.3147*12**3 #convert to in^3
    tankHeight = propellantVolume/(np.pi*radius**2)
    return tankHeight

keroTankHeight = tankHeight(radiusIn,volume_kero)
loxTankHeight = tankHeight(radiusIn,volume_LOX)

####################################
#Determination of Nitrogen Pressure#
####################################

#find propellant tank pressures

def pressFromCDA(mdot, rho, p_downstream, CDA):
    #mdot: kg/s, rho: kg/m^3, p_downtream: PA, CDA: m^2
    return (mdot/CDA)**2 / (2*rho) + p_downstream

p_chamber_PA = p_chamber * 6894.76 #convert to pascals
loxTankPressure = pressFromCDA(massflow_LOX,density_LOX,p_chamber_PA,combined_CDA_LOX) #pascals
keroTankPressure = pressFromCDA(massflow_LOX/OF,density_kero,p_chamber_PA,combined_CDA_kero) #pascals

print("LOX Tank Pressure: " + str(round(loxTankPressure/6894.76,2)) + " psi")
print("Kero Tank Pressure: " + str(round(keroTankPressure/6894.76,2)) + " psi")

volFlow_kero = massflow_kero/density_kero #m^3/s
volFlow_LOX = massflow_LOX/density_LOX

print(volFlow_kero)
print(volFlow_LOX)

#isothermal nitrogen flow in lox tank assumed
SCFM_nitrogen_LOX_side = volFlow_LOX * loxTankPressure/(101325) * 2118.88 #convert to standard cubic feet per minute
SCFM_nitrogen_Kero_side = volFlow_kero * keroTankPressure/(101325) * 2118.88 
