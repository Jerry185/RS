import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

with open('datasets/weibo/weibo_repost_network.csv', 'r') as f:
    rt_time = []
    for line in f:
        time= line.strip().split(',')[-1]
        day = time[7:9]
        hms= time[9:17].replace(':', '')
        time = int(day + hms)
        rt_time.append(time)
 #计算转发时间的先后顺序

array = np.array(rt_time)
order = array.argsort()
ranks = order.argsort()

'''################# 构建微博转发网络'''
G = nx.Graph()
with open('datasets/weibo/weibo_repost_network.csv', 'r') as f:
    for position, line in enumerate(f):
        mid, uid, rtmid, rtuid= line.strip().split(',')[:-1]
        G.add_edge(uid, rtuid, time = ranks[position])
edges,colors = zip(*nx.get_edge_attributes(G,'time').items())
degree=G.degree()#计算节点的出度
path_length = nx.all_pairs_shortest_path_length(G)
depth =[ path_length['2803301701'][i] for i in degree.keys()]
pos=nx.spring_layout(G) #设置网络的布局
fig = plt.figure("n1",figsize=(10, 8),facecolor='white')
nx.draw(G, pos, nodelist = degree.keys(),
        node_size = [np.sqrt(v+1)*10 for v in (degree.values())], node_color = depth,
        node_shape = 'o', cmap=plt.cm.hot,
        edgelist = edges, edge_color = 'gray', width = 0.5,
        with_labels = False, arrows = False)

'''
##############节点指标统计
'''
UG=G.to_undirected()
eccen = nx.eccentricity(UG)#节点离心度
max=max(eccen.values()) #4
min=min(eccen.values())#2
nx.diameter(G) # 网络直径4
nx.radius(G) #网络半径2
path =nx.all_pairs_shortest_path(G)
nx.shortest_path(G, source = '2803301701', target ='1783628693' )
#['2803301701', '1904107133', '1783628693']
nx.shortest_path_length(G, source = '2803301701', target ='1783628693' ) #2
nx.average_shortest_path_length(G) # 网络平均最短距离0.001
nx.average_shortest_path_length(UG) # 网络平均最短距离2.05

degree = nx.degree(G)  #度
closenesss = nx.closeness_centrality(G) #接近度
betweenness = nx.betweenness_centrality(G) #中间度

'''################## 网络的度的分布，双对数 '''
degree_hist = nx.degree_histogram(G)
x = range(len(degree_hist))
y = [i / int(sum(degree_hist)) for i in degree_hist]
plt.figure("n2",figsize=(10, 8),facecolor='white')
plt.subplot(1, 2, 1)
plt.loglog(x, y, color = 'blue', linewidth = 2, marker = 'o')
plt.title('Degree Distribution')
plt.ylabel('Probability')
plt.xlabel('Degree')


'''################### 网络的度的分布排名'''

from collections import defaultdict
import scipy.stats as ss

d = sorted(degree.values(), reverse = True )
d_table = defaultdict(int)
for k in d:
    d_table[k] += 1

d_value = sorted(d_table)
d_freq = [d_table[i] for i in d_value]
d_prob = [i/sum(d_freq) for i in d_freq]
d_rank = ss.rankdata(d_value).astype(int)
plt.subplot(1, 2, 2)
plt.loglog(d_rank, d_prob, color = 'blue', linewidth = 2, marker = 'o')
plt.title('Degree Rank-order Distribution')
plt.ylabel('Probability')
plt.xlabel('Rank')

'''##########################网络属性'''

G.number_of_nodes() # 节点数量1047
G.number_of_edges() # 链接数量1508
nx.density(G) # 网络密度0.001
nx.info(G)
#'Name: \nType: DiGraph\nNumber of nodes: 1047\nNumber of edges: 1518\nAverage in degree:   1.4499\nAverage out degree:   1.4499'
nx.transitivity(G) # 传递性0.001
nx.average_clustering(UG) # 网络群聚系数0.227
nx.degree_assortativity_coefficient(UG) # 匹配性-0.668

'''###################### 扩散度'''
eccen = nx.eccentricity(UG) #节点离心度
eccen['2803301701']  #深度为2, '2803301701'即@人民日报
#找到扩散深度最大的节点
path_length = nx.all_pairs_shortest_path_length(G)
oPath = path_length['2803301701']
maxDepth = filter(lambda x: oPath[x] == max(oPath.values()), oPath.keys())# 扩散深度最大的节点数量29


'''########################扩散速度'''
from datetime import datetime
with open('datasets/weibo/weibo_repost_network.csv', 'r') as f:
    rt_time = []
    for line in f:
        time= line.strip().split(',')[-1]
        day = time[7:9]
        hms= time[9:17].replace(':', '')
        time = int(day + hms)
        rt_time.append(time)

day = [('2014-08-0'+str(i)[:1]+'-'+str(i)[1:3]) for i in rt_time]
day = [datetime.strptime(d, '%Y-%m-%d-%H') for d in day]
day_weibo = datetime.strptime('2014-08-07-19', '%Y-%m-%d-%H') #源微博发出时间
hours = [(i-day_weibo).total_seconds()/3600 for i in day]
values, base = np.histogram(hours, bins = 40)
cumulative = np.cumsum(values)
plt.figure("n3",figsize=(10, 8),facecolor='white')
plt.subplot(1, 2, 1)
plt.plot(base[:-1], cumulative, c = 'red')
plt.title('Cumulative Diffusion')
plt.ylabel('Number of Retweets')
plt.xlabel('Hours')
plt.subplot(1, 2, 2 )
plt.plot(base[:-1], values, c = 'orange')
plt.title('Hourly Diffusion')
plt.xlabel('Hours')
plt.show()

