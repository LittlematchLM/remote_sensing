import collections
import numpy as np
import pandas as pd


hy_lat = np.array([1, 2, 2, 2, 2, 2, 2])
hy_lon = np.array([2, 2, 1, -1, 1, 2, -1])
hy_swh = np.array([0.5, 0.66, 1.3, 0.58, 0.6, 0.99, 2.3])
hy_time = np.array([6.17701975668108E8,
                    6.17701976021226E8,
                    6.17701977042735E8,
                    6.17701981312124E8,
                    6.17701982018682E8,
                    6.17701983664886E8,
                    6.1564864
                    ])
hy_value_grid = np.full(fill_value=np.nan, shape=[6, 6])
hy_time_grid = np.full(fill_value=np.nan, shape=[6, 6])
hy_num_grip = np.zeros(shape=[6, 6])

time_dict = {}
for i in range(len(hy_swh)):
    x = hy_lat[i]
    y = hy_lon[i]
    if hy_num_grip[x][y] == 0:
        hy_value_grid[x][y] = hy_swh[i]
        hy_time_grid[x][y] = hy_time[i]
        hy_num_grip[x][y] = 1
        dict_name = str(x) + '+' + str(y)
        time_dict[dict_name] = {hy_time_grid[x][y]: hy_value_grid[x][y]}
        print('1' + str(dict_name))
    else:
        dict_name = str(x) + '+' + str(y)
        time_dict[dict_name][hy_time[i]] = hy_swh[i]
        print('2' + str(dict_name))
