from scipy import spatial


def get_total_variance(data_list, center):
    distances_from_center = []
    squered_distances_from_center = []

    print('#############################################################################choosen data len ' + str(
        len(data_list)))
    for data in data_list:
        distances_from_center.append(spatial.distance.cosine(center, data))
    avg_distance_from_center = sum(distances_from_center) / len(distances_from_center)
    for a in distances_from_center:
        squered_distances_from_center.append(pow(a, 2))

    return (sum(squered_distances_from_center) - pow(avg_distance_from_center, 2))
