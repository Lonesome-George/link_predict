#coding=utf-8

from __future__ import division
from utils import load_data_dict

trainData = '../data/train.txt'
testData = '../data/test.txt'
predictData = '../data/ensemble_result.txt'
validateResult = '../data/validate_result.txt'

if __name__=='__main__':
    trainset = load_data_dict(trainData)
    testset = load_data_dict(testData)
    predictset = load_data_dict(predictData)
    with open(validateResult, 'w') as fp:
        for node, train_friends in trainset.iteritems():
            if not testset.has_key(node):
                test_friends = []
            else:
                test_friends = testset[node]
            if not predictset.has_key(node):
                pred_friends = []
            else:
                pred_friends = predictset[node]
            fp.write('%d\t%d\t%d\t%d\t%f\n' % (node, len(train_friends),
                len(test_friends), len(pred_friends), len(test_friends)/len(train_friends)))
        fp.close()