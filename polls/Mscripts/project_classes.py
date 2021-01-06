class cluster_n_element:
    def __init__(self, cluster, element):
        self.cluster = cluster
        self.element = element


class distance_n_center:
    def __init__(self, distance, center):
        self.distance = distance
        self.center = center


class cluster_n_list_element:
    def __init__(self, listelement, cluster, lock):
        self.cluster = cluster
        self.listelement = listelement
        self.lock = lock


class query_n_sentence_list:
    def __init__(self, query, sentence_list):
        self.query = query
        self.hs = 0
        self.nhs = 0
        self.sentence_list = sentence_list


class json_data_cls:
    def __init__(self, data, user, userno):
        self.data = data
        self.user = user
        self.userno = userno


class fileInfo:
    def __init__(self, url, name):
        self.name = name
        self.url = url