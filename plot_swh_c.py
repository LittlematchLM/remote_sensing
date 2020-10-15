from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import h5py
import glob
"读取单个netCDF文件并可视化，最后图像为一条轨道上的数据"

fig = plt.figure()
# read netCDF file
my_h5file = '.\H2B_nc_data\ICESAT2_ATL12_20200711\\ATL12_20200710205055_02370801_003_01.h5'

with h5py.File(my_h5file, 'r') as f:
    lats = f['gt2l']['ssh_segments']['latitude'][:]
    lons = f['gt2l']['ssh_segments']['longitude'][:]
    swh = f['gt2l']['ssh_segments']['heights']['swh'][:]

# Draw the map
# m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
m = Basemap(projection='npaeqd', boundinglat=60, lon_0=180, resolution='c')
x, y = m(lons, lats)
# Draw the scatterplot
h = m.scatter(x, y, c=swh, marker='.', cmap=plt.cm.jet, alpha=0.8)

plt.cm.ScalarMappable.set_clim(h, vmin=0, vmax=10)
m.colorbar(location='right')
m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180., 180., 60.), labels=[0, 0, 0, 1])

plt.show()
