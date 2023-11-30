import matplotlib.pyplot as plt
import fluids as fl
import sympy as sp
from pint import _DEFAULT_REGISTRY as u

class propFeed():
    def __init__(self, name):
        #Creating name/label attribute
        self.name = name

class liquids(propFeed):
    def __init__(self, name, density, viscosity, massFlow):
        self.fluidDensity = density
        self.fluidViscosity = viscosity
        self.fluidMassFlow = massFlow

        #Accesses the superclass name attribute, by running the superclass constructor with name as argument
        super().__init__(name)

class liquidValves(liquids):
    def __init__(self, name, density, viscosity, massFlow, Cv, ID):
        self.Cv = Cv
        self.ID = ID
        super().__init__(name, density, viscosity, massFlow)

        self.K = fl.fittings.Cv_to_K(Cv, ID)

    #def KFactorFunc(self):
        #K, Cv, ID = sp.symbols("K, Cv, ID", real=True)
        #eqn = sp.Eq(K, (1.6 * 10**9)*((ID**4)/(Cv/1.56)**2))
        #solutionList = sp.solve(eqn, K)
        #solution = solutionList[0].subs([(Cv, self.Cv), (ID, self.Cv)])
        #print(solution)