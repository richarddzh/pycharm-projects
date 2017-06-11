def last_index(a_list, func):
    for i in range(len(a_list) - 1, -1, -1):
        if func(a_list[i]):
            return i
    return -1
