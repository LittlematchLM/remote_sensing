#!/usr/bin/env python
# coding: utf-8

# # 读取所有对比结果

# In[156]:


from sklearn.metrics import mean_squared_error, r2_score
from HaiYangData import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os


# In[158]:


years = ['2019','2020']
months = ['04','05','06','07','08','09']
output_dir = r'E:\\HLCourse\\experiment_marine_technology\\finally_project\\output\\'
dataframe_dir = r'E:\\HLCourse\\experiment_marine_technology\\finally_project\\dataframe\\'
path_title = r'HY&IS swh'
resolution = 25000
var = r'swh'
satelite1 = 'HaiYang2'
satelite2 = 'ICESAT2'
# In[195]:


# 将WGS 84坐标（4326）转化为极射投影
crs = CRS.from_epsg(4326)
crs = CRS.from_string("epsg:4326")
crs = CRS.from_proj4("+proj=latlon")
crs = CRS.from_user_input(4326)
crs2 = CRS(proj="aeqd")

transformer = HaiYangData.set_transformer(crs,crs2)
transformer_back = HaiYangData.set_transformer(crs2,crs)


# In[155]:


def polar_plot(x_map, y_map,grid, vmax ,vmin,color_lable=None,title=None,cmap = plt.cm.jet):
m = Basemap(projection='npaeqd', boundinglat=66, lon_0=0, resolution='c')
m.pcolormesh(x_map, y_map, data=grid, cmap=cmap,vmin=vmin, vmax=vmax,latlon = True)
cb = m.colorbar(location='bottom')
if color_lable:
    cb.set_label(color_lable)
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90., 120., 10.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180., 180., 60.), labels=[0, 0, 0, 1])
plt.title(title)


# # 读取处理HY2/ALT&Cryosat2/SIRAL SWH对比结果

# In[15]:


files = glob.glob(dataframe_dir + path_title + '*.csv')
files.sort()


# In[148]:


data_df= pd.DataFrame(columns = ['ij','hy_time_round','other_time_round','hy_time','hy_value','other_time','other_value','diff'])
for f in files:
data_df = pd.concat([data_df,(pd.read_csv(f))])


# In[144]:


data_df = data_df.drop(data_df[data_df['diff'] > data_df['diff'].std() * 3 ].index)
data_df = data_df.drop(data_df[data_df['diff'] < np.negative(data_df['diff'].std() * 3) ].index)


# In[145]:


plt.figure(figsize=(6, 6))
plt.scatter(data_df['hy_value'], data_df['other_value'], marker='.')
plt.plot(np.linspace(0,5),np.linspace(0,5),color='r')
x_tick = range(0,6,1)
plt.xticks(x_tick)
plt.yticks(x_tick)
plt.grid(True)
plt.text(4, 2.8, 'Bias = '+str(round(data_df['diff'].mean(), 3)))
plt.text(4, 2.4, 'STD = '+str(round(data_df['diff'].std(), 3)))
plt.text(4,2.0,'Sample# = ' + str(data_df.shape[0]))
plt.text(4,3.2,'RMSE = ' + str(round(np.sqrt(mean_squared_error(data_df['hy_value'], data_df['other_value'])),3)))
plt.text(4,3.6,'R^2 = ' + str(round(r2_score(data_df['hy_value'], data_df['other_value']),3)))

plt.xlabel(satelite1+' ' + var + '(m)')
plt.ylabel(satelite2+' ' + var + '(m)')
plt.title(satelite1+' & '+ satelite2 + var + str(years) + str(months) )


plt.savefig(r'output/scatter_plot/'+str( years) + str(months)  +'3std'+satelite1+' & '+ satelite2 +' '+ var +' '+ 'scatter_plot.jpg')
plt.show()

# In[196]:


hy_alt = HaiYangData(satellite='hy', sensor='alt',resolution=resolution)

hy_x_map, hy_y_map = hy_alt.get_map_grid(transformer_back)

draw_diff_grid = hy_alt.get_nan_grid(hy_alt.nlat, hy_alt.nlon)
for i in range(data_df.shape[0]):
    draw_diff_grid[int(data_df.iloc[i].ij.split('+')[0])][int(data_df.iloc[i].ij.split('+')[1])] = data_df.iloc[i]['diff']


# In[201]:


plt.figure(figsize=(9, 9))
polar_plot(hy_x_map, hy_y_map,draw_diff_grid,vmax=1, vmin = -1,color_lable=var+' Bias(m)',title=satelite1+' & '+satelite2 + str(years) + str(months))
plt.savefig(r'output/'+ str(years) + str(months)  +'3std'+satelite1+' & '+satelite2 + var +' '+ 'location_plot.jpg')
