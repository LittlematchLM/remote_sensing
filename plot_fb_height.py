from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import h5py
import glob

"读取单个h5文件并可视化,最后图像为一条轨道上的数据"

fig = plt.figure(figsize=(16, 12))
# read netCDF file
dir_path = '.\H2B_nc_data\ICESAT2_ATL12_20200711'
ncfiles = glob.glob(dir_path + '\*.h5')
lon_array = np.array([])
lat_array = np.array([])
swh_array = np.array([])
for ncfile in ncfiles:
    with h5py.File(ncfile, 'r') as f:
        lats = f['gt2l']['ssh_segments']['latitude'][:]
        lons = f['gt2l']['ssh_segments']['longitude'][:]
        swh = f['gt2l']['ssh_segments']['heights']['swh'][:]
    lon_array = np.append(lon_array, lons)
    lat_array = np.append(lat_array, lats)
    swh_array = np.append(swh_array, swh)


# Draw the map
m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
# m = Basemap(projection='npaeqd', boundinglat=60, lon_0=180, resolution='c')
x, y = m(lon_array, lat_array)

# Draw the scatterplot
h = m.scatter(x, y, c=swh_array, marker='.', linewidths=0.5, cmap=plt.cm.jet, alpha=0.8)
m.colorbar(location='right')
plt.cm.ScalarMappable.set_clim(h, vmin=0, vmax=5)

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180., 180., 60.), labels=[0, 0, 0, 1])

plt.show()
# plt.savefig(fname=my_h5file.split('.')[0]+'\\jpg\\20200711_swh_npaeqd.jpg')
