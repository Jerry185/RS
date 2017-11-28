import csv
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import pandas as pd

'''
协同过滤算法实验，使用movielens数据集，使用pandas工具进行数据处理
'''
filename = r"datasets/MovieLens/ratings.dat"
rnames = ['user_id','movie_id','rating','timestamp']

#获取数据集
ratings = pd.read_table(filename,sep='::',header=None,names=rnames,engine='python')
print("Ratings in MovieLens have %s row data\r\n"%len(ratings))

# 进行数据处理，获取透视图,将数据转换为以user为列，movie为列，rating为值的表格
data = ratings.pivot(index='user_id',columns='movie_id',values='rating')
print(data[:3])

'''推荐的第一步:
方法：计算 user 之间的相关系数;
工具：DataFrame.corr(method='pearson', min_periods=1) 方法，可以对所有列互相计算相关系数。
相关系数是用于评价两个变量间线性关系的一个值，取值范围为 [-1, 1]，-1代表负相关，0 代表不相关，1 代表正相关。
其中 0~0.1 一般被认为是弱相关，0.1~0.4 为相关，0.4~1 为强相关。
'''
'''
################################################### 下面代码为评估min_period参数代码######
代码太复杂 ，详细要看http://python.jobbole.com/83938/

#################################################
下面开始推荐算法：
'''
corr = data.T.corr(min_periods=200) #设置min_periods=200，最小样本数量为200，将会把评价数小于200的样本过滤掉。
corr_clean = corr.dropna(how='all') #缺失值处理
corr_clean = corr_clean.dropna(axis=1,how='all') ##删除全空的行和列
print(corr_clean[:10])
lucky = np.random.permutation(corr_clean.index)[0] #随机抽取一位用户为她做推荐
gift = data.ix[lucky]
gift = gift[gift.isnull()]#现在 gift 是一个全空的序列

corr_lucky = corr_clean[lucky].drop(lucky)  # lucky 与其他用户的相关系数 Series，不包含 lucky 自身 >> >
corr_lucky = corr_lucky[corr_lucky > 0.1].dropna()  # 筛选相关系数大于 0.1 的用户 >> >
for movie in gift.index:  # 遍历所有 lucky 没看过的电影
    prediction = []
    for other in corr_lucky.index:  # 遍历所有与 lucky 相关系数大于 0.1 的用户
        if not np.isnan(data.ix[other, movie]):
            prediction.append((data.ix[other, movie], corr_clean[lucky][other]))
    if prediction:
        gift[movie] = sum([value * weight for value, weight in prediction]) / sum([pair[1] for pair in prediction])

result=gift

print(result[:10])