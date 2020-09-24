from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np

"读取单个netCDF文件并可视化，最后图像为一条轨道上的数据"

fig = plt.figure()
# read netCDF file
my_ncfile = 'E:\python_workfile\\remote_sensing_alt_demo\H2B_nc_data\H2B_OPER_GDR_2PC_0043_0082_20200611T183611_20200611T192819.nc'
fh = Dataset(my_ncfile, mode='r')

lons = fh.variables['lon'][:]
lats = fh.variables['lat'][:]
swhc = fh.variables['swh_c'][:]
swhc_units = fh.variables['swh_c'].units
fh.close()
lon_mean = lons.mean()
lat_mean = lats.mean()

# Draw the map
m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
x, y = m(lons, lats)
# Draw the scatterplot
m.scatter(x, y, c=swhc, marker='.', cmap=plt.cm.jet, alpha=0.8)
m.colorbar(location='right')

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180., 180., 60.), labels=[0, 0, 0, 1])

plt.show()
