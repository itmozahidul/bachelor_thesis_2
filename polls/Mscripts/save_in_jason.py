import json
import os

from .fleiss_kappa_value_k import fleiss_kappa_value_k
from .project_classes import json_data_cls


def save_in_json(query_n_sentences_list):
    ans = 0
    if not os.path.isfile('./media/Survey_info/json_data.json'):
        query_n_sentences_dic_list = []
        for q_n_s_l in query_n_sentences_list:
            query_n_sentences_dic_list.append(q_n_s_l.__dict__)
        json_data_ob = json_data_cls(query_n_sentences_dic_list, [], 0)
        with open('./media/Survey_info/json_data.json', 'w') as j_d_f_w1:
            json.dump(json_data_ob.__dict__, j_d_f_w1)
        j_d_f_w1.close()
        ans = 1
    return ans


def edit_in_json(request_POST):
    name = request_POST['user']
    ans = 0
    fleiss_kappa = 0

    if os.path.isfile('./media/Survey_info/json_data.json'):
        pfd = open('./media/Survey_info/json_data.json')
        json_data = json.load(pfd)
        pfd.close()
        for data in json_data["data"]:
            temp_hs = 0
            temp_nhs = 0
            for s_l in data['sentence_list']:

                if data['query'] + s_l + '1' in request_POST:
                    temp_hs += 1

                if data['query'] + s_l + '0' in request_POST:
                    temp_nhs += 1
            data['hs'] = int(data['hs']) + temp_hs
            data['nhs'] = int(data['nhs']) + temp_nhs

        if name not in json_data['user']:
            json_data['user'].append(name)
            json_data['userno'] += 1
            json_data_ob2 = json_data_cls(json_data["data"], json_data['user'], json_data['userno'])

            if json_data['userno'] == 3:
                data_Matrix =[]
                for product in json_data["data"]:
                    data_Matrix.append([product['hs'], product['nhs']])
                fleiss_kappa = fleiss_kappa_value_k(data_Matrix)

            else:
                with open('./media/Survey_info/json_data.json', 'w') as j_d_f_w2:
                    json.dump(json_data_ob2.__dict__, j_d_f_w2)
                    ans = 1
                j_d_f_w2.close()


    return [fleiss_kappa, ans]
