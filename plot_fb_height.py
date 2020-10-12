from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import h5py
from matplotlib import cm, colors

"读取单个h5文件并可视化,最后图像为一条轨道上的数据"

fig = plt.figure(figsize=(16, 12))
# read netCDF file
my_h5file = 'E:\python_workfile\\remote_sensing\\H2B_nc_data\\ICESAT2_20200711\\ATL10-01_20200710235929_02390801_003_01.h5'

f = h5py.File(my_h5file, 'r')

lats = f['gt2l']['freeboard_beam_segment']['beam_freeboard']['latitude'][:]
lons = f['gt2l']['freeboard_beam_segment']['beam_freeboard']['longitude'][:]
beam_fb_height = f['gt2l']['freeboard_beam_segment']['beam_freeboard']['beam_fb_height'][:]

f.close()
lon_mean = lons.mean()
lat_mean = lats.mean()

# Draw the map
#m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
m = Basemap(projection='npaeqd', boundinglat=60, lon_0=180, resolution='c')
x, y = m(lons, lats)

# Draw the scatterplot
h = m.scatter(x, y, c=beam_fb_height, marker='.',linewidths=0.5, cmap=plt.cm.jet, alpha=0.8)
m.colorbar(location='right')
plt.cm.ScalarMappable.set_clim(h, vmin=0, vmax=0.3)

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180., 180., 60.), labels=[0, 0, 0, 1])

plt.show()
# plt.savefig(fname=my_h5file.split('.')[0]+'\\jpg\\20200711_swh_npaeqd.jpg')
