import numpy as np


def get_table(img, table_info, color):
    score = []
    color
    for num, i in enumerate(table_info):
        if img[int(i[0])][int(i[1])] == color:
            score.append(0)
        else:
            score.append(1)

    score = np.array(score)
    return score


def calc_rate(img, info, color):
    rate = get_table(img, info, color)
    return rate.mean()
