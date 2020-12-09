import numpy as np


def get_table(img, table_info):
    for num, i in enumerate(table_info):
        if not (img[int(i[0])][int(i[1])] == i[2]):
            if i[3]:
                table_info[num] = [int(i[0]), int(i[1]), img[int(i[0])][int(i[1])], 0]
            else:
                table_info[num] = [int(i[0]), int(i[1]), img[int(i[0])][int(i[1])], 1]


def calc_rate(img, info):
    table_info = info
    get_table(img, table_info)
    table = np.array(table_info).T
    return (table[3][:]).mean()
