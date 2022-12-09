#!/usr/bin/env python
# -*- coding:utf-8 -*-
import warnings
import numpy as np
import pandas as pd
import numpy as np
import tool
import pickle
from key_deal import SkDeal  # 引用类，密钥处理

warnings.filterwarnings("ignore")


class TrieNode:
    def __init__(self):
        self.child = {}
        self.id = None


class TrieTree:

    def __init__(self):
        self.algorithm = "trietree"
        self.root = TrieNode()

    def add_keyword(self, id, keyword):
        node_curr = self.root
        for word in keyword:
            index = tuple(word)
            if node_curr.child.get(index) is None:
                node_next = TrieNode()
                node_curr.child[index] = node_next  # 把孩子节点word的值赋给node_next
            node_curr = node_curr.child[index]
        node_curr.id = id
        return self.root

    def add_keywords_from_list(self, keywords, tree_hight): #split：树的高度
        for id, keyword in enumerate(keywords):
            split_index = np.array_split(keyword, tree_hight)
            self.add_keyword(id, split_index)


    def EncIndex(self, sk, Enc_index ,tree_level):  # I :onehot向量,只针对一条向量
        lens = len(Enc_index)
        S = sk[tree_level][2] # 划分向量
        r = np.random.randint(1, 10)  # 生成一个随机数,用于随机划分
        r_i = np.random.randint(1, 10)  # 生成一个随机数，用于向量相乘
        I_a = np.zeros(lens, dtype=np.int32)
        I_b = np.zeros(lens, dtype=np.int32)
        I = r_i * np.array(Enc_index)
        for j, vals in enumerate(S):
            if vals == 0:
                I_a[j] = I_b[j] = I[j]
            else:
                # 如果s_j=1
                I_a[j] = I[j] - r
                I_b[j] = r
                # I_a[j] = I_b[j] = I[j]
        I_1 = np.inner(sk[tree_level][0], I_a)
        I_2 = np.inner(sk[tree_level][1], I_b)  # 将M2矩阵转置后与I_b点乘
        E_Index = [tuple(I_1), tuple(I_2)]
        return tuple(E_Index)

    def BuildIndextree(self, sk):  # 必须要新建立一棵树才行,应该用层次遍历
        node_curr = self.root
        queue = []
        queue.append(node_curr)
        tree_level = -1
        while queue:
            i = 0
            numberFlag = len(queue)
            tree_level = tree_level +1
            while i < numberFlag:
                node_curr = queue.pop(0)  # 删除队列的第一个元素
                key = node_curr.child.keys()
                for k in tuple(key):
                    if node_curr.child.get(k) is not None:
                        enc_index = self.EncIndex(sk, k,tree_level)
                        node = node_curr.child.get(k)
                        dict = node_curr.child
                        queue.append(node)
                        # dict.update(enc_index=dict.pop(k)) #更改数据
                        dict[enc_index] = dict.pop(k)
                i +=1
        return self.root

