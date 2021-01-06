from .variance import get_total_variance


def get_best_cluster(set_of_all_clusters_for_different_initial_value):
    choosen_cluster_no = 0
    Choosen_clusters = []
    Total_Variance_n_clusters_dictionary = {}
    Total_Variance_list = []

    for Clusters in set_of_all_clusters_for_different_initial_value:
        cluster_number = len(Clusters)
        varianc_list = []
        for Cluster in Clusters:
            if len(Cluster.listelement) != 0:
                variance = get_total_variance(Cluster.listelement, Cluster.cluster)
                varianc_list.append(variance)

        print(sum(varianc_list))
        print(cluster_number)
        Total_Variance_n_clusters_dictionary[sum(varianc_list)] = Clusters
        Total_Variance_list.append(sum(varianc_list))
    for sum_of_variance in Total_Variance_n_clusters_dictionary:
        if sum_of_variance == min(Total_Variance_list):
            Choosen_clusters = Total_Variance_n_clusters_dictionary[sum_of_variance]
    return Choosen_clusters


def get_best_cluster_with_different_length(set_of_all_clusters_for_different_initial_value):
    choosen_cluster_no = 0
    Choosen_clusters = []
    Total_Variance_n_clusterNo_dictionary = {}
    Total_Variance_list = []
    for Clusters in set_of_all_clusters_for_different_initial_value:
        cluster_number = len(Clusters)
        varianc_list = []
        for Cluster in Clusters:
            variance = get_total_variance(Cluster.listelement, Cluster.cluster)
            varianc_list.append(variance)
        print(sum(varianc_list))
        print(cluster_number)
        Total_Variance_n_clusterNo_dictionary[cluster_number] = sum(varianc_list)
        Total_Variance_list.append(sum(varianc_list))
        print(
            '#############################################################################choosen clusters len ' + str(
                len(Total_Variance_n_clusterNo_dictionary)))
    for cl_num in Total_Variance_n_clusterNo_dictionary:
        print('min v_l :' + str(cl_num) + ' min_V :' + str(min(Total_Variance_list)))
        if Total_Variance_n_clusterNo_dictionary[cl_num] == min(Total_Variance_list):
            choosen_cluster_no = cl_num
    for Clusters in set_of_all_clusters_for_different_initial_value:
        if len(Clusters) == choosen_cluster_no:
            Choosen_clusters = Clusters

    return Choosen_clusters
