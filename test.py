from __future__ import division
from utils import evaluate, load_data_list, load_data_set, load_data_dict
from graph import Graph
import math

def test_precs():
    friends_latent = load_data_set('../data/friends_latent.txt')
    friends = set()
    for link in friends_latent:
        friends.add((link[0], link[1]))
    test = load_data_set('../data/test.txt')
    print len(friends & test)

def common_friends(graph, node_a, node_b):
    friends_a = set(graph.node(node_a).keys())
    friends_b = set(graph.node(node_b).keys())
    return friends_a & friends_b

def test_cmn_friends():
    g = Graph("../data/train.txt")
    # g = Graph("../data/friends.txt")
    g.read()
    test = load_data_list("../data/friends_latent.txt")
    with open('../data/test_result.txt', 'w') as fp:
        for t in test:
            fp.write('%d\t%d\t%d\n' % (t[0], t[1], len(common_friends(g, t[0], t[1]))))
        fp.close()

def test_jaccard():
    g = Graph("../data/train.txt")
    # g = Graph("../data/friends.txt")
    g.read()
    test = load_data_list("../data/friends_latent.txt")
    with open('../data/test_result2.txt', 'w') as fp:
        for t in test:
            friends_a = set(g.node(t[0]).keys())
            friends_b = set(g.node(t[1]).keys())
            cmn_friends = friends_a & friends_b
            jaccard = len(cmn_friends) / (len(friends_a) + len(friends_b) - len(cmn_friends))
            fp.write('%d\t%d\t%f\n' % (t[0], t[1], jaccard))
        fp.close()

def test_adamic():
    g = Graph("../data/train.txt")
    # g = Graph("../data/friends.txt")
    g.read()
    test = load_data_list("../data/friends_latent.txt")
    with open('../data/test_result3.txt', 'w') as fp:
        for t in test:
            friends_a = set(g.node(t[0]).keys())
            friends_b = set(g.node(t[1]).keys())
            cmn_friends = friends_a & friends_b
            adamic_coef = 0.0
            for node in cmn_friends:
                adamic_coef += 1 / math.log(len(g.node(node)))
            fp.write('%d\t%d\t%f\n' % (t[0], t[1], adamic_coef))
        fp.close()

def test_pren_attachment():
    g = Graph("../data/train.txt")
    # g = Graph("../data/friends.txt")
    g.read()
    test = load_data_list("../data/friends_latent.txt")
    with open('../data/test_result4.txt', 'w') as fp:
        for t in test:
            friends_a = set(g.node(t[0]).keys())
            friends_b = set(g.node(t[1]).keys())
            fp.write('%d\t%d\t%d\n' % (t[0], t[1], len(friends_a) * len(friends_b)))
        fp.close()

def normalize(link_scores):
    if not link_scores: return {}
    max_score = max(link_scores.values())
    for link, score in link_scores.iteritems():
        link_scores[link] = score / max_score
    return link_scores

def ensemble():
    trainset = load_data_dict('../data/train.txt')
    ratios = load_data_dict('../data/ratio.txt') # ratio that testset / trainset
    link_scores = {}
    filenames = ('../data/test_result.txt', '../data/test_result2.txt', '../data/test_result3.txt', '../data/test_result4.txt')
    for filename in filenames:
        result = load_data_list(filename)
        temp_scores = {}
        node = 0
        for ni, nj, score in result:
            if ni == node:
                temp_scores[(ni, nj)] = score
            else:
                for link, score in normalize(temp_scores).iteritems():
                    if not link_scores.has_key(link[0]): link_scores[link[0]] = {}
                    if not link_scores[link[0]].has_key(link[1]): link_scores[link[0]][link[1]] = 0
                    link_scores[link[0]][link[1]] += score
                node = ni
                temp_scores = {}
                temp_scores[(ni, nj)] = score
    with open('../data/ensemble_result.txt', 'w') as fp:
        result_set = set()
        total_count = 0
        for ni, temp_scores in link_scores.iteritems():
            count = int(ratios[ni][0] * len(trainset[ni]))
            if count > 1: count -= 1
            temp_scores = dict(sorted(temp_scores.iteritems(), key=lambda x:x[1], reverse=True)[0:count])
            for nj, score in temp_scores.iteritems():
                if (ni,nj) in result_set: continue
                fp.write('%d\t%d\n' % (ni, nj))
                fp.write('%d\t%d\n' % (nj, ni))
                result_set.add((ni,nj))
                result_set.add((nj,ni))
                total_count += 2
        print 'total_count:', total_count
        fp.close()

if __name__ == '__main__':
    # test_precs()
    test_cmn_friends()
    test_jaccard()
    test_adamic()
    test_pren_attachment()
    ensemble()
    result = load_data_set('../data/ensemble_result.txt')
    test = load_data_set('../data/test.txt')
    evaluate(test, result)

