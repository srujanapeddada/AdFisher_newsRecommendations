import sys
import numpy as np
sys.path.append("../core")
import analysis.permutation_test
import analysis.statistics
import random
import converter.reader

log_file = 'log.nyt_searchAndClick_Sports.txt'
nfeat = 5

def means(X_test, y_test):
    n, x1, x0 = 0., [0.]*X_test.shape[2], [0.]*X_test.shape[2]
    for i in xrange(0, X_test.shape[0]):
        for j in xrange(0, X_test.shape[1]):
            n += 1.
            arr = X_test[i][j]
#             avg = np.sum(arr*np.arange(len(arr)))/np.sum(arr)
            if(y_test[i][j] == 1):
                x1 += arr
            else:
                x0 += arr
    return 2*x0/n, 2*x1/n

def variances(X_test, y_test, x0, x1):
    n, var0, var1 = 0., [0.]*X_test.shape[2], [0.]*X_test.shape[2]
    for i in xrange(0, X_test.shape[0]):
        for j in xrange(0, X_test.shape[1]):
            n += 1.
            arr = X_test[i][j]
            if(y_test[i][j] == 1):
                var1 += (np.square(arr - x1))
            else:
                var0 += (np.square(arr - x0))
    return 2*var0/n, 2*var1/n

def compute_A(X_test,y_test, a=1, b=0):
    count, g, e = 0., [0.]*X_test.shape[2], [0.]*X_test.shape[2]
#     print X_test
#     print y_test
    for i in xrange(0, X_test.shape[0]):
        for m in xrange(0, X_test.shape[1]):
            for n in xrange(0, X_test.shape[1]):
#                 print m, n
#                 print y_test[i]
                if(y_test[i][m] == a and  y_test[i][n] == b):
                    count += 1.
#                     print m, X_test[i][m]
#                     print n, X_test[i][n]
                    arra = X_test[i][m]
                    arrb = X_test[i][n]
                    g = np.array(arra>arrb) + g
                    e = np.array(arra==arrb) + e
    return g,e,count
    

def compute_effect_size(X, y, type):
    if type == 'cohen d':
        x0, x1 = means(X, y)
        var0, var1 = variances(X, y, x0, x1)
        s = np.sqrt((var0+var1)/2.)
        es10 = (x1-x0)/s
        topk1 = np.argsort(es)[::-1][:nfeat]
        topk0 = np.argsort(es)[:nfeat]
        return es10, es10, topk1, topk0
    elif type == 'A' or type == 'delta' or type == 'CL':
        g10, e10, count = compute_A(X,y,a=1,b=0)
        g01, e01, count = compute_A(X,y,a=0,b=1)
        if type == 'A':
            A10 = (g10+0.5*e10)/count
            A01 = (g01+0.5*e01)/count
            topk1 = np.argsort(A10)[::-1][:nfeat]
            topk0 = np.argsort(A01)[::-1][:nfeat]
            return A10, A01, topk1, topk0
        if type == 'CL':
            CL10 = g10/count
            CL01 = g01/count
            topk1 = np.argsort(CL10)[::-1][:nfeat]
            topk0 = np.argsort(CL01)[::-1][:nfeat]
            return CL10, CL01, topk1, topk0
        if type == 'delta':
            CL10 = g10/count
            CL01 = g01/count
            d10 = CL10-CL01
            topk1 = np.argsort(d10)[::-1][:nfeat]
            topk0 = np.argsort(d10)[:nfeat]
            return d10, d10, topk1, topk0
            


collection, names = converter.reader.read_log(log_file)
X, y, feat = converter.reader.get_feature_vectors(collection[:100], feat_choice='news')
es1, es0, topk1, topk0 = compute_effect_size(X,y, type = 'CL')
# es = compute_effect_size(X,y, type = 'cohen d')


for i in topk0:
    print es0[i]
    feat.choose_by_index(i).display()

print "--------------------------------"

for i in topk1:
    print es1[i]
    feat.choose_by_index(i).display()

analysis.statistics.print_frequencies(X, y, feat, topk0, topk1)

print np.sort(es1)
print np.sort(es0)
