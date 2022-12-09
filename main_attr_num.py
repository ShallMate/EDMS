import random
import numpy as np
import tool
import csv
import pandas as pd
import warnings
import Update
from pre_tree import TrieTree


warnings.filterwarnings("ignore")

# 加密后数据集的形式 id，enc_medical
def enc_file(key, path, enc_path):
    df = pd.read_csv(path)
    data = np.array(df.loc[:, :])  # 按行读取文件
    # labels = list(df.columns.values) # 第一行标签
    # t = data.shape[0]  # 行数
    with open(enc_path, 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['id', 'enc_medical'])
        for id, val in enumerate(data):
            to_str = ','.join(str(i) for i in val)  # 加密需要string类型，将数组转换为string类型
            ecdata = tool.aesEncrypt(key, to_str)
            csv_writer.writerow([id, ecdata])
        # print(ecdata)
        # data = aesDecrypt(key, ecdata)
        # print(data)


def BuildIndex(sk, V, V_split):
    trie = TrieTree()
    trie.add_keywords_from_list(V, V_split)  # 创建树
    Enindex = trie.BuildIndextree(sk)
    return Enindex


def Trapdoor(V, sk, split):
    r_t = np.random.randint(1, 10)  # 生成一个随机数，用于向量相乘
    V = V * r_t  # 向量乘以一个随机数
    T = []
    split_index = np.array_split(V, split)
    for i, s in enumerate(split_index):
        lens = s.size
        S = sk[i][2]  # 提取私钥中的S
        r = np.random.randint(1, 10)  # 生成一个随机数，用于q划分，随机相加求和
        T_a = np.zeros(lens)
        T_b = np.zeros(lens)
        for j, vals in enumerate(S):
            if vals == 1:
                T_a[j] = T_b[j] = s[j]
            else:
                # 如果s_j=0
                T_a[j] = s[j] - r
                T_b[j] = r
                # T_a[j] = T_b[j] = s[j]
        T_P = np.inner(sk[i][0], T_a)  # 将M1矩阵的逆后与T_a点乘
        T_DP = np.inner(sk[i][1], T_b)  # 将M2矩阵的逆后与T_b点乘
        t = np.array([T_P, T_DP])
        T.append(t)
    return T


def Search(search_Tree, Trapdoor):  # 可以效仿层次遍历
    File = []
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
                    if node.id != None:
                        File.append(node.id)
            i += 1
    return File


# 根据数据集的id筛选加密的数据
def get_file(Index, key):
    df = pd.read_csv("doc/enfile/medical_index.csv")
    with open('./doc/medical_file.csv', 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        for i in Index:
            enc_data = df.loc[df['id'] == i, 'enc_medical'].tolist()
            data = tool.aesDecrypt(key, enc_data[0])
            csv_writer.writerow([data])


# 插入相应的节点，并添加相应的文档在数据集类，id的问题需要解决（自动增加的id，而不是指定的id）
def update_insert(enc_path, ecdata, Enindex_tree, index, trapdoor, id):
    with open(enc_path, 'a', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([id, ecdata])
    insert_tree = Update.insert(Enindex_tree, trapdoor, index, id)
    return insert_tree


# 删除对应的文件的id索引后对应的文件（对应文件指派相应的id比较合适）
def update_delete(Enindex_tree, trapdoor,enc_path):
    delete_tree,file = Update.delete(Enindex_tree, trapdoor)
    df = pd.read_csv("doc/enfile/medical_index.csv")
    for i in file:
        df = df.drop(df.index[df['id'] == i])
    data = np.array(df.loc[:, :])  # 按行读取文件
    with open(enc_path, 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['id', 'enc_medical'])
        for val in data:
            csv_writer.writerow(val)
    return delete_tree

