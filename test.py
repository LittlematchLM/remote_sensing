from HaiYangData import *
import glob


hyfiles = glob.glob(r'G:\remote_sensing_data\hy2b\ALT\2019\07\*.nc')
hyfiles = hyfiles[0:28]
hy_value = ['swh_ku','swh_c','sig0_ku']

hy_alt = HaiYangData(satellite='hy', sensor='alt',resolution=25000)
hy_ori_df = pd.DataFrame(np.column_stack((hy_alt.from_nc_files(hyfiles, value=hy_value))), columns=['lon', 'lat', 'time']+hy_value)

# 删除无效点,只处理北纬66°以上的数据
hy_fill_value = 32767
hy_ori_df = hy_ori_df.drop(list(np.where(hy_ori_df['swh_ku'] == hy_fill_value)[0][:]))
hy_ori_df = hy_alt.data_filter(hy_ori_df,'lat',66)

# 将WGS 84坐标（4326）转化为极射投影
crs = CRS.from_epsg(4326)
crs = CRS.from_string("epsg:4326")
crs = CRS.from_proj4("+proj=latlon")
crs = CRS.from_user_input(4326)
crs2 = CRS(proj="aeqd")

transformer = hy_alt.transforme(crs,crs2)
transformer_back = hy_alt.transforme(crs2,crs)

df_e,df_w = hy_alt.split_W_E_earth(hy_ori_df,transformer)

# 交叉点平均化
mean_grid_e = hy_alt.coincident_point_mean(df_e,'swh_ku',hy_alt.nlat, hy_alt.nlon,hy_alt.resolution)
mean_grid_w = hy_alt.coincident_point_mean(df_w,'swh_ku',hy_alt.nlat, hy_alt.nlon,hy_alt.resolution)


finally_grid = np.full(shape=(hy_alt.nlat,hy_alt.nlon),fill_value=65533)
finally_grid[np.where((np.isnan(mean_grid_e)) == False)] = mean_grid_e[np.where((np.isnan(mean_grid_e)) == False)]
finally_grid[np.where((np.isnan(mean_grid_w)) == False)] = mean_grid_w[np.where((np.isnan(mean_grid_w)) == False)]

# 校准y坐标
hy_x = np.arange(hy_alt.nlat)
hy_y = np.arange(hy_alt.nlon)
hy_xx , hy_yy = np.meshgrid(hy_x * hy_alt.resolution, hy_y * hy_alt.resolution)

# 将xx,yy转换回坐标形式
hy_y_map, hy_x_map = transformer_back.transform(hy_xx , hy_yy)

hy_x_map_west = hy_x_map-180


plt.figure(figsize=(16, 9))

hy_m = Basemap(projection='npaeqd', boundinglat=66, lon_0=180, resolution='c')
# hy_xi, hy_yi = hy_m(hy_x_map, hy_y_map)
# hy_xi_west ,hy_yi_west = hy_m(hy_x_map_west, hy_y_map_west)
# Draw the scatterplot
h = hy_m.pcolormesh(hy_x_map, hy_y_map, data=finally_grid, cmap=plt.cm.jet,vmin=0, vmax=5,latlon = True)
# h2 = hy_m.pcolormesh(hy_x_map_west1 ,hy_y_map, data=finally_grid, cmap=plt.cm.jet,vmin=0, vmax=5,latlon = True)
hy_m.colorbar(location='right')
hy_m.drawcoastlines()
hy_m.fillcontinents()
hy_m.drawmapboundary()
hy_m.drawparallels(np.arange(-90., 120., 10.), labels=[1, 0, 0, 0])
hy_m.drawmeridians(np.arange(-180., 180., 60.), labels=[0, 0, 0, 1])
# plt.title("HY2B SWH  "+ year+ month)
plt.show()
plt.close()


plt.figure(figsize=(9,9))
#m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=0, urcrnrlon=360, resolution='c')
m = Basemap(projection='npaeqd', boundinglat=60, lon_0=180, resolution='c')
x, y = m(hy_ori_df['lon'].values, hy_ori_df['lat'].values)

# Draw the scatterplot

h = m.scatter(hy_ori_df['lon'].values, hy_ori_df['lat'].values, c=hy_ori_df['swh_ku'].values, marker='o', cmap=plt.cm.jet, alpha=0.8,latlon=True)
m.colorbar(location='right')
m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180., 180., 30.), labels=[0, 0, 0, 1])
plt.cm.ScalarMappable.set_clim(h, vmin=0, vmax=5)
plt.show()