#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np


def num_dict(rang_num):
    dict = {}
    for num in range(rang_num):
        a = int(num % 10000 / 1000) # 取千位数字
        b = int(num % 1000 / 100)  # 取百位数字
        c = int(num % 100 / 10)  # 取十位数字
        d = int(num % 10)  #
        num_vect = np.zeros(41, dtype=int)
        num_vect[0] = 1
        num_vect[a + 1] = 1
        num_vect[b + 11] = 1
        num_vect[c + 21] = 1
        num_vect[d + 31] = 1
        dict1 = {num: num_vect}
        dict.update(dict1)
    return dict


if __name__ == '__main__':
    dict = num_dict(10000)
    print(dict)
