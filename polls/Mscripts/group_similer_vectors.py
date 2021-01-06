from .cluster_data import cluster_data
from .variance import get_total_variance


def group_similer_vectors(data, n):
    k = 2
    clusters_list = []
    cluster_n_variance_dic = {}
    while True:
        if k == len(data):
            break
        Clusters = cluster_data(data, k, 4)
        clusters_list.append(Clusters)
        k += 1
    for clusters in clusters_list:
        variance = 0
        for cluster in clusters:
            variance = variance + get_total_variance(cluster.listelement, cluster.cluster)
        cluster_n_variance_dic[variance] = len(clusters)
    ans = []
    x = []
    y = []
    for b in cluster_n_variance_dic:
        y.append(b)
        x.append(cluster_n_variance_dic[b])

    for c in clusters_list:
        print(n)
        if len(c) == int(n):
            ans = c
    print('ans len ' + str(len(ans)))

    return [ans, x, y]
