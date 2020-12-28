from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
import os
import glob

"读取一个文件夹的n个netCDF文件并可视化，最后图像为n条轨道上的数据"

fig = plt.figure(figsize=(16, 12))
# read all netCDF file
cy_dir_path = r'E:\python_workfile\remote_sensing\H2B_nc_data\H2B_20200711\20200711'
cyfiles = glob.glob(cy_dir_path + '\*.nc')
cy_lon_array = np.array([])
cy_lat_array = np.array([])
cy_swh_array = np.array([])
cy_swh_mask_array = np.array([])
for cyfile in cyfiles:
    with Dataset(cyfile, mode='r') as fh:
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        swh = fh.variables['swh_c'][:]
        swh_mask = swh.mask
        if np.array(swh_mask, dtype=bool).shape == ():
            swh_mask = np.full((len(swh),), False)
        cy_lon_array = np.append(cy_lon_array, lons)
        cy_lat_array = np.append(cy_lat_array, lats)
        cy_swh_array = np.append(cy_swh_array, swh)
        cy_swh_mask_array = np.append(cy_swh_mask_array, swh_mask)

cy_swh_array_masked = np.ma.array(cy_swh_array, mask=cy_swh_mask_array)
plt.figure(figsize=(9,9))
#m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
m = Basemap(projection='npaeqd', boundinglat=60, lon_0=180, resolution='c')
x, y = m(cy_lon_array, cy_lat_array)

# Draw the scatterplot

h = m.scatter(x, y, c=cy_swh_array_masked, marker='o', cmap=plt.cm.jet, alpha=0.8)
m.colorbar(location='right')
m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180., 180., 30.), labels=[0, 0, 0, 1])
plt.cm.ScalarMappable.set_clim(h, vmin=0, vmax=5)
plt.title('origin SWH HY2B 20200711')
# 测试宿舍电脑上传
plt.show()
# 存储图像
#plt.savefig(fname=dir_path+'\\jpg\\20200711_swh_c_cyl.jpg')
