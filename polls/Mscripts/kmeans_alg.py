from scipy import spatial

from .project_classes import cluster_n_element, cluster_n_list_element, distance_n_center
from .get_random_number_unequal import get_random_number_unequal


def kmeans(data, k, shift):
    clusters = []
    clustered_element_list = []
    print('############whileloop1 start##################')
    # lock = 0
    cluster_centers = []
    while True:
        print('############whileloop2 start##################')
        cluster_list_temp = []
        if len(cluster_centers) == 0:
            index_list = get_random_number_unequal(k, len(data) - 1)
            for index in index_list:
                print('index ' + str(index))
                cluster_centers.append(data[index])
        for v in data:
            dist_n_cluster_dic_temp = []
            distance_temp = []
            for c in cluster_centers:
                dist_n_cluster_dic_temp.append(distance_n_center(spatial.distance.cosine(c, v), c))
                distance_temp.append(spatial.distance.cosine(c, v))
            for d in dist_n_cluster_dic_temp:
                if d.distance == min(distance_temp):
                    cluster_list_temp.append(cluster_n_element(d.center, v))
            distance_temp.clear()
            dist_n_cluster_dic_temp.clear()

        print('centers_no = ' + str(len(cluster_centers)))
        lock = 0
        for c in cluster_centers:
            list_v = []
            list_v_l = []
            for e in cluster_list_temp:
                if (e.cluster == c).all():
                    list_v_l.append(e.element.tolist())
                    list_v.append(e.element)
            if len(list_v) != 0:
                new_center = sum(list_v) / len(list_v)
            else:
                new_center = c
            if (c == new_center).all():
                print('---------------------------------------------')
                clusters.append(cluster_n_list_element(list_v, c, 1))
                lock = lock + 1

            else:
                clusters.append(cluster_n_list_element(list_v, new_center, 0))
                print('+++++++++++++++++++++++++++++++++++++++++++++')
        for x in clusters:
            print('element_length' + str(len(x.listelement)))
        print('lock = ' + str(lock))
        print('value of k = ' + str(k))
        if lock == k:
            break
        else:
            cluster_centers.clear()
            for y in clusters:
                cluster_centers.append(y.cluster)
            clusters.clear()
    for el in clusters:
        clustered_element_list.append(el.listelement)
    return clusters
