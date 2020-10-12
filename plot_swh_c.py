from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
from matplotlib import cm, colors

"读取单个netCDF文件并可视化，最后图像为一条轨道上的数据"


def mapll(xy, latitude, longitude):
    RE = 6378.273
    E2 = 0.006693883
    PI = 3.141592654
    E = np.sqrt(E2)

    if np.abs(latitude) < PI / 2:
        SL = 70 * PI / 180
        T = np.tan(PI / 4 - latitude / 2) / ((1 - E * np.sin(latitude)) / (1 + E * np.sin(latitude))) ^ (E / 2)
        TC = np.tan(PI / 4 - SL / 2) / ((1 - E * np.sin(SL)) / (1 + E * np.sin(SL))) ^ (E / 2)
        MC = np.cos(SL) / np.sqrt(1.0 - E2 * (np.sin(SL) ^ 2))
        RHO = RE * MC * T / TC

        xy[1] = -RHO * np.cos(longitude)
        xy[0] = RHO * np.sin(longitude)
    return xy


fig = plt.figure()
# read netCDF file
my_ncfile = 'E:\python_workfile\\remote_sensing\H2B_nc_data\H2B_20200711\H2B_OPER_GDR_2PC_0045_0143_20200711T234207_20200712T003004.nc'
fh = Dataset(my_ncfile, mode='r')

lons = fh.variables['lon'][:]
lats = fh.variables['lat'][:]
swhc = fh.variables['swh_c'][:]
swhc_units = fh.variables['swh_c'].units
fh.close()
lon_mean = lons.mean()
lat_mean = lats.mean()

a, b = np.meshgrid(lons, lats)
c = np.zeros((a.shape))
i = np.arange(2083)
c[i, i] = swhc[:]

# Draw the map
m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
x, y = m(lons, lats)
# Draw the scatterplot
# h = m.scatter(x, y, c=swhc, marker='.', cmap=plt.cm.jet, alpha=0.8)

# plt.cm.ScalarMappable.set_clim(h, vmin=0, )

cs = m.pcolor(a, b, c, cmap=plt.cm.jet, latlon=True)
m.colorbar(location='right')
m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180., 180., 60.), labels=[0, 0, 0, 1])

plt.show()
