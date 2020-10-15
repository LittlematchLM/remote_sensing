import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-5, 5, 1)
y = np.arange(-5, 4, 1)
xx, yy = np.meshgrid(x, y, sparse=True)
z = np.sin(xx ** 2 + yy ** 2) / (xx ** 2 + yy ** 2)
h = plt.pcolor(x, y, z)
print(x.shape, y.shape,)
print(xx.shape, yy.shape, z.shape)
plt.show()
