import numpy as np
import matplotlib.pyplot as plt
#test

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
    reynoldsRange = np.array((density * velocityRange * diamRange) / viscosity)
    
    #Friction Factor Calculation
    frictionFactorRange = np.empty(len(diamRange))
    for i in np.arange(0, len(frictionFactorRange), 1):
        if reynoldsRange[i] <= 2000:
            frictionFactorRange[i] = 64 / reynoldsRange[i]
        elif reynoldsRange[i] < 4000:
            frictionFactorRange[i] = 64 / reynoldsRange[i] #should be replaced with whatever actually happens at transitional flow
        elif reynoldsRange[i] >= 4000:
            frictionFactorRange[i] = haaland(reynoldsRange[i], roughness, diamRange[i])
            #frictionFactorRange[i] = colebrookSolver(reynoldsRange[i], roughness, diamRange[i])
    
    #For debugging
    #print(f"Diameters: {diamRange} \n")
    #print(f"Area: {areaRange} \n")
    #print(f"Velocity: {velocityRange} \n")
    fig, ax = plt.subplots()
    varPlot = ax.plot(reynoldsRange, frictionFactorRange)
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.show()

    return frictionFactorRange, density, velocityRange, diamRange, straightLength

def colebrook(f, Re, e, D):
    return 1/np.sqrt(f) + 2*np.log10((e/D)/3.7 + 2.51/(Re*np.sqrt(f)))

def colebrookSolver(Re, e, D, tolerance=1e-6, maxIterations=100):
    f = 0.02  # Initial guess for the friction factor

    for i in range(maxIterations):
        fNew = f - colebrook(f, Re, e, D)
        
        if abs(fNew - f) < tolerance:
            return fNew
        
        f = fNew

def straightDarcyWeisbach():
    f, rho, u_avg, D, L = variablesFunc()
    Pdrop = f * L * (rho/2) * np.divide(np.square(u_avg), D)
    return Pdrop

def haaland(Re, e, D):
    return np.power((1/(-1.8 * np.log10(np.power((e/D)/3.7, 1.11) + (6.9/Re)))), 2)

straightDarcyWeisbach() 