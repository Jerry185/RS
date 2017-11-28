import csv
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd


filename = "datasets/FilmTrust/ratings.txt"
filename1="datasets/FilmTrust/trust.txt"
data=pd.read_table(filename,header=None,names=['userid','itemid','rating'],encoding='gb2312',delim_whitespace=True)
trust_data=pd.read_table(filename1,header=None,names=['trustor','trustee','trustvalue'],encoding='gb2312',delim_whitespace=True)

print("\r\nFilmTrust Rating Datasets\r\n %s with %d rows\r\n" % (filename, len(data)))


#查看前五条数据
print(data.head(15)  )
#查看每列数据类型以及nan情况
print(data.info())
# 获得所有object属性
print(data.describe())
# 数据排序
#print(data.sort_values(by=['rating'],axis=0,ascending=True))

''' ========缺失值处理====================

# 直接丢弃缺失数据列的行
print df4.dropna(axis=0,subset=['col1'])  # 丢弃nan的行,subset指定查看哪几列 
print df4.dropna(axis=1)  # 丢弃nan的列
# 采用其他值填充
dataset['Cabin'] = dataset['Cabin'].fillna('U') 
dataset['Title'] = dataset['Title'].fillna(0) 
# 采用出现最频繁的值填充
freq_port = train_df.Embarked.dropna().mode()[0]
dataset['Embarked'] = dataset['Embarked'].fillna(freq_port)
# 采用中位数或者平均数填充
test_df['Fare'].fillna(test_df['Fare'].dropna().median(), inplace=True)
test_df['Fare'].fillna(test_df['Fare'].dropna().mean(), inplace=True)
'''

#data.plot() #曲线图
#data.plot(kind='bar') # 柱状图
plt.scatter(data.head(50)['userid'],data.head(50)['rating'])
plt.show()