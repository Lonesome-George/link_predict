#coding=utf-8

# stat ratio that test / train

from __future__ import division
from graph import Graph
from utils import separate_edge_rate, load_data_dict

trainData = '../data/train.txt'
testData = '../data/test.txt'
ratioStat = '../data/ratio.txt'

def create_test():
    # read original data as graph
    g = Graph("../data/friends.txt")
    # load data
    g.read()
    # separate data as 90% train set and 10% test set
    sep = separate_edge_rate(g, 0.1)
    # write test set to "test.txt" file
    with open("../data/test.txt", "w") as fp:
        for e in sep:
            fp.write("%s\t%s\n" % (e[0], e[1]))
    # write train set to "train.txt" file
    g.write("../data/train.txt")

def stat_ratio():
    ratios = {}
    count = 100
    for i in range(count):
        print i
        create_test()
        trainset = load_data_dict(trainData)
        testset = load_data_dict(testData)
        for node, train_friends in trainset.iteritems():
            if not testset.has_key(node):
                test_friends = []
            else:
                test_friends = testset[node]
            if not ratios.has_key(node): ratios[node] = 0
            ratios[node] += len(test_friends) / len(train_friends)
    with open(ratioStat, 'w') as fp:
        for node, ratio in ratios.iteritems():
            fp.write('%d\t%.3f\n' % (node, ratios[node]/count))
        fp.close()

if __name__=='__main__':
    stat_ratio()