import numpy as np
import matplotlib.pyplot as plt
import fluids # as fl
import pint

def variablesFunc():
    #Input Variables
    massFlow = float(input("Enter Mass Flow Rate (kg/s): "))
    density = float(input("Enter Fluid Density (kg/m^3): "))
    viscosity = float(input("Enter Fluid Viscosity (Pa*s): "))
    roughness = float(input("Enter Pipe Roughness (m): "))
    diamRange = np.arange(float(input("Enter Minimum Pipe ID (m): ")), float(input("Enter Maximum Pipe ID (m): ")), float(input("Enter Step Size for Pipe ID (m): ")))
    straightLength = float(input("Enter Total Length of System (m): "))
  
    
    #Calculated Variables
    areaRange = np.array(np.square((diamRange / 2)) * np.pi)
    velocityRange = np.array(np.divide((massFlow), (areaRange * density)))
    reynoldsRange = fluids.vectorized.Reynolds(V=velocityRange, mu = viscosity, rho = density, D = diamRange)
    frictionFactorRange = fluids.vectorized.friction_factor(Re = reynoldsRange, eD = np.divide(roughness,diamRange), Darcy = True)
    kFactorRange = fluids.vectorized.K_from_f(fd = frictionFactorRange, L = straightLength, D = diamRange)
    pressureDrop = fluids.vectorized.dP_from_K(K = kFactorRange, rho = density, V = velocityRange)
    #Debugging: print(f"Reynolds Range: {reynoldsRange}\n Diameter Range: {diamRange}")
    #print (f "" )

    fig, ax = plt.subplots()
    varPlot = ax.plot(diamRange, pressureDrop)
    ax.set_xscale('linear')
    ax.set_yscale('linear')
    plt.show()

    return density, velocityRange, diamRange, straightLength

variablesFunc()