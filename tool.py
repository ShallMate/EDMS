#!/usr/bin/env python
# -*- coding:utf-8 -*-
import csv

from Crypto.Cipher import AES
import base64
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import num_tree
from attribute_tree import AgeTree

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


# 加密
def aesEncrypt(key, data):
    '''
    AES的ECB模式加密方法
    :param key: 密钥
    :param data:被加密字符串（明文）
    :return:密文
    '''
    key = key.encode('utf8')
    # 字符串补位
    data = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
    result = cipher.encrypt(data.encode())
    encodestrs = base64.b64encode(result)
    enctext = encodestrs.decode('utf8')
    return enctext


# 解密
def aesDecrypt(key, data):
    '''

    :param key: 密钥
    :param data: 加密后的数据（密文）
    :return:明文
    '''
    key = key.encode('utf8')
    data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_ECB)

    # 去补位
    text_decrypted = unpad(cipher.decrypt(data))
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted


def cvsEncrypt(path, key):  # 生成密文
    df = pd.read_csv(path)
    data = np.array(df.loc[:, :])  # 按行读取文件
    # labels = list(df.columns.values) # 第一行标签
    # t = data.shape[0]  # 行数
    for val in data:
        to_str = ','.join(str(i) for i in val)  # 加密需要string类型，将数组转换为string类型
        with open('D:\ProgramData\PyProjects\Multi-keyword-fuzzy-searchable-encryption-main\doc\enfile\medical_enc.csv', 'a',
                  encoding='utf-8') as f:
            ecdata = aesEncrypt(key, to_str)
            f.write(ecdata + '\n')
        # print(ecdata)
        # data = aesDecrypt(key, ecdata)
        # print(data)


def get_feature(path):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        result = list(reader)
        feature = result[0]
        return feature


def get_keyword(path):
    df = pd.read_csv(path)
    keyword = []
    dicts = {}
    index = 0
    for key in get_feature(path):
        keyword1 = df[key].drop_duplicates().values.tolist()  # 获取数据并去重
        keyword1 = sorted(keyword1)
        sort_dict = {}
        for key_dict in keyword1:
            sort_dict1 = {key_dict: index}
            index = index + 1
            sort_dict.update(sort_dict1)
        dict1 = {key: sort_dict}
        # dicts = dict(dicts, **dict1)
        dicts.update(dict1)
        keyword = keyword + keyword1
    return keyword, dicts

def get_attrkeyword(path):
    df = pd.read_csv(path)
    all_keyword = [] #所有关键词
    keyword = [] #非属性树关键词
    dicts = {} #二重字典
    index = 0
    for key in get_feature(path):
        list = ['age', 'diag_1', 'diag_2', 'diag_3','rand1']
        if key in list:
            all_key = df[key].drop_duplicates().values.tolist()  # 获取数据并去重
            all_keyword = all_keyword + all_key
            continue
        keyword1 = df[key].drop_duplicates().values.tolist()  # 获取数据并去重
        keyword1 = sorted(keyword1)
        sort_dict = {}
        for key_dict in keyword1:
            sort_dict1 = {key_dict: index}
            index = index + 1
            sort_dict.update(sort_dict1)
        dict1 = {key: sort_dict}
        # dicts = dict(dicts, **dict1)
        dicts.update(dict1)
        keyword = keyword + keyword1
        all_keyword = all_keyword + keyword1
    return all_keyword, keyword, dicts


def get_vect(df):
    raw_convert_data = np.array(df)
    model_enc = OneHotEncoder()  # 建立标志转换模型对象（也称为哑编码对象）
    df_new2 = model_enc.fit_transform(raw_convert_data).toarray().astype(int)  # 标志转换
    return df_new2


def get_trapvect(path, search_word):  # search_word以字典的形式传入
    keyword, dic = get_keyword(path)
    trap_vect = [1] * len(keyword)
    for key, val in search_word.items():
        loc = dic[key][val]
        trap_vect[loc] = 0
        for k, i in dic[key].items():
            if val == k:
                trap_vect[i] = 1
            else:
                trap_vect[i] = 0
    return np.array(trap_vect)

def get_age_dict(): #年龄属性树
    trie = AgeTree()
    age_tree = [['1-100', '0-30', '0-10', (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)],
           ['1-100', '0-30', '10-20', (10, 11, 12, 13, 14, 15, 16, 17, 18, 19)],
           ['1-100', '0-30', '20-30', (20, 21, 22, 23, 24, 25, 26, 27, 28, 29)],
           ['1-100', '0-30', '*'],
           ['1-100', '30-60', '30-40', (30, 31, 32, 33, 34, 35, 36, 37, 38, 39)],
           ['1-100', '30-60', '40-50', (40, 41, 42, 43, 44, 45, 46, 47, 48, 49)],
           ['1-100', '30-60', '50-60', (50, 51, 52, 53, 54, 55, 56, 57, 58, 59)],
           ['1-100', '30-60', '*'],
           ['1-100', '60-100', '60-70', (60, 61, 62, 63, 64, 65, 66, 67, 68, 69)],
           ['1-100', '60-100', '70-80', (70, 71, 72, 73, 74, 75, 76, 77, 78, 79)],
           ['1-100', '60-100', '80-90', (80, 81, 82, 83, 84, 85, 86, 87, 88, 89)],
           ['1-100', '60-100', '90-100', (90, 91, 92, 93, 94, 95, 96, 97, 98, 99)]]
    trie.add_keywords_from_list(age_tree)
    age_dict = trie.build_dict()
    return age_dict

def get_diag_dict(): #diag树
    dict = np.load('./doc/dict/diag.npy', allow_pickle='TRUE')
    diag_dict = dict.item()
    return diag_dict

def get_num_dict(): #数字树
    num_dict = num_tree.num_dict(10000)
    return num_dict

def get_attrvect(df):
    age_dict = get_age_dict()
    diag_dict = get_diag_dict()
    num_dict = get_num_dict()
    raw_convert_data = np.array(df)
    f = raw_convert_data[:, 5:]
    age_list = raw_convert_data[:, 0] #age
    diag_list = raw_convert_data[:,1:4] #diag列
    num_list = raw_convert_data[:, 4]  # rand1列
    model_enc = OneHotEncoder()  # 建立标志转换模型对象（也称为哑编码对象）
    df_new2 = model_enc.fit_transform(f).toarray().astype(int)  # 标志转换
    vect_len = len(df_new2) # 记录个数
    vect_len1 = len(df_new2[0])+3*len(diag_dict[0])+len(age_dict[0])+len(num_dict[0]) #总向量维度
    df_vect = np.zeros((vect_len,vect_len1), dtype=int)
    for i, vect in enumerate(df_new2):
        age = age_list[i]
        diag1 = diag_list[i][0]
        diag2 = diag_list[i][1]
        diag3 = diag_list[i][2]
        rand1 = num_list[i]
        age_vect = age_dict[age]
        diag1_vect = diag_dict[diag1]
        diag2_vect = diag_dict[diag2]
        diag3_vect = diag_dict[diag3]
        rand1_vect = num_dict[rand1]
        vect = np.concatenate((age_vect,diag1_vect,diag2_vect,diag3_vect,rand1_vect,vect), axis=0)
        df_vect[i] = vect
    return df_vect

def get_attrtrapvect(path, search_word):
    allkeyword, keyword, dic = get_attrkeyword(path)
    age_dict = get_age_dict()
    diag_dict = get_diag_dict()
    num_dict = get_num_dict()
    other_vect = [1] * len(keyword)
    age_vect = [1] *len(age_dict[0])
    rand_vect = [1] * len(num_dict[0])
    diag1_vect = diag2_vect =diag3_vect = [1] * len(diag_dict[0])
    for key, val in search_word.items():
        if key =='age':
            age_vect = age_dict[val]
        elif key == 'diag_1':
            diag1_vect = diag_dict[val]
        elif key == 'diag_2':
            diag2_vect = diag_dict[val]
        elif key == 'diag_3':
            diag3_vect = diag_dict[val]
        elif key == 'rand1':
            rand_vect = num_dict[val]
        else:
            loc = dic[key][val]
            other_vect[loc] = 0
            for k, i in dic[key].items():
                if val == k:
                    other_vect[i] = 1
                else:
                    other_vect[i] = 0
    trap_vect = np.concatenate((age_vect,diag1_vect, diag2_vect, diag3_vect,rand_vect,other_vect), axis=0)
    return np.array(trap_vect)

def vect_len(df):
    vect = get_attrvect(df)
    lens = len(vect[0])
    return lens
