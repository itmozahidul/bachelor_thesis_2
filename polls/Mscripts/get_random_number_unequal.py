import random


def get_random_number_unequal(no, rng):
    number_list = []
    for i in range(no):
        while True:
            number_tem = random.randint(0, rng)
            if len(number_list) == 0:
                number_list.append(number_tem)
                break
            else:
                if number_tem not in number_list:
                    number_list.append(number_tem)
                    break
    return number_list
