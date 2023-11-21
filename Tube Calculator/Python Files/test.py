import numpy as np
import matplotlib.pyplot as plt
import fluids as fl
from pint import _DEFAULT_REGISTRY as u

#Converter Function
def convertFunc():
    #Define initial variables (user would input these)
    a = 909856*(u.inch)
    b = 15*(u.inch)
    c = 15*(u.inch)

    #Converts variables to standard units
    astandard = a.to("meter")
    bstandard = a.to("meter")
    cstandard = a.to("meter")
    return astandard, bstandard, cstandard #Returns variables, so that other functions can use

#Function which actually performs the calculation
def calcFunc():
    #Creates new variables, assigns them the values returned by converterFunc()
    a, b, c = convertFunc()
    
    #Performs calculations
    ans = a * b * c
    print(ans)

calcFunc()