import csv
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import pandas as pd

data_url = "https://raw.githubusercontent.com/alstat/Analysis-with-Programming/master/2014/Python/Numerical-Descriptions-of-the-Data/data.csv"
df = pd.read_csv(data_url)

print(df.describe())

'''
               Abra        Apayao      Benguet        Ifugao       Kalinga
count     79.000000     79.000000    79.000000     79.000000     79.000000
mean   12874.379747  16860.645570  3237.392405  12414.620253  30446.417722
std    16746.466945  15448.153794  1588.536429   5034.282019  22245.707692
min      927.000000    401.000000   148.000000   1074.000000   2346.000000
25%     1524.000000   3435.500000  2328.000000   8205.000000   8601.500000
50%     5790.000000  10588.000000  3202.000000  13044.000000  24494.000000
75%    13330.500000  33289.000000  3918.500000  16099.500000  52510.500000
max    60303.000000  54625.000000  8813.000000  21031.000000  68663.000000

############假设检验 t检验
'''

from scipy import stats as ss

# Perform one sample t-test using 1500 as the true mean
print(ss.ttest_1samp(a=df.ix[:, 'Abra'], popmean=15000))

# OUTPUT
#(-1.1281738488299586, 0.26270472069109496)

'''
图表分析， 盒模型,目前还没有研究他的应用
'''
#plt.figure(1)
#plt.show(df.plot(kind='box'))

'''柱状图，'''
#data=df['Abra']
#plt.figure(2)
#plt.show(data.plot(kind='bar'))

'''# 散点图，直观显示两个变量的相关性'''
plt.scatter(df['Abra'],df['Apayao'])
plt.show()