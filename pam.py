import csv
import numpy as np
import random
import math
import sys

def dtw_distance(a, b, w=10):
    
    n, m = len(a), len(b)
    dtw_matrix = np.zeros((n+1, m+1))
    
    for i in range(n+1):
        for j in range(m+1):
            dtw_matrix[i, j] = np.inf
    dtw_matrix[0, 0] = 0
    
    for i in range(1, n+1):
        for j in range(np.max([1, i-w]), np.min([m, i+w])+1):
            dtw_matrix[i, j] = 0
    
    for i in range(1, n+1):
        for j in range(np.max([1, i-w]), np.min([m, i+w])+1):
            # can change to different formula
            cost = abs(a[i-1] - b[j-1])
            # edit distance logic to find min path/value
            dtw_matrix[i, j] = cost + np.min([dtw_matrix[i-1, j-1], dtw_matrix[i, j-1], dtw_matrix[i-1, j]])

    return dtw_matrix[n,m]

def get_total_distance(p,coll):
    cost = 0
    for c in coll:
        cost += dtw_distance(c,p)
    return cost    

def average_silhouette_coefficient(data_set, cluster):
    rv = 0
    for i in range(0, len(data_set)):
        c = cluster[i]
        a = 0
        a_num = 0
        b = {}
        for j in range(0, len(cluster)):
            if i == j:
                continue
            c1 = cluster[j]
            dis = dtw_distance(data_set[i], data_set[j])
            if c1 == c:
                a += dis
                a_num += 1
            else:
                if c1 not in b:
                    b[c1] = [dis]
                else:
                    b[c1].append(dis)
        a_value , b_value = 0, 0
        if a_num != 0:
            a_value = a / a_num
        if len(b) != 0:
            b_value = min([0 if len(b[i]) == 0 else sum(b[i]) / len(b[i]) for i in b])			   
        s = (b_value - a_value) / max(a_value, b_value)
        rv += s
    return rv / len(data_set)

def pam(data_set, k):
    m = len(data_set)
    n = len(data_set[0])
    # random position of first centriod
    index = random.sample(list(range(m)), k)
    # index = far_possible(data_set,index[0],k)
    centroids = [[0 for i in range(n)]for i in range(k)]

    for i, j in enumerate(index):
        centroids[i] = data_set[j]
   # print centroids
    # cluster[i] means the cluster[i]'s centroid
    cluster = [-1 for i in range(m)]
    stop = False
    print(m,n)
    while not stop:
        stop = True
        for i in range(0, m):
            pos = cluster[i]
            min_distance = float('inf')
            if (pos != -1):
                min_distance = dis = dtw_distance(centroids[pos], data_set[i])
            #print("54th")
            for j in range(0, k):
                if (j == pos):
                    #print("57th")
                    continue
                dis = dtw_distance(centroids[j], data_set[i])
                if dis < min_distance:
                    min_distance = dis
                    pos = j
            if cluster[i] != pos:
                #stop = False
                cluster[i] = pos
        #print("66th")        
        for j in range(0, k):
            coll = []
            for u in range(0, len(cluster)):
                if cluster[u] == j:
                    coll.append(data_set[u])
            if len(coll) > 0:
                cost = get_total_distance(centroids[j],coll)
                new_centroid = centroids[j]
                for p in coll:
                    # try different point
                    if (centroids[j] == p):
                       # print("78th")
                        continue
                    new_cost = get_total_distance(p,coll)
                    if cost > new_cost:
                        cost = new_cost
                        new_centroid = p
                if new_centroid != centroids[j]:
                    stop = False
                    centroids[j] = new_centroid       


        #print cluster, centroids
    return cluster, centroids

def read_file(file_name):
    rv = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                
                line_count += 1
            else:
                row = list(map(float,row))
                rv.append(row)
                line_count += 1
    print(f'Processed {line_count} lines.')
    return rv

if __name__ == '__main__':
    # please use csv file
    cal = {}
    rv = read_file(sys.argv[1])
   # print(rv)
    size = int(sys.argv[3])
    cluster, centroids =  pam(rv[0:size],int(sys.argv[2]))
    print(centroids)
    print(cluster)
    print(average_silhouette_coefficient(rv[0:size],cluster))
    sse = 0
    for i in range(0, len(cluster)):
        index = cluster[i]
        sse += dtw_distance(rv[0:int(sys.argv[2])][i], centroids[index])
    print(sse)    
    #print(dtw_distance(rv[0],rv[1]))
