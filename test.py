import numpy as np
import pandas as pd
hy_cy_coincident_list = np.array([['750+38', 619631968.508203, 1.37, 619632901.375125, 0.984],
 ['751+38', 619631969.516053, 1.252, 619632899.488252, 1.284],
 ['751+38', 619631969.516053, 1.252, 619632900.431687, 1.564],
 ['752+38', 619631970.498717, 1.216, 619632898.544823, 1.207],
 ['754+15', 620496875.487952, 1.717, 620496159.649289, 1.896],
 ['754+15', 620496875.487952, 1.717, 620496160.592718, 1.924],
 ['755+15', 620496876.49617, 1.82, 620496158.705851, 1.793],
 ['755+-120', 620503126.503192, 2.648, 620502126.6794109, 2.652],
 ['755+-120', 620503127.511161, 2.468, 620502126.6794109, 2.652],
 ['756+-120', 620503128.51914, 2.29, 620502125.73597, 2.574],
 ['756+-120', 620503128.51914, 2.7, 620502125.73597, 2.896],
 ['756+-120',620505128,3.12,620503333,3.22]
 ])

time_win = 1800
hy_cy_df = pd.DataFrame(hy_cy_coincident_list, columns=['ij', 'hy_time', 'hy_value', 'other_time', 'other_value'])

hy_cy_df['hy_time_round'] = ((hy_cy_df['hy_time'].astype(np.float))/time_win).astype(np.int)

hy_cy_df['other_time_round'] = ((hy_cy_df['other_time'].astype(np.float))/time_win).astype(np.int)
hy_cy_mean_df = hy_cy_df.groupby(['ij','hy_time_round','other_time_round']).mean()

hy_cy_df

#
# c = pd.DataFrame(columns=['ij', 'hy_time', 'hy_value', 'other_time', 'other_value'])
#
# b = np.array([])
# time1, time2, value1, value2, num_count = 0, 0, 0, 0, 0
# for num in range(1,hy_cy_coincident_list.shape[0]):
#
#     if hy_cy_coincident_list[num-1][0] == hy_cy_coincident_list[num][0]:
#
#         if((float(hy_cy_coincident_list[num-1][1]) - float(hy_cy_coincident_list[num][1]))< time_win) and ((float(hy_cy_coincident_list[num-1][3]) - float(hy_cy_coincident_list[num][3]))< time_win):
#             value1 += np.float(hy_cy_coincident_list[num-1][2])
#             time1 +=  np.float(hy_cy_coincident_list[num-1][1])
#             value2 += np.float(hy_cy_coincident_list[num-1][4])
#             time2 += np.float(hy_cy_coincident_list[num-1][3])
#             num_count += 1
#             print(num_count)
#             print(value1,time1,value2,time2)
#         else:
#             value1 += np.float(hy_cy_coincident_list[num-1][2])
#             time1 +=  np.float(hy_cy_coincident_list[num-1][1])
#             value2 += np.float(hy_cy_coincident_list[num-1][4])
#             time2 += np.float(hy_cy_coincident_list[num-1][3])
#             num_count += 1
#             temp = np.array([hy_cy_coincident_list[num-1][0],time1/num_count,value1/num_count,time2/num_count,value2/num_count])
#             print('该停止了')
#             np.hstack(b,temp)
#             time1, time2, value1, value2, num_count = 0, 0, 0, 0, 0
#     else:
#         print('下一个点')
#         b = np.hstack((b,hy_cy_coincident_list[num-1]))
#
#
# b = b.reshape(6,5)

