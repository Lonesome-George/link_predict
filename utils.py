#coding=utf-8

import random

def separate_edge_sum(graph, edge_sum):
    sep_edge = set()
    forbidden = set()
    while True:
        if not graph.direct_graph():
            if len(sep_edge) / 2 == edge_sum:
                break
        else:
            if len(sep_edge) == edge_sum:
                break
        node_a_list = list(graph.all_nodes() - forbidden)
        if len(node_a_list) == 0:
            break
        node_a = random.choice(node_a_list)
        if len(graph.node(node_a)) == 1:
            forbidden.add(node_a)
            continue
        node_b_list = list(set(graph.node(node_a)) - forbidden)
        if len(node_b_list) == 0:
            forbidden.add(node_a)
            continue
        node_b = random.choice(node_b_list)
        if len(graph.node(node_b)) == 1:
            forbidden.add(node_b)
            continue
        sep_edge.add((node_a, node_b))
        if not graph.direct_graph():
            sep_edge.add((node_b, node_a))
        graph.del_edge(node_a, node_b)
    return sep_edge

def separate_edge_rate(graph, edge_rate):
    if not 0 < edge_rate < 1:
        return set()
    edge_sum = int(graph.sum_edges() * edge_rate)
    return separate_edge_sum(graph, edge_sum)

def evaluate(test, result, quiet=False):
    test_copy = result.copy()
    for node_tuple in test_copy:
        result.add((node_tuple[1], node_tuple[0]))
    hit_sum = len(test & result)
    precision = 1.0 * hit_sum / len(result)
    recall = 1.0 * hit_sum / len(test)
    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    if not quiet:
        print("Hit Sum: %d" % hit_sum)
        print("Precision: %f" % precision)
        print("Recall: %f" % recall)
        print("F1: %f" % f1)
    rst = {"Hit Sum": hit_sum, "Precision": precision, "Recall": recall, "F1": f1}
    return rst

def load_data_list(filename):
    dataset = []
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
            if len(s) == 0: continue
            s = s.replace(" ", "\t")
            tup = tuple(s.split("\t"))
            inttup = []
            for t in tup:
                if t.find('.') == -1: inttup.append(int(t))
                else: inttup.append(float(t))
            dataset.append(tuple(inttup))
    return dataset

def load_data_set(filename):
    return set(load_data_list(filename))

# 潜在朋友，包含二度和三度人脉
def latent_friends(node, graph):
    links = set(graph.node(node).keys())
    temp_links = set()
    for node in links:
        temp_links = temp_links | set(graph.node(node).keys())
    links = links | temp_links
    return links