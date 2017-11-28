import csv
import matplotlib.pyplot as plt
import scipy.stats as stats

# ========================获取数据集=================768rows============
def loadCsv(filename):
    lines = csv.reader(open(filename))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    return dataset


filename = "../../pima-indians-diabetes.data"
dataset = loadCsv(filename)
print("1、======Loaded data file %s with %d rows" % (filename, len(dataset)))

# =====================按76：33的比例随机分为训练集和测试集================
import random


def splitDataset(dataset, splitRatio):
    trainSize = int(len(dataset) * splitRatio)
    trainSet = []
    copy = list(dataset)
    while len(trainSet) < trainSize:
        index = random.randrange(len(copy))
        trainSet.append(copy.pop(index))
    return [trainSet, copy]
