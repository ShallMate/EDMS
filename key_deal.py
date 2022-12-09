#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
import pickle


class SkDeal:
    def __init__(self, len, split):
        self.algorithm = "SkDeal"
        self.SK = self.genkey(len, split)

    def genkey(self, len, split):
        S = np.random.randint(0, 2, [len])
        SK = []
        split_index = np.array_split(S, split)
        for i, s in enumerate(split_index):
            len = s.size
            while True:
                m1 = np.random.randint(0, 2, [len, len])  # 01bit
                m2 = np.random.randint(0, 2, [len, len])
                if int(np.linalg.det(m1)) != 0:  # 可逆矩阵
                    if int(np.linalg.det(m2)) != 0:
                        break
            sk = [m1, m2, s]
            SK.append(sk)
        return SK

    def sk_tran(self, SK):  # 矩阵的转置
        SK_T = []
        for sk in SK:
            S = sk[2]
            M_T1 = np.transpose(sk[0])  # 矩阵的转置
            M_T2 = np.transpose(sk[1])
            sk_T = [M_T1, M_T2, S]
            SK_T.append(sk_T)
        return SK_T

    def sk_inv(self, SK):  # 矩阵的逆
        SK_l = []
        for sk in SK:
            S = sk[2]
            M_I1 = np.linalg.inv(sk[0])
            M_I2 = np.linalg.inv(sk[1])
            sk_l = [M_I1, M_I2, S]
            SK_l.append(sk_l)
        return SK_l


if __name__ == "__main__":
    sk = SkDeal(284, 22)
    sk_2 = sk.sk_tran(sk.SK)
    sk_3 = sk.sk_inv(sk.SK)
    file = open(".\doc\my_dump.txt", "wb")
    pickle.dump(sk, file)
    file.close()
    file = open(".\doc\my_dump.txt", "rb")
    p = pickle.load(file)
    file.close()
