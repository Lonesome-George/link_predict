#coding=utf-8

from __future__ import division
from graph import Graph
from utils import evaluate, load_data_set, latent_friends
import math

INFINITE = 99999999
MIN_TOTAL_FRIENDS = 20

class Model:
    def __init__(self, graph):
        self.__graph = graph
        self.__conns = {}

    def find_latent_friends(self):
        for ni in self.__graph.all_nodes():
            if ni % 100 == 0: print ni
            if not self.__conns.has_key(ni):
                self.__conns[ni] = {}
            fringe_nodes = set(self.__graph.node(ni).keys())
            if len(fringe_nodes) < 2: continue # 自己的直接朋友少于2,认为自己没有其他朋友
            for k in range(2,3):
                fringe_nodes = self.find_kdegree_friends(ni, fringe_nodes, k)
                for nj in fringe_nodes:
                    if self.__graph.edge(ni, nj) is None: self.__conns[ni][nj] = k
        filename = '../data/friends_latent.txt'
        with open(filename, 'w') as fp:
            for nodei, items in self.__conns.iteritems():
                for nodej, dist in items.iteritems():
                    string = '%d\t%d\t%d\n' %(nodei, nodej, dist)
                    fp.write(string)
            fp.close()

    # 查找k度人脉
    def find_kdegree_friends(self, me, nodes, k):
        kfriends = {}
        if k > 1:
            for node in nodes:
                fringe_nodes = set(self.__graph.node(node).keys())
                for nj in fringe_nodes:
                    if me == nj: continue
                    else:
                        cmn_friends = self.find_common_friends(fringe_nodes, set(self.__graph.node(nj).keys()))
                        kfriends[nj] = cmn_friends
        kfriends = sorted(kfriends.iteritems(), key=lambda x:x[1], reverse=True)
        return set([x[0] for x in kfriends])

    def find_common_friends(self, nodes_a, nodes_b):
        return len(nodes_a & nodes_b)

    def train(self):
        link_scores = {}
        nodes = self.__graph.all_nodes()
        for ni in nodes:
            linkis = self.__graph.node(ni)
            for nj in nodes:
                if ni >= nj or self.__graph.edge(ni, nj) is not None: continue
                linkjs = self.__graph.node(nj)
                # cmn_neighbors = [x for x in linkis if x in linkjs]
                # adamic_coef = 0.0
                # for node in cmn_neighbors:
                #     adamic_coef += 1 / math.log(len(self.__graph.node(node)))
                # link_scores[(ni,nj)] = adamic_coef
                link_scores[(ni,nj)] = len(linkis) * len(linkjs)
        return dict(sorted(link_scores.iteritems(), key=lambda x:x[1], reverse=True))

    def train_v2(self):
        friends_latent = load_data_set('../data/friends_latent.txt')
        link_scores = {}
        idx = 0
        for ni, nj, dist in friends_latent:
            if idx % 10000 == 0: print idx
            idx += 1
            linkis = latent_friends(ni, self.__graph)
            linkjs = latent_friends(nj, self.__graph)
            # if linkis is None or linkjs is None: continue
            # else: link_scores[(ni,nj)] = len(linkis) * len(linkjs)
            if len(linkis) == 0 or len(linkjs) == 0: continue
            else:
                # cmn_neighbors = [x for x in linkis if x in linkjs]
                # adamic_coef = 0.0
                # for node in cmn_neighbors:
                #     adamic_coef += 1 / math.log(len(self.__graph.node(node)))
                # link_scores[(ni,nj)] = adamic_coef
                link_scores[(ni,nj)] = len(linkis & linkjs) #len(cmn_neighbors)
        return dict(sorted(link_scores.iteritems(), key=lambda x:x[1], reverse=True))

    def predict(self, link_scores, pred_num):
        pred_edges = set()
        cur_num = 0
        for nodes, score in link_scores.iteritems():
            if cur_num < pred_num:
                pred_edges.add((nodes[0], nodes[1]))
                pred_edges.add((nodes[1], nodes[0]))
                cur_num += 2
        with open('../data/result.txt', "w") as fp:
            for pred_edge in pred_edges:
                string = '%s\t%s\n' % (pred_edge[0], pred_edge[1])
                fp.write(string)
            fp.close()
        return pred_edges

if __name__ == '__main__':
    g = Graph("../data/train.txt")
    g.read()
    model = Model(g)
    # link_scores = model.train()
    # result = model.predict(link_scores, 17646)
    ''' new version '''
    model.find_latent_friends()
    # link_scores = model.train_v2()
    # result = load_data_set('../data/result.txt')
    # test = load_data_set('../data/test.txt')
    # evaluate(test, result)