import numpy as np
import matplotlib.pyplot as plt


dataset = np.loadtxt('dataset.txt')


x0 = dataset[:, 0]
plt.plot(x0)

x1 = dataset[:, 1]
plt.plot(x1)

x2 = dataset[:, 2]
plt.plot(x2)

x3 = dataset[:, 3]
plt.plot(x3)

plt.show()

