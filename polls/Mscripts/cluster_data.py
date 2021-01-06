from .get_best_cluster import get_best_cluster
from .kmeans_alg import kmeans


# i represents number of sample with one k value. each time it taks different initial centers.
# with get_best_cluster() function it chooses one cluster with minimum variance.


def cluster_data(data, k, step):
    clusters_list = []
    shift = 1
    i = 0
    while True:
        if i == step:
            break
        clusters = kmeans(data, k, shift)
        clusters_list.append(clusters)
        shift += 10
        i += 1
    return get_best_cluster(clusters_list)
