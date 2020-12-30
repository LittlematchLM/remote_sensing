import numpy as np
import pandas as pd
from astropy.time import Time
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

def time_change(long_time):
     year = 2000 + int(long_time/(60*60*24*365))
     month = 0+ (long_time - (long_time/(60*60*24*365)))
     day =
     return year

year = time_change(620503127)

from datetime import datetime
import datetime
import time
strTime = '2000-01-01 00:00:00'

startTime = datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
print (startTime)

startTime2 = (startTime + datetime.timedelta(seconds=620503128)).strftime("%Y-%m-%d %H:%M:%S")
print (startTime2)

startTime3 = (startTime + datetime.timedelta(seconds=620502125)).strftime("%Y-%m-%d %H:%M:%S")
print (startTime3)


listt = [620505128,620503333]
a = lambda ltime: (datetime.datetime.strptime('2000-01-01 00:00:00', "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=ltime)).strftime("%Y-%m-%d %H:%M:%S")
ll = map(a,listt)

a=[('b',3),('a',2),('d',4),('c',1)]