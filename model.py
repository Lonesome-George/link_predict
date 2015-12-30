#coding=utf-8

from __future__ import division
from graph import Graph
from utils import evaluate

INFINITE = 99999999

class Model:
    def __init__(self, graph):
        self.__graph = graph

    def train(self):
        cmn_neighbors = {}
        nodes = self.__graph.all_nodes()
        for ni in nodes:
            linkis = self.__graph.node(ni)
            for nj in nodes:
                if nj <= ni or self.__graph.edge(ni, nj) is not None: continue
                linkjs = self.__graph.node(nj)
                intersect =[x for x in linkis if x in linkjs]
                cmn_neighbors[(ni,nj)] = len(intersect) / (len(linkis) + len(linkjs) - len(intersect))
        return dict(sorted(cmn_neighbors.iteritems(), key=lambda x:x[1], reverse=True))

    def predict(self, cmn_neighbors, pred_num):
        pred_edges = set()
        cur_num = 0
        for nodes, neighbors in cmn_neighbors.iteritems():
            if cur_num < pred_num:
                pred_edges.add((nodes[0], nodes[1]))
                pred_edges.add((nodes[1], nodes[0]))
                cur_num += 2
        with open('../data/result.txt', "w") as fp:
            for pred_edge in pred_edges:
                string = '%d\t%d\n' % (pred_edge[0], pred_edge[1])
                fp.write(string)
            fp.close()
        return pred_edges

def load_data(filename):
    dataset = set()
    with open(filename, "r") as fp:
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
            node_tuple = tuple(s.split("\t"))
            dataset.add(node_tuple)
    return dataset

if __name__ == '__main__':
    g = Graph("../data/train.txt")
    g.read()
    model = Model(g)
    cmn_neighbors = model.train()
    result = model.predict(cmn_neighbors, 17646)
    result = load_data('../data/result.txt')
    test = load_data('../data/test.txt')
    evaluate(test, result)