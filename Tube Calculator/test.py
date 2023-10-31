import numpy as np
import matplotlib.pyplot as plt

a = [1, 2, 3]
b = [3, 2, 1]

fig, ax = plt.subplots()
lines = ax.plot(a, b)
plt.show()

print(np.square(a))
print(np.divide(a, b))
print (2 * a)