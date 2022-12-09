#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from pre_tree import TrieNode


def add_keyword(node, id, keyword):
    node_curr = node
    for word in keyword:
        index = tuple(word)
        if node_curr.child.get(index) is None:
            node_next = TrieNode()
            node_curr.child[index] = node_next  # 把孩子节点word的值赋给node_next
        node_curr = node_curr.child[index]
    node_curr.id = id

def insert(search_Tree, Trapdoor,index,id): #输入查询，索引，id
    node_curr = search_Tree  # 关键词的头, 每遍历完一遍后需要重新初始化
    queue = []
    queue.append(node_curr)
    tree_level = -1
    while queue:
        i = 0
        numberFlag = len(queue)
        tree_level = tree_level + 1
        while i < numberFlag:
            node_curr = queue.pop(0)
            key = node_curr.child.keys()
            for k in key:
                La = np.array(k[0])
                Lb = np.array(k[1])
                R_i = np.dot(La, Trapdoor[tree_level][0]) + np.dot(Lb, Trapdoor[tree_level][1])
                if (int(R_i) == 0 and node_curr.child.get(k) is not None):
                    node = node_curr.child.get(k)
                    queue.append(node)
                    del(index[0])
            if queue == []:
                add_keyword(node_curr,id,index)
                break
            i += 1
    return search_Tree

def delete(search_Tree, Trapdoor): #可以删除包含该属性的所有叶子节点
    node_curr = search_Tree  # 关键词的头, 每遍历完一遍后需要重新初始化
    queue = []
    file = []
    queue.append(node_curr)
    tree_level = -1
    while queue:
        i = 0
        numberFlag = len(queue)
        tree_level = tree_level + 1
        while i < numberFlag:
            delkey = []
            node_curr = queue.pop(0)
            key = node_curr.child.keys()
            for k in key:
                La = np.array(k[0])
                Lb = np.array(k[1])
                R_i = np.dot(La, Trapdoor[tree_level][0]) + np.dot(Lb, Trapdoor[tree_level][1])
                if (int(R_i) == 0 and node_curr.child.get(k) is not None):
                    node = node_curr.child.get(k)
                    queue.append(node)
                    if node.id != None:
                        file.append(node.id)
                        delkey.append(k)
                        del(queue[-1])
            for value in delkey:
                del node_curr.child[value]
            i += 1
    return search_Tree,file

def updateindex(V, sk, split):
    r_t = np.random.randint(1, 10)  # 生成一个随机数，用于向量相乘
    V = V * r_t  #向量乘以一个随机数
    T = []
    split_index = np.array_split(V, split)
    for i,s in enumerate(split_index):
        lens = s.size
        S = sk[i][2]  # 提取私钥中的S
        r = np.random.randint(1, 10)  # 生成一个随机数，用于q划分，随机相加求和
        T_a = np.zeros(lens)
        T_b = np.zeros(lens)
        for j, vals in enumerate(S):
            if vals == 0:
                T_a[j] = T_b[j] = s[j]
            else:
                # 如果s_j=0
                T_a[j] = s[j] - r
                T_b[j] = r
                # T_a[j] = T_b[j] = s[j]
        T_P = np.inner(sk[i][0], T_a)  # 将M1矩阵的逆后与T_a点乘
        T_DP = np.inner(sk[i][1], T_b)  # 将M2矩阵的逆后与T_b点乘
        t = [tuple(T_P), tuple(T_DP)]
        T.append(t)
    return T


