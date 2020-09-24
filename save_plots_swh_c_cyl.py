from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
import os

"读取单个netCDF文件并可视化，最后图像为一条轨道上的数据"


def read_ncfile_value(fh, value):
    '''读取文件，value为要读取的参数
    return： lons, lats, value'''
    lons = fh.variables['lon'][:]
    lats = fh.variables['lat'][:]
    value = fh.variables[value][:]
    return lons, lats, value


fig = plt.figure()
# read all netCDF file
dir_path = 'E:\python_workfile\\remote_sensing\H2B_nc_data\H2B_20200611'
ncfiles = os.listdir(dir_path)
for ncfile in ncfiles:
    fh = Dataset(dir_path + '\\' + ncfile, mode='r')
    lons = fh.variables['lon'][:]
    lats = fh.variables['lat'][:]
    swhc = fh.variables['swh_c'][:]
    swhc_units = fh.variables['swh_c'].units

    fh.close()

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

    plt.savefig(dir_path+'\\'+ncfile.split('.')[0]+'.jpg')
    plt.close()
