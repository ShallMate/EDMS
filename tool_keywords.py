import csv

from Crypto.Cipher import AES
import base64
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

from attribute_tree import AgeTree
from tool import get_feature, get_age_dict, get_diag_dict


def get_attrkeyword_1000(path):
    df = pd.read_csv(path)
    keyword = []
    dicts = {}
    index = 0
    for key in get_feature(path):
        if key == 'age' or key == 'diag_1':
            continue
        key_ignore = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
        if key in key_ignore:
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
    return keyword, dicts


def get_attrvect_1000(df):
    age_dict = get_age_dict()
    diag_dict = get_diag_dict()
    raw_convert_data = np.array(df)
    f = raw_convert_data[:, 16:]
    age_list = raw_convert_data[:, 0]  # age
    diag_list = raw_convert_data[:, 1:16]  # diag列
    model_enc = OneHotEncoder()  # 建立标志转换模型对象（也称为哑编码对象）
    df_new2 = model_enc.fit_transform(f).toarray().astype(int)  # 标志转换
    vect_len = len(df_new2)  # 记录个数
    vect_len1 = len(df_new2[0]) + 15 * len(diag_dict[0]) + len(age_dict[0])  # 向量维度
    df_vect = np.zeros((vect_len, vect_len1), dtype=int)

    for i, vect in enumerate(df_new2):
        age = age_list[i]
        age_vect = age_dict[age]
        diag1 = diag_list[i][0]
        diag1_vect = diag_dict[diag1]
        temp_vect = np.concatenate((age_vect, diag1_vect), axis=0)
        for j in range(14):
            diag = diag_list[i][j + 1]
            diag_vect = diag_dict[diag]
            temp_vect = np.concatenate((temp_vect, diag_vect), axis=0)
        # diag1 = diag_list[i][0]
        # diag2 = diag_list[i][1]
        # diag3 = diag_list[i][2]
        # diag1_vect = diag_dict[diag1]
        # diag2_vect = diag_dict[diag2]
        # diag3_vect = diag_dict[diag3]
        #     vect = np.concatenate((age_vect,diag1_vect,diag2_vect,diag3_vect,vect), axis=0)
        vect = np.concatenate((temp_vect, vect), axis=0)
        df_vect[i] = vect
        # print(len(vect))
    return df_vect


def get_attrtrapvect_1000(path, search_word):
    keyword, dic = get_attrkeyword_1000(path)
    age_dict = get_age_dict()
    diag_dict = get_diag_dict()
    other_vect = [1] * len(keyword)
    age_vect = [1] * len(age_dict[0])
    diag1_vect = diag2_vect = diag3_vect = diag4_vect = diag5_vect = diag6_vect = \
        diag7_vect = diag8_vect = diag9_vect = diag10_vect = diag11_vect = diag12_vect = \
        diag13_vect = diag14_vect = diag15_vect =[1] * len(diag_dict[0])
    for key, val in search_word.items():
        if key == 'age':
            age_vect = age_dict[val]
        elif key == 'diag_1':
            diag1_vect = diag_dict[val]
        elif key == '1':
            diag2_vect = diag_dict[val]
        elif key == '2':
            diag3_vect = diag_dict[val]
        elif key == '3':
            diag4_vect = diag_dict[val]
        elif key == '4':
            diag5_vect = diag_dict[val]
        elif key == '5':
            diag6_vect = diag_dict[val]
        elif key == '6':
            diag7_vect = diag_dict[val]
        elif key == '7':
            diag8_vect = diag_dict[val]
        elif key == '8':
            diag9_vect = diag_dict[val]
        elif key == '9':
            diag10_vect = diag_dict[val]
        elif key == '10':
            diag11_vect = diag_dict[val]
        elif key == '11':
            diag12_vect = diag_dict[val]
        elif key == '12':
            diag13_vect = diag_dict[val]
        elif key == '13':
            diag14_vect = diag_dict[val]
        elif key == '14':
            diag15_vect = diag_dict[val]
        else:
            loc = dic[key][val]
            other_vect[loc] = 0
            for k, i in dic[key].items():
                if val == k:
                    other_vect[i] = 1
                else:
                    other_vect[i] = 0
    trap_vect = np.concatenate((age_vect, diag1_vect, diag2_vect, diag3_vect, diag4_vect,
                                diag5_vect, diag6_vect, diag7_vect, diag8_vect, diag9_vect,
                                diag10_vect, diag11_vect, diag12_vect, diag13_vect, diag14_vect,
                                diag15_vect,  other_vect), axis=0)
    return np.array(trap_vect)


if __name__ == '__main__':
    path = "doc/dataset/verif/1000-2000.CSV"
    # path = ""
    # key = '1234567890123454'  # 必须要16或着倍数
    search = {'race': 'Caucasian', 'gender': 'Female', 'admission_type_id': 5, 'age': '20-30', 'diag_1': 401}
    df = pd.read_csv(path)
    t = get_attrtrapvect_1000(path, search_word=search)
    print(len(t))
    get_attrvect_1000(df)
    # df_new = vect_attri(df)
    # print(df_new)
