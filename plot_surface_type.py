from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
import glob
import pandas as pd

"读取单个netCDF文件并可视化，图像分别存在各自的文件夹中"


def get_lon_lat(DataFarme):
    xx = np.array(DataFarme.lon)
    yy = np.array(DataFarme.lat)
    return xx, yy


def get_projxy(bm_class, DataFarme):
    xx, yy = get_lon_lat(DataFarme)
    x, y = bm_class(xx, yy)

    return x, y


def read_ncfile_value(fh, value):
    '''读取文件，value为要读取的参数
    return： lons, lats, value'''
    lons = fh.variables['lon'][:]
    lats = fh.variables['lat'][:]
    value = fh.variables[value][:]
    return lons, lats, value


# read all netCDF file
dir_path = r'H:\remote_sensing_data\HY-2B\2019\07'
ncfiles = glob.glob(dir_path + '\*.nc')

ncfiles = ncfiles[267:293]

lon_array = np.array([])
lat_array = np.array([])
ice_array = np.array([])
type_array = np.array([])
rain_array = np.array([])
swh_array = np.array([])
#     value_mask_array = np.array([])
swh_mask_array = np.array([])
value = 'ice_flag'
for file in ncfiles:
    with Dataset(file, mode='r') as fh:
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        ice = fh.variables['ice_flag'][:]
        type = fh.variables['surface_type'][:]
        rain = fh.variables['rain_flag'][:]
        lon_array = np.append(lon_array, lons)
        lat_array = np.append(lat_array, lats)
        ice_array = np.append(ice_array, ice)
        type_array = np.append(type_array, type)
        rain_array = np.append(rain_array, rain)
        swh = fh.variables['swh_ku'][:]
        swh_mask = swh.mask
        if np.array(swh_mask, dtype=bool).shape == ():
            swh_mask = np.full((len(swh),), False)
        swh_array = np.append(swh_array, swh)
        swh_mask_array = np.append(swh_mask_array, swh_mask)

swh_array_masked = np.ma.array(swh_array, mask=swh_mask_array)

df = pd.DataFrame((lon_array, lat_array, ice_array, type_array, rain_array, swh_array),
                  index=['lon', 'lat', 'ice', 'type', 'rain', 'swh'])
df = df.T
# df = df.drop(df[(df.ice == 0)].index)


lat_min = 66
df = df.drop(df[(df.lat < lat_min)].index)
df = df.drop(df[(df.swh > 100)].index )

ice_df = df.drop(df[(df.ice == 0)].index)
rain_df = df.drop(df[(df.rain == 0)].index)

surface_df = df.drop(df[(df.type == 2)].index)
# surface_df = surface_df.drop(surface_df[(surface_df.type == 1)].index)

plt.figure(figsize=(9, 9))
# fig, (ax1,ax2,ax3,ax4) = plt.subplot(2,2)
m = Basemap(projection='npaeqd', boundinglat=66, lon_0=180, resolution='c')
# x1, y1 = get_projxy(m, ice_df)
# m.scatter(x1, y1, marker='x', alpha=0.5, color='r')
# plt.title('ice point ')
# x2, y2 = get_projxy(m, rain_df)
# m.scatter(x2, y2, marker='o', alpha=0.5, color='b')
# plt.title('rain point ')

x3, y3 = get_projxy(m, surface_df)
m.scatter(x3, y3, marker='.', alpha=0.5, color='g')
plt.title('land point ')

# plt.title('red: ice, blue: rain, green: land')
m.drawcoastlines()
# m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180., 180., 60.), labels=[0, 0, 0, 1])

plt.show()
# plt.savefig('./pic3')
