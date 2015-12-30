#coding=utf-8

from graph import Graph
from utils import evaluate

INFINITE = 99999999

class Model:
    def __init__(self, graph):
        self.__graph = graph

    def train(self):
        # dists = {}
        # nodes = self.__graph.all_nodes()
        # edges = self.__graph.all_edges()
        # for k in nodes:
        #     if k % 100 == 0: print k
        #     for i in nodes:
        #         if not dists.has_key(i): dists[i] = {}
        #         for j in nodes:
        #             dists[i][j] = INFINITE
        #             if not edges[i].has_key(k) or not edges[k].has_key(j): continue
        #             if edges[i][k] + edges[k][j] < dists[i][j]:
        #                 dists[i][j] = edges[i][k] + edges[k][j]
        # distList = list(dists.asList())
        # print distList
        # distList = sorted(distList, key=lambda x:x[2])

        cmn_neighbors = {}
        nodes = self.__graph.all_nodes()
        # edges = self.__graph.all_edges()
        for ni in nodes:
            # cmn_neighbors[ni] = {}
            linkis = self.__graph.node(ni)
            for nj in nodes:
                if nj <= ni: continue
                linkjs = self.__graph.node(nj)
                # cmn_neighbors[ni][nj] = len([x for x in linkis if x in linkjs])
                cmn_neighbors[(ni,nj)] = len([x for x in linkis if x in linkjs])
        return dict(sorted(cmn_neighbors.iteritems(), key=lambda x:x[1], reverse=True))

    def predict(self, cmn_neighbors, pred_num):
        pred_edges = list()
        cur_num = 0
        for nodes, neighbors in cmn_neighbors.iteritems():
            if cur_num < pred_num and self.__graph.edge(nodes[0], nodes[1]) is not None:
                pred_edges.append((nodes[0], nodes[1]))
                pred_edges.append((nodes[1], nodes[0]))
                cur_num += 2
        return pred_edges

def load_test():
    testset = list()
    with open('../data/test.txt', "r") as fp:
        data = fp.read()
        if "\r\n" in data:
            data_list = data.split("\r\n")
        else:
            data_list = data.split("\n")
        for s in data_list:
            comment_index = s.find("#")
            if comment_index != -1:
                s = s[: comment_index]
            if len(s) == 0:
                continue
            s = s.replace(" ", "\t")
            node_tuple = s.split("\t")
            testset.append(node_tuple)
    return testset

if __name__ == '__main__':
    g = Graph("../data/train.txt")
    g.read()
    model = Model(g)
    cmn_neighbors = model.train()
    result = model.predict(cmn_neighbors, 17646)
    test = load_test()
    evaluate(test, result)