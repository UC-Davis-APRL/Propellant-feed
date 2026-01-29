import numpy as np
import math
import time
from scipy.optimize import fsolve

#constants and variables
burntime = 10 # seconds
p_chamber = 360 #psi
OF = 1.4
massflow = 1.83 #kg/s

ullageRatio = 1.15 # percentage of tank that is ullage
density_LOX = 1097 #kg/m^3
density_kero = 820 #kg/m^3
volume_N2 = 9 * 0.001 #m^3


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
volFlow_LOX = massflow_LOX/density_LOX #m^3/s

#isothermal nitrogen flow in both tanks assumed
SCFM_nitrogen_LOX_side = volFlow_LOX * loxTankPressure/(101325) * 2118.88 #convert to standard cubic feet per minute
SCFM_nitrogen_Kero_side = volFlow_kero * keroTankPressure/(101325) * 2118.88 


####################################
#regulator flow curve interpolation#
###Functions estimated in Desmos####
####################################

def getInlet415(Pdownstream,volumetricFlow):
    def func415(x, *args):
        Pdownstream, volumetric_flow = args
        return np.sqrt((0.00134667*x**2 - 11.39333 * x + 1060) * volumetric_flow + (0.12664*x**2 + 298.12 * x -114120)) + 0.0000285296*x**2 + 0.440726 * x - Pdownstream
    
    initGuess = 5000
    args = (Pdownstream,volumetricFlow)
    root, info, status, msg = fsolve(func415, initGuess,args=args,full_output=True)
    return root

def getInlet873(Pdownstream,volumetricFlow):
    def func873(x, *args):
        Pdownstream, volumetric_flow = args
        return np.sqrt((-0.000233333*x**2 - 0.243333*x - 170) * volumetric_flow + (0.4336*x**2 - 411.2*x + 161200)) - 0.0000459938*x**2 + 0.548679*x - Pdownstream

    initGuess = 5000
    args = (Pdownstream,volumetricFlow)
    root, info, status, msg = fsolve(func873, initGuess,args=args,full_output=True)
    return root

upstreamLOXPress = getInlet873(loxTankPressure/6894.76,SCFM_nitrogen_LOX_side)[0]
upstreamKeroPress = getInlet873(keroTankPressure/6894.76,SCFM_nitrogen_Kero_side)[0] 

#print("upstream lox pressure: " + str(upstreamLOXPress))
#print(f"upstream kero pressure: {upstreamKeroPress}")

def RK(pressure,temperature):
    def func(x,*args):
        a, b, P, T = args
        R = 8.3144
        return ((R * T) / (x - b)) - (a/(np.sqrt(T) * x*(x+b))) - P

    a_nitrogen = 1.553 
    b_nitrogen = 2.677e-5

    args = a_nitrogen,b_nitrogen,pressure,temperature

    initGuess = 0.01
    molarVolume, info, status, msg = fsolve(func,initGuess,args=args,full_output=True)

    return molarVolume[0]

#end state
N2TankPressureFinal = max(upstreamKeroPress*6894.76,upstreamLOXPress*6894.76)
converganceDiff = 1
N2TankPressureInit = 10000000 #initial guess
prevN2TankPressure = 0
k = 1.4
counter = 0

while converganceDiff > 1 or counter < 100:

    N2TankTempFinal = 298 * (N2TankPressureFinal/N2TankPressureInit) ** (1-(1/k))
    print(N2TankTempFinal)
    molsN2Tank = volume_N2 / RK(N2TankPressureFinal,N2TankTempFinal)
    molsKeroTank = volume_kero / RK(keroTankPressure,298)
    molsLOXTank = volume_LOX / RK(loxTankPressure,90)#isothermal assumption may not be correct and we may need to use a lower temperature

    totalMols = molsKeroTank + molsLOXTank + molsN2Tank

    R = 8.3145
    T = 298
    v = volume_N2/totalMols
    a_nitrogen = 1.553 
    b_nitrogen = 2.677e-5

    N2TankPressureInit = (R*T)/(v - b_nitrogen) - a_nitrogen/(v*(v+b_nitrogen)*np.sqrt(T))
    converganceDiff = abs(N2TankPressureInit - prevN2TankPressure)
    prevN2TankPressure = N2TankPressureInit
    counter += 1


print("Nitrogen Tank Pressure: " + str(round(N2TankPressureInit/6894.76,2)) + " psi")

print(volume_kero / RK(keroTankPressure,298))
print(volume_LOX / RK(loxTankPressure,90))#isothermal assumption may not be correct and we may need to use a lower temperature)