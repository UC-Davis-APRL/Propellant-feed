import numpy as np
import matplotlib.pyplot as plt
import fluids as fl
from pint import _DEFAULT_REGISTRY as u

#Input Variables
volumetricFlow = 0.0018*(u.meter**3/u.second)
minDiam = 0.1*(u.inch)
maxDiam = 5*(u.inch)
diamStep = 0.01*(u.inch)

#Convert Variables to Standard Units
volumetricFlowS = volumetricFlow.to(u.meter**3/u.second)
minDiamS = minDiam.to(u.meter)
maxDiamS = maxDiam.to(u.meter)
diamStepS = diamStep.to(u.meter)

#Let the calculations begin
diamRange = (np.arange(minDiamS.magnitude, maxDiamS.magnitude, diamStepS.magnitude))*(u.meter)
areaRange = np.square(diamRange / (2*u.dimensionless)) * np.pi*(u.dimensionless)
velocityRange = np.divide((volumetricFlowS), (areaRange))

#Plotting time
fig, ax = plt.subplots()
varPlot = ax.plot(diamRange.to("inch"), velocityRange.to("meter/second"))
ax.grid(visible = True)
ax.set_xscale('linear')
ax.set_yscale('linear')
ax.set_xlabel("Diameter (in)")
ax.set_ylabel("Velocity (m/s)")
plt.axhline(y = 99.312, color = 'r', linestyle = '-')
plt.xticks(np.arange(0, 5+0.5, 0.25), rotation = 'vertical')
plt.show()