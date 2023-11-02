import numpy as np
import matplotlib.pyplot as plt

a = np.array([1, 2, 3])
b = np.array([3, 2, 1])

fig, ax = plt.subplots()
lines = ax.plot(a, b)
plt.show()

def haaland(Re, e, D):
    return np.power((1/(-1.8 * np.log10(np.power((e/D)/3.7, 1.11) + (6.9/Re)))), 2)

print(np.square(a))
print(np.divide(a, b))
print (2 * a)

print(haaland(100, 0.001, 0.5))
print(np.power(2, 2))