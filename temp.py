from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
from matplotlib import cm, colors

a = np.array([1, 2, 3])
b = np.array([1, 2, 3])
ax, bx = np.meshgrid(a, b)
print(ax, bx)
fig, (ax0, ax1) = plt.subplots(nrows=2)

c = np.array([1, 2, 3, 4])
c.reshape((2, 2))
im = ax0.pcolormesh(ax, bx, c)

plt.show()
