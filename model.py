#coding=utf-8

from __future__ import division
from graph import Graph

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

if __name__ == '__main__':
    g = Graph("../data/train.txt")
    # g = Graph("../data/friends.txt")
    g.read()
    model = Model(g)
    ''' new version '''
    model.find_latent_friends()