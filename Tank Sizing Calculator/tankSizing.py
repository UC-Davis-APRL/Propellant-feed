import numpy as np
import math
import time

#constants and variables
burntime = 10 # seconds
ullageRatio = 1.15 # percentage of tank that is ullage

density_LOX = 1097.26 #kg/m^3
massflow_LOX = 1.5 #kg/s

density_kero = 820 #kg/s

OF = 2.2

def propVolumeCalc(burntime, massflow, ullageRatio, density):
    mass=burntime*massflow
    volume=mass/density
    volumeFinal=volume*ullageRatio

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

