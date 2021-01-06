def fleiss_kappa_value_k(M):
    P_c = 0
    P_0 = 0
    k = 0
    print('Raw M')
    print(M)
    list_of_Raw_element_list = M
    list_of_Colum_element_list = []
    all_element_sum = 0
    for i in range(len(M[0])):
        Colum_element_list = []
        for r in M:
            Colum_element_list.append(r[i])
        list_of_Colum_element_list.append(Colum_element_list)
    print('colum M')
    print(list_of_Colum_element_list)
    # P_c calculation
    for e1 in list_of_Colum_element_list:
        all_element_sum += sum(e1)
    for e1 in list_of_Colum_element_list:
        P_c += pow((sum(e1) / all_element_sum), 2)
    print('P_c')
    print(P_c)
    # P_0 calculation

    temp_P_0 = 0
    for f1 in list_of_Raw_element_list:
        total_vote_no = sum(f1)
        temp = 0
        for f2 in f1:
            temp += (pow(f2, 2) - f2)
        temp_P_0 += (temp / (total_vote_no * (total_vote_no - 1)))
    P_0 = temp_P_0 / len(M)
    print('P_0')
    print(P_0)
    k = (P_0 - P_c) / (1 - P_c)
    return k
